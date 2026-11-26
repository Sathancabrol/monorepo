import {randomUUID} from 'node:crypto';
const BASE='http://127.0.0.1:8188';
export function workflow({checkpoint,prompt,filename,size,steps,denoise,seed}){
 return {
  '1':{class_type:'CheckpointLoaderSimple',inputs:{ckpt_name:checkpoint}},
  '2':{class_type:'CLIPTextEncode',inputs:{clip:['1',1],text:prompt}},
  '3':{class_type:'CLIPTextEncode',inputs:{clip:['1',1],text:''}},
  '4':{class_type:'LoadImage',inputs:{image:filename}},
  '5':{class_type:'ImageScale',inputs:{image:['4',0],upscale_method:'bilinear',width:size,height:size,crop:'center'}},
  '6':{class_type:'VAEEncode',inputs:{pixels:['5',0],vae:['1',2]}},
  '7':{class_type:'KSampler',inputs:{model:['1',0],positive:['2',0],negative:['3',0],latent_image:['6',0],seed,steps,cfg:1,sampler_name:'euler_ancestral',scheduler:'normal',denoise}},
  '8':{class_type:'VAEDecode',inputs:{samples:['7',0],vae:['1',2]}},
  '9':{class_type:'PreviewImage',inputs:{images:['8',0]}}
 };
}
export function validate(d){
 if(!d||typeof d.checkpoint!=='string'||!d.checkpoint||d.checkpoint.length>240||typeof d.prompt!=='string'||d.prompt.length>1000)throw Error('Checkpoint ou prompt invalide');
 if(![256,320,384,512].includes(d.size)||!Number.isInteger(d.steps)||d.steps<2||d.steps>8||!Number.isFinite(d.denoise)||d.denoise<.25||d.denoise>1||d.steps*d.denoise<1||!Number.isSafeInteger(d.seed)||d.seed<0)throw Error('Réglages invalides (steps × denoise ≥ 1)');
 if(typeof d.image!=='string'||d.image.length>900000||!/^data:image\/jpeg;base64,[A-Za-z0-9+/]+={0,2}$/.test(d.image))throw Error('JPEG attendu');
 const bytes=Buffer.from(d.image.split(',')[1],'base64');if(bytes.length<8||bytes[0]!==255||bytes[1]!==216)throw Error('JPEG invalide');
 return bytes;
}
export function makeRealityHandler({fetcher=fetch,pause=ms=>new Promise(r=>setTimeout(r,ms)),maxPoll=120}={}){
 let busy=false, pending=null;
 const sessionInput='olympus-reality-'+randomUUID()+'.jpg';
 async function request(path,opts={}){
  const r=await fetcher(BASE+path,{...opts,signal:AbortSignal.timeout(8000)});
  if(!r.ok)throw Error('ComfyUI HTTP '+r.status);return r;
 }
 async function models(){
  const j=await (await request('/object_info/CheckpointLoaderSimple')).json();
  return j.CheckpointLoaderSimple?.input?.required?.ckpt_name?.[0]||[];
 }
 const send=(res,status,data)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
 return async function handle(req,res,url,bodyJson){
  if(url.pathname==='/api/reality/models'&&req.method==='GET'){
   try{send(res,200,{models:await models(),busy});}catch(e){send(res,503,{error:'ComfyUI indisponible : '+e.message});}return true;
  }
  if(url.pathname!=='/api/reality/frame'||req.method!=='POST')return false;
  if(busy){send(res,409,{error:'Une génération est déjà en cours'});return true;}
  busy=true;
  try{
   let d,bytes;try{d=await bodyJson(req);bytes=validate(d);}catch(e){send(res,400,{error:e.message});return true;}
   if(pending){
    const old=await (await request('/history/'+pending)).json();
    if(!old[pending]){send(res,409,{error:'Génération précédente encore en attente dans ComfyUI. Vérifier sa file.'});return true;}
    pending=null;
   }
   if(!(await models()).includes(d.checkpoint)){send(res,400,{error:'Checkpoint non installé'});return true;}
   const form=new FormData();
   form.append('image',new Blob([bytes],{type:'image/jpeg'}),sessionInput);form.append('type','input');form.append('overwrite','true');
   const uploaded=await (await request('/upload/image',{method:'POST',body:form})).json();
   if(!uploaded.name||uploaded.subfolder)throw Error('Réponse upload inattendue');
   const result=await (await request('/prompt',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:workflow({...d,filename:uploaded.name}),client_id:'olympus-reality'})})).json();
   if(!/^[a-f0-9-]{36}$/i.test(result.prompt_id||''))throw Error('ID de génération invalide');
   pending=result.prompt_id;
   for(let i=0;i<maxPoll;i++){
    const hist=await (await request('/history/'+pending)).json(),job=hist[pending];
    if(job){
     pending=null;
     if(job.status?.status_str==='error')throw Error('Échec de génération : vérifier la console ComfyUI');
     const img=job.outputs?.['9']?.images?.[0];
     if(!img?.filename)throw Error('Aucune image générée');
     const params=new URLSearchParams({filename:img.filename,subfolder:img.subfolder||'',type:img.type||'output'});
     const output=await request('/view?'+params);
     const type=output.headers.get('content-type')||'';
     if(!/^image\/(png|jpeg|webp)/i.test(type))throw Error('Sortie image invalide');
     const buffer=Buffer.from(await output.arrayBuffer());if(buffer.length>8*1024*1024)throw Error('Sortie trop grande');
     send(res,200,{image:'data:'+type.split(';')[0]+';base64,'+buffer.toString('base64')});return true;
    }
    await pause(1000);
   }
   send(res,504,{error:'Délai dépassé. La file ComfyUI peut toujours travailler ; aucun nouveau job avant sa fin.'});
  }catch(e){send(res,502,{error:String(e.message).slice(0,250)});}
  finally{busy=false;}
  return true;
 };
}

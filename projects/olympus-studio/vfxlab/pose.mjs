// Optional local-only pose and person segmentation. No CDN at runtime.
export class RealityPose {
 constructor(){this.task=null;this.loading=false;this.active=false;this.last=0;this.next=0;this.points=[];this.center=null;this.mask=document.createElement('canvas');this.ctx=this.mask.getContext('2d');this.valid=false;}
 async start(){
  if(this.loading)return;this.loading=true;
  try{
   if(!this.task){
    const {FilesetResolver,PoseLandmarker}=await import('./vendor/vision_bundle.mjs');
    const files=await FilesetResolver.forVisionTasks('/vfxlab/vendor/wasm');
    this.task=await PoseLandmarker.createFromOptions(files,{baseOptions:{modelAssetPath:'/vfxlab/vendor/pose_landmarker_lite.task',delegate:'CPU'},runningMode:'VIDEO',numPoses:1,outputSegmentationMasks:true});
   }
   this.active=true;this.reset();
  }finally{this.loading=false;}
 }
 reset(){this.points=[];this.center=null;this.valid=false;this.last=0;this.next=0;}
 stop(){this.active=false;this.reset();}
 close(){this.stop();this.task?.close();this.task=null;}
 tick(canvas,t){
  if(!this.active||!this.task||t<this.next)return;
  const begin=performance.now();let result;
  try{
   result=this.task.detectForVideo(canvas,t);
   this.points=result.landmarks?.[0]||[];
   const p=[11,12,23,24].map(i=>this.points[i]).filter(x=>x&&x.visibility>.45);
   this.center=p.length>=2?{x:p.reduce((s,x)=>s+x.x,0)/p.length,y:p.reduce((s,x)=>s+x.y,0)/p.length}:null;
   this.valid=false;const m=result.segmentationMasks?.[0];
   if(m&&this.points.length){
    this.mask.width=m.width;this.mask.height=m.height;
    const values=m.getAsFloat32Array(),im=this.ctx.createImageData(m.width,m.height);
    for(let i=0;i<values.length;i++){const a=Math.max(0,Math.min(1,(values[i]-.35)/.35));im.data[i*4]=255;im.data[i*4+1]=255;im.data[i*4+2]=255;im.data[i*4+3]=Math.round(a*255);}
    this.ctx.putImageData(im,0,0);this.valid=true;
   }
   this.last=t;
  }finally{result?.close?.();this.next=t+Math.max(150,(performance.now()-begin)*3);}
 }
 fresh(t){return this.active&&t-this.last<1000&&this.points.length>0;}
 draw(ctx,w,h,t){
  if(!this.fresh(t))return;
  const links=[[11,12],[11,13],[13,15],[12,14],[14,16],[11,23],[12,24],[23,24],[23,25],[25,27],[24,26],[26,28],[0,7],[0,8]];
  ctx.save();ctx.strokeStyle='#7ef5db';ctx.fillStyle='#b4fff0';ctx.lineWidth=2;
  for(const [i,j] of links){const a=this.points[i],b=this.points[j];if(!a||!b||a.visibility<.45||b.visibility<.45)continue;ctx.beginPath();ctx.moveTo(a.x*w,a.y*h);ctx.lineTo(b.x*w,b.y*h);ctx.stroke();}
  for(const p of this.points){if(p.visibility<.45)continue;ctx.beginPath();ctx.arc(p.x*w,p.y*h,2.5,0,Math.PI*2);ctx.fill();}
  ctx.restore();
 }
}

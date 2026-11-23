/* BTP Studio v4 — editable Bruckner-style cumulative earthworks curve.
 * Trapezoidal sections in place. Transport matching and logistics not inferred. */
(function(){
"use strict";
const KEY="btp_bruckner_v4",PROJECT="btp_project_active_v1";
const $=id=>document.getElementById(id);
const fmt=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:1});
const defaults=()=>[
 {pk:0,cut:2,fill:0},{pk:100,cut:4,fill:0.4},{pk:200,cut:2,fill:1.5},
 {pk:300,cut:0.5,fill:4},{pk:400,cut:0.4,fill:2.5},{pk:500,cut:2,fill:0.7}
];
function id(){try{return localStorage.getItem(PROJECT)||"sans-dossier"}catch(e){return "sans-dossier"}}
function source(){try{const x=JSON.parse(localStorage.getItem(KEY)||"{}");return x&&typeof x==="object"?x:{}}catch(e){return {}}}
function rows(){const v=source()[id()];return Array.isArray(v)&&v.length>=2?v:defaults()}
function valid(r){
 if(!Array.isArray(r)||r.length<2||r.length>100)throw Error("Il faut 2 à 100 profils");
 for(const t of r)if(![t.pk,t.cut,t.fill].every(v=>Number.isFinite(v)&&v>=0))throw Error("Sections négatives ou non numériques");
 for(let i=1;i<r.length;i++)if(r[i].pk<=r[i-1].pk)throw Error("PK non strictement croissants");
 return r;
}
function model(raw){
 valid(raw);let cum=0,cut=0,fill=0;
 const result=raw.map((t,i)=>{
  const delta=i===0?0:t.pk-raw[i-1].pk;
  const vCut=i===0?0:delta*(t.cut+raw[i-1].cut)/2,vFill=i===0?0:delta*(t.fill+raw[i-1].fill)/2;
  cut+=vCut;fill+=vFill;cum+=vCut-vFill;
  return {...t,delta,vCut,vFill,cum};
 });
 return {rows:result,cut,fill,balance:cut-fill};
}
function store(raw){const s=source();s[id()]=valid(raw);localStorage.setItem(KEY,JSON.stringify(s))}
function input(n,field,index){return '<input aria-label="Profil '+index+' '+field+'" type="number" min="0" max="100000000" step="any" data-b4-index="'+index+'" data-b4-key="'+field+'" value="'+n+'" style="width:80px;background:#102129;color:#edfaef;border:1px solid #50666c;border-radius:5px;padding:5px">'}
function info(id,value){const el=$(id);if(el)el.textContent=value}
function render(){
 const view=$("tech-bruckner-view"),tbody=$("bruckner-table-body");if(!view||!tbody)return;
 let m;
 try{m=model(rows())}catch(e){tbody.textContent=e.message;return}
 tbody.innerHTML=m.rows.map((r,i)=>'<tr><td style="padding:5px">'+input(r.pk,"pk",i)+'</td><td style="padding:5px">'+fmt(r.delta)+'</td>'+
 '<td style="padding:5px">'+input(r.cut,"cut",i)+'</td><td style="padding:5px">'+input(r.fill,"fill",i)+'</td>'+
 '<td style="padding:5px">'+fmt(r.vCut)+'</td><td style="padding:5px">'+fmt(r.vFill)+'</td>'+
 '<td style="padding:5px">'+fmt(r.cum)+'</td><td style="padding:5px;color:#dec8a0">À étudier</td></tr>').join("");
 info("bruckner-total-deb",fmt(m.cut)+" m³");
 info("bruckner-total-rem",fmt(m.fill)+" m³");
 info("bruckner-solde",(m.balance>=0?"+":"")+fmt(m.balance)+" m³");
 info("bruckner-dmt","Non calculée");
 for(const [result,label] of [["bruckner-total-deb","Déblais en place (exemple)"],["bruckner-total-rem","Remblais géométriques (exemple)"],["bruckner-dmt","Distance de transport : non calculable ici"]]){
  const node=$(result);if(node&&node.previousElementSibling)node.previousElementSibling.textContent=label;
 }
 draw(m);
}
function draw(m){
 const cv=$("bruckner-canvas");if(!cv||!cv.getContext)return;const ctx=cv.getContext("2d");
 const W=cv.width,H=cv.height,padL=65,padR=25,padT=18,padB=35;
 ctx.clearRect(0,0,W,H);ctx.fillStyle="#0b1520";ctx.fillRect(0,0,W,H);
 const arr=m.rows,lo=Math.min(0,...arr.map(x=>x.cum)),hi=Math.max(0,...arr.map(x=>x.cum));
 const diff=Math.max(1,hi-lo),span=Math.max(1,arr[arr.length-1].pk-arr[0].pk);
 const xx=pk=>padL+(pk-arr[0].pk)/span*(W-padL-padR),yy=v=>H-padB-(v-lo)/diff*(H-padB-padT);
 ctx.strokeStyle="#3a5960";ctx.lineWidth=1;for(let i=0;i<5;i++){const y=padT+i*(H-padB-padT)/4;ctx.beginPath();ctx.moveTo(padL,y);ctx.lineTo(W-padR,y);ctx.stroke()}
 ctx.beginPath();ctx.strokeStyle="#92b6a5";ctx.moveTo(padL,yy(0));ctx.lineTo(W-padR,yy(0));ctx.stroke();
 ctx.beginPath();ctx.strokeStyle="#7fcdd0";ctx.lineWidth=3;arr.forEach((r,i)=>{if(i===0)ctx.moveTo(xx(r.pk),yy(r.cum));else ctx.lineTo(xx(r.pk),yy(r.cum))});ctx.stroke();
 arr.forEach(r=>{ctx.beginPath();ctx.fillStyle="#b8ed83";ctx.arc(xx(r.pk),yy(r.cum),4,0,Math.PI*2);ctx.fill()});
 ctx.fillStyle="#cfe2d9";ctx.font="12px system-ui";ctx.fillText("m³ cumulés",8,15);ctx.fillText(fmt(hi),8,30);ctx.fillText(fmt(lo),8,H-padB);
 ctx.fillText("PK "+arr[0].pk,padL,H-10);ctx.fillText("PK "+arr[arr.length-1].pk,W-90,H-10);
}
function update(e){
 const node=e.target;if(!node.matches("[data-b4-index]"))return;
 const index=Number(node.dataset.b4Index),key=node.dataset.b4Key,r=rows();
 const n=Number(node.value);if(!Number.isFinite(n)||n<0){node.setCustomValidity("Valeur positive requise");node.reportValidity();return}
 const next=r.map(x=>({...x}));next[index][key]=n;
 try{valid(next);store(next);render();}catch(err){node.setCustomValidity(err.message);node.reportValidity();node.setCustomValidity("")}
}
window.resetBrucknerData=function(){
 if(!confirm("Réinitialiser les profils Bruckner à des données fictives de démonstration ?"))return;
 store(defaults());render();
};
window.exportBrucknerCSV=function(){
 const m=model(rows()),fields=["pk","delta","cut","fill","vCut","vFill","cum"];
 const cols=["PK (m)","Distance partielle (m)","Section déblai (m²)","Section remblai (m²)","Volume déblai géométrique (m³)","Volume remblai géométrique (m³)","Cumul géométrique (m³)"];
 const csv=[cols.join(";"),...m.rows.map(r=>fields.map(k=>String(r[k]).replace(".",",")).join(";"))].join("\r\n");
 const url=URL.createObjectURL(new Blob(["\uFEFF"+"# EXEMPLE / SAISIE LOCALE - à contrôler, sans correction foisonnement/compactage\r\n"+csv],{type:"text/csv;charset=utf-8"}));
 const a=document.createElement("a");a.href=url;a.download="btp-profil-bruckner-"+id()+".csv";a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);
};
function init(){
 const v=$("tech-bruckner-view"),table=$("bruckner-table-body");if(!v||!table)return;
 table.addEventListener("change",update);
 const header=v.querySelector(".card-header")||v.querySelector(".card");
 if(header&&!$("btp-bruckner-add")){
  const add=document.createElement("button");add.id="btp-bruckner-add";add.className="btn btn-secondary";add.textContent="+ Profil PK";add.style.margin="8px";add.onclick=function(){
   const r=rows(),last=r[r.length-1];
   if(r.length>=100){alert("Maximum 100 profils.");return}
   try{store([...r,{pk:last.pk+100,cut:last.cut,fill:last.fill}]);render()}catch(e){alert(e.message)}
  };
  header.appendChild(add);
 }
 const p=document.createElement("p");p.textContent="Profil géométrique de démonstration : sections interpolées entre PK. Ne constitue pas une épure de transport optimisée. Calcul de distances/mouvements de matériaux et facteurs de foisonnement à effectuer séparément.";p.style.cssText="font-size:11px;color:#edc996;margin:8px 0 12px";v.insertBefore(p,v.firstChild);
 render();
 window.addEventListener("storage",e=>{if(e.key===KEY||e.key===PROJECT)render()});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
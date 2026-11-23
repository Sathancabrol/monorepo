/* BTP Studio — corrective calculations, verified dimensions and explicit assumptions.
   Calculates engineering orders of magnitude ONLY. No normative or contractual certification. */
(function(root,factory){
  "use strict";
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  if(root)root.BTPMathV4=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
  "use strict";
  function valid(x,label,min,max){const n=Number(x);if(!Number.isFinite(n)||n<min||n>max)throw Error(label+" : valeur invalide");return n}
  function hydraulic(dn,K,slopePct,fillPct){
    const d=valid(dn,"Diamètre mm",1,5000)/1000,k=valid(K,"Strickler K",1,200),s=valid(slopePct,"Pente %",0,100)/100;
    const f=valid(fillPct,"Remplissage %",0.1,100)/100,r=d/2;
    const aFull=Math.PI*r*r,rhFull=d/4;
    const theta=2*Math.acos(Math.max(-1,Math.min(1,1-2*f)));
    const a=r*r*(theta-Math.sin(theta))/2,p=r*theta,rh=p>0?a/p:0;
    const v=k*Math.pow(rh,2/3)*Math.sqrt(s),fullV=k*Math.pow(rhFull,2/3)*Math.sqrt(s);
    return {areaM2:a,rhM:rh,perimeterM:p,qLs:a*v*1000,qFullLs:aFull*fullV*1000,vMps:v,fullV,fillRatio:f};
  }
  function basin(ha,c,rainMm,outflowLsPerHa){
    const area=valid(ha,"Surface ha",.000001,100000),coef=valid(c,"Coefficient",0,1),
      rain=valid(rainMm,"Pluie mm",0,1000),q=valid(outflowLsPerHa,"Débit fuite L/s/ha",0,10000);
    return {grossRunoffM3:area*10000*rain/1000*coef,allowedLs:q*area};
  }
  function electric(powerW,lengthM,sectionMm2,material,phase){
    const P=valid(powerW,"Puissance W",0,1e10),L=valid(lengthM,"Longueur",0,1e6),S=valid(sectionMm2,"Section",.01,1000);
    if(!["cuivre","alu"].includes(material))throw Error("Conducteur invalide");
    if(!["mono","tri"].includes(phase))throw Error("Alimentation invalide");
    const rho=material==="cuivre"?.0225:.036,voltage=phase==="mono"?230:400;
    // Resistive-only idealization, cos(phi)=1, no reactance or thermal derating.
    const ib=phase==="mono"?P/voltage:P/(Math.sqrt(3)*voltage);
    const deltaU=(phase==="mono"?2:Math.sqrt(3))*rho*L*ib/S;
    return {currentA:ib,dropV:deltaU,dropPct:deltaU/voltage*100,voltage};
  }
  return Object.freeze({hydraulic,basin,electric});
});
(function(){
"use strict";
const api=window.BTPMathV4;if(!api)return;
const el=id=>document.getElementById(id);
const v=id=>el(id)?.value;
const fr=(n,places=2)=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:places});
function show(id,text){const node=el(id);if(node)node.textContent=text}
function info(target,text){
  const node=el(target);if(!node)return;const panel=node.closest(".card")||node.parentElement;
  if(panel&&!panel.querySelector('[data-btp-math-notice="'+target+'"]')){
    const p=document.createElement("p");p.dataset.btpMathNotice=target;
    p.style.cssText="margin:10px 0 0;color:#efc695;font-size:11px;line-height:1.45";
    p.textContent=text;panel.appendChild(p);
  }
}
window.updateHydrauliqueCalculation=function(){
 try{
  const q=api.hydraulic(v("hydrau-dn"),v("hydrau-materiau"),v("hydrau-pente"),v("hydrau-fill"));
  show("hydrau-qps-res",fr(q.qFullLs)+" L/s");show("hydrau-q-res",fr(q.qLs)+" L/s");
  show("hydrau-v-res",fr(q.vMps,3)+" m/s");
  show("hydrau-autocurage-res","Vitesse calculée, autocurage à vérifier");
  show("hydrau-s-detail",fr(q.areaM2,5)+" m²");show("hydrau-rh-detail",fr(q.rhM,5)+" m");
  show("hydrau-l-detail",fr(q.perimeterM,4)+" m");
  info("hydrau-autocurage-res","Manning–Strickler, écoulement uniforme supposé, pente hydraulique égale à la pente déclarée. Ne détermine pas seul l’autocurage ni la conformité au CCTP.");
 }catch(e){show("hydrau-q-res","Saisie à corriger");show("hydrau-autocurage-res",e.message)}
};
window.updateBassinCalculation=function(){
 try{
  const b=api.basin(v("bassin-surface"),v("bassin-coef-c"),v("bassin-pluie"),v("bassin-qfuite-spec"));
  show("bassin-volume-res",fr(b.grossRunoffM3,1)+" m³ (brut)");
  show("bassin-qfuite-total-res",fr(b.allowedLs)+" L/s");
  show("bassin-ajutage-res","Indéterminé");
  info("bassin-ajutage-res","Volume de ruissellement brut = surface × pluie × coefficient. Ce n’est PAS le volume utile de bassin : une pluie de projet (hyétogramme, durée), l’hydrogramme, l’infiltration et la loi de vidange sont indispensables. Ajutage non dimensionné.");
 }catch(e){show("bassin-volume-res","Saisie à corriger");show("bassin-ajutage-res",e.message)}
};
window.updateElectriqueCalculation=function(){
 try{
  const e=api.electric(v("elec-puissance"),v("elec-longueur"),v("elec-section"),v("elec-metal"),v("elec-type-alim"));
  show("elec-ib-res",fr(e.currentA)+" A");
  show("elec-deltau-res",fr(e.dropV)+" V ("+fr(e.dropPct)+" %)");
  show("elec-conformite-res",e.dropPct<=5?"Sous seuil indicatif 5 %":"Au-dessus de 5 % (hypothèse)");
  info("elec-conformite-res","Calcul résistif simplifié : cos φ = 1, pas de réactance, d’harmoniques ni d’échauffement complémentaire. Ne prouve pas le respect des normes NF C 15-100 / 17-200 ; vérification par professionnel requise.");
 }catch(e){show("elec-deltau-res","Saisie à corriger");show("elec-conformite-res",e.message)}
};
window.updateEPCalculation=function(){
 const h=Number(v("ep-hauteur")),d=Number(v("ep-interdist"));
 if(!(h>0&&d>0)){show("ep-lux-res","Saisie à corriger");return}
 show("ep-lux-res","Non calculable : données photométriques nécessaires");
 info("ep-lux-res","La hauteur et l’espacement ne suffisent pas à calculer un éclairement (lux). Ajouter flux lumineux, distribution photométrique, disposition, réflectances et facteur de maintenance, puis vérifier selon les prescriptions du projet. Rapport espacement/hauteur indicatif : "+fr(d/h)+".");
};
function initialize(){
 if(el("hydrau-dn"))window.updateHydrauliqueCalculation();
 if(el("bassin-surface"))window.updateBassinCalculation();
 if(el("elec-section"))window.updateElectriqueCalculation();
 if(el("ep-interdist"))window.updateEPCalculation();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initialize);else initialize();
})();
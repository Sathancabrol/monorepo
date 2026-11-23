/* BTP technical calculators V1. Independent educational calculations, no regulatory certification.
 * Runs locally, without network calls. */
(function(root){
"use strict";
const EPS=1e-10;
function positive(value,name,zeroAllowed=false){
  if(value===null||value===undefined||String(value).trim()==="")throw Error(name+" : valeur manquante");
  const n=Number(value);
  if(!Number.isFinite(n)||(zeroAllowed?n<0:n<=0))throw Error(name+" : valeur invalide");
  return n;
}
function hydraulic(o){
 const k=positive(o.k,"Strickler"), d=positive(o.diameterMm,"Diamètre")/1000;
 const slope=positive(o.slopePct,"Pente")/100;
 const f=positive(o.fillPct,"Remplissage")/100;
 if(f>1)throw Error("Remplissage supérieur à 100 %");
 const radius=d/2,theta=Math.acos(Math.max(-1,Math.min(1,1-2*f)));
 const area=radius*radius*(theta-Math.sin(theta)*Math.cos(theta));
 const perimeter=2*radius*theta;
 const fullArea=Math.PI*radius*radius, fullR=d/4;
 const qFull=k*fullArea*Math.pow(fullR,2/3)*Math.sqrt(slope);
 const rh=area/perimeter;
 const velocity=k*Math.pow(rh,2/3)*Math.sqrt(slope);
 return {qFullLs:qFull*1000,qLs:velocity*area*1000,velocityMs:velocity,areaM2:area,hydraulicRadiusM:rh,wetPerimeterM:perimeter};
}
function basin(o){
 const ha=positive(o.areaHa,"Surface"),c=positive(o.runoff,"Ruissellement");
 if(c>1)throw Error("Coefficient supérieur à 1");
 const rain=positive(o.rainMm,"Pluie"),specific=positive(o.outflowLsHa,"Débit de fuite",true);
 // Gross runoff volume only: duration and hydrograph are unknown.
 return {grossRunoffM3:ha*10000*(rain/1000)*c,outflowLs:ha*specific,orificeMm:null};
}
function electrical(o){
 const phase=o.phase==="tri"?"tri":"mono";
 const voltage=phase==="tri"?400:230;
 const rho=o.metal==="alu"?0.036:0.0225;
 const power=positive(o.powerW,"Puissance"),length=positive(o.lengthM,"Longueur");
 const section=positive(o.sectionMm2,"Section");
 // Resistive approximation, unity power factor, excludes reactance and cable temperature.
 const current=power/(phase==="tri"?Math.sqrt(3)*voltage:voltage);
 const drop=(phase==="tri"?Math.sqrt(3):2)*rho*length*current/section;
 return {currentA:current,dropV:drop,dropPct:100*drop/voltage,model:"Estimation résistive cos φ=1 ; non normative"};
}
function lighting(o){
 const height=positive(o.heightM,"Hauteur"),spacing=positive(o.spacingM,"Interdistance");
 return {ratio:spacing/height,estimatedLux:null,explanation:"Éclairement non calculable sans flux lumineux, photométrie, largeur et facteur de maintenance."};
}
function fmt(n,digits=2){return Number.isFinite(n)?n.toLocaleString("fr-FR",{maximumFractionDigits:digits,minimumFractionDigits:digits}):"—";}
function set(id,text){const el=document.getElementById(id);if(el)el.textContent=text;}
function value(id){const el=document.getElementById(id);return el?el.value:null;}
function safe(run,ids){try{run()}catch(e){ids.forEach(id=>set(id,"Saisie invalide"));console.warn("[BTP calcul indicatif]",e.message);}}
function updateHydrauliqueCalculation(){
 safe(()=>{const r=hydraulic({k:value("hydrau-materiau"),diameterMm:value("hydrau-dn"),slopePct:value("hydrau-pente"),fillPct:value("hydrau-fill")});
 set("hydrau-qps-res",fmt(r.qFullLs)+" L/s");set("hydrau-q-res",fmt(r.qLs)+" L/s");
 set("hydrau-v-res",fmt(r.velocityMs)+" m/s");
 set("hydrau-autocurage-res","Vitesse indicative — vérification métier requise");
 set("hydrau-s-detail",fmt(r.areaM2,4)+" m²");set("hydrau-rh-detail",fmt(r.hydraulicRadiusM,4)+" m");
 set("hydrau-l-detail",fmt(r.wetPerimeterM,4)+" m");
 },["hydrau-qps-res","hydrau-q-res","hydrau-v-res","hydrau-autocurage-res"]);
}
function updateBassinCalculation(){
 safe(()=>{const r=basin({areaHa:value("bassin-surface"),runoff:value("bassin-coef-c"),rainMm:value("bassin-pluie"),outflowLsHa:value("bassin-qfuite-spec")});
 set("bassin-volume-res",fmt(r.grossRunoffM3)+" m³ (volume brut)");
 set("bassin-qfuite-total-res",fmt(r.outflowLs)+" L/s");
 set("bassin-ajutage-res","Non dimensionné — hydrogramme requis");
 },["bassin-volume-res","bassin-qfuite-total-res","bassin-ajutage-res"]);
}
function updateElectriqueCalculation(){
 safe(()=>{const r=electrical({phase:value("elec-type-alim"),metal:value("elec-metal"),powerW:value("elec-puissance"),lengthM:value("elec-longueur"),sectionMm2:value("elec-section")});
 set("elec-ib-res",fmt(r.currentA)+" A");
 set("elec-deltau-res",fmt(r.dropV)+" V ("+fmt(r.dropPct)+" %)");
 set("elec-conformite-res","Estimation résistive — conformité non évaluée");
 },["elec-ib-res","elec-deltau-res","elec-conformite-res"]);
}
function updateEPCalculation(){
 safe(()=>{const r=lighting({heightM:value("ep-hauteur"),spacingM:value("ep-interdist")});
 set("ep-lux-res","Non calculable sans photométrie (espacement/H = "+fmt(r.ratio)+")");
 },["ep-lux-res"]);
}
const api={hydraulic,basin,electrical,lighting};
if(typeof module!=="undefined"&&module.exports)module.exports=api;
if(root&&root.document){
 root.BTPTechnicalCalculators=api;
 Object.assign(root,{updateHydrauliqueCalculation,updateBassinCalculation,updateElectriqueCalculation,updateEPCalculation});
 function init(){[updateHydrauliqueCalculation,updateBassinCalculation,updateElectriqueCalculation,updateEPCalculation].forEach(f=>f());}
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
}
})(typeof window!=="undefined"?window:typeof globalThis!=="undefined"?globalThis:null);

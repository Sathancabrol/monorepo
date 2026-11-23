/* BTP Studio v4 - inventory ledger and fleet maintenance records.
 * Manual data only; legacy simulated cards/telemetry remain separate.
 * No server, no online GPS, no equipment compliance certification. */
(function(){
"use strict";
const STOCK="btp_local_stock_movements_v4",FLEET="btp_local_fleet_v4";
const $=id=>document.getElementById(id),fr=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:2});
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const today=()=>new Date().toISOString().slice(0,10),stamp=()=>new Date().toISOString();
function get(key){try{const v=JSON.parse(localStorage.getItem(key)||"[]");return Array.isArray(v)?v:[]}catch(e){return []}}
function save(key,rows){if(rows.length>3000)throw Error("Maximum 3 000 enregistrements");localStorage.setItem(key,JSON.stringify(rows))}
function ensureId(id){const x=String(id??"").trim().slice(0,80);if(!x)throw Error("Référence obligatoire");return x}
function positive(v){const n=Number(v);if(!Number.isFinite(n)||n<=0||n>1e7)throw Error("Quantité positive obligatoire");return n}
function fdownload(name,body){
 const u=URL.createObjectURL(new Blob(["\uFEFF"+body],{type:"text/csv;charset=utf-8"})),a=document.createElement("a");a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),3000)
}
function csv(v){let s=String(v??"");if(/^[=+\-@\t\r]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"'}
function rowsToCSV(headers,rows){return headers.map(h=>csv(h[1])).join(";")+"\r\n"+rows.map(r=>headers.map(h=>csv(r[h[0]])).join(";")).join("\r\n")}
function renderFleet(){
 const node=$("btp-v4-fleet-table");if(!node)return;
 const rows=get(FLEET),sorted=rows.slice().sort((a,b)=>String(a.name).localeCompare(String(b.name),"fr"));
 const tr=sorted.map(r=>'<tr><td>'+esc(r.name)+'</td><td>'+esc(r.type)+'</td><td>'+esc(r.site||"—")+'</td><td><select data-fleet-status="'+esc(r.name)+'" style="background:#0f2629;border:1px solid #4b6d69;color:#fff;border-radius:6px;padding:4px">'+
 ["Disponible","Affecté","En maintenance","Hors service"].map(s=>'<option '+(r.status===s?"selected":"")+'>'+s+'</option>').join("")+'</select></td><td>'+esc(r.nextControl||"Non renseigné")+'</td><td><button type="button" class="btn btn-secondary" data-fleet-remove="'+esc(r.name)+'">Retirer de la liste</button></td></tr>').join("");
 node.innerHTML=tr||'<tr><td colspan="6" style="text-align:center;color:#adc3bd;padding:14px">Aucun matériel saisi. Les véhicules des anciennes cartes restent des exemples indépendants.</td></tr>';
 const total=$("btp-v4-fleet-count");if(total)total.textContent=rows.length+" équipement(s) consignés localement";
}
function renderStock(){
 const node=$("btp-v4-stock-table");if(!node)return;
 const rows=get(STOCK),groups=new Map();
 rows.forEach(r=>{const key=r.ref+"|"+r.zone+"|"+r.unit;
  if(!groups.has(key))groups.set(key,{ref:r.ref,desc:r.desc,zone:r.zone,unit:r.unit,quantity:0});
  groups.get(key).quantity+=r.direction==="Entrée"?r.quantity:-r.quantity;
 });
 node.innerHTML=Array.from(groups.values()).map(r=>'<tr><td>'+esc(r.ref)+'</td><td>'+esc(r.desc)+'</td><td>'+esc(r.zone)+'</td><td style="font-weight:800;color:'+(r.quantity<0?"#e9a79f":"#bce985")+'">'+fr(r.quantity)+" "+esc(r.unit)+'</td></tr>').join("")||'<tr><td colspan="4" style="text-align:center;color:#b1c5be;padding:13px">Aucun stock renseigné. Les stocks du plan 3D historique sont fictifs.</td></tr>';
 const count=$("btp-v4-stock-count");if(count)count.textContent=rows.length+" mouvement(s) locaux";
}
function setupPanel(tab,title,id,body){
 if(!tab||$(id))return;
 const panel=document.createElement("section");panel.id=id;panel.style.cssText="background:#13292e;border:1px solid #64837d77;border-radius:13px;padding:15px;margin:0 0 17px;color:#dcefe4";
 panel.innerHTML='<div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:center"><div><div style="font-size:10px;font-weight:850;color:#bce985;letter-spacing:.13em">REGISTRE LOCAL V4</div><h3 style="font-size:17px;margin:3px 0">'+title+'</h3><p style="font-size:11px;color:#abc4b7;margin:0">Saisies manuelles, sans télémétrie ni preuve de conformité automatique.</p></div></div>'+body;
 tab.insertBefore(panel,tab.firstChild);
}
function init(){
 setupPanel($("tab-fleet"),"Parc matériel et disponibilité", "btp-v4-fleet",
 '<form id="btp-v4-fleet-form" style="display:flex;flex-wrap:wrap;gap:7px;margin:12px 0">'+
 '<input required id="f4-name" maxlength="80" placeholder="Réf/immatriculation" aria-label="Référence matériel">'+
 '<input id="f4-type" maxlength="120" placeholder="Catégorie / engin" aria-label="Type engin">'+
 '<input id="f4-site" maxlength="120" placeholder="Affectation / dépôt" aria-label="Affectation">'+
 '<select id="f4-status" aria-label="Statut"><option>Disponible</option><option>Affecté</option><option>En maintenance</option><option>Hors service</option></select>'+
 '<label style="font-size:11px">Prochain contrôle <input id="f4-next" type="date" aria-label="Prochain contrôle"></label>'+
 '<button type="submit" class="btn btn-primary">Ajouter / actualiser</button><button type="button" class="btn btn-secondary" id="f4-export">CSV</button></form>'+
 '<p id="f4-error" style="font-size:11px;color:#f0c5a2" aria-live="polite"></p>'+
 '<div style="overflow:auto"><table style="width:100%;font-size:11px"><thead><tr><th>Référence</th><th>Type</th><th>Affectation</th><th>Statut</th><th>Prochain contrôle</th><th>Action</th></tr></thead><tbody id="btp-v4-fleet-table"></tbody></table></div><small id="btp-v4-fleet-count" style="color:#b2d0bd"></small>');
 setupPanel($("tab-depot"),"Entrées, sorties et stock disponible","btp-v4-stock",
 '<form id="btp-v4-stock-form" style="display:flex;flex-wrap:wrap;gap:7px;margin:12px 0">'+
 '<input id="s4-ref" required maxlength="80" placeholder="Référence article" aria-label="Référence article">'+
 '<input id="s4-desc" maxlength="120" placeholder="Désignation" aria-label="Désignation">'+
 '<input id="s4-zone" maxlength="120" placeholder="Zone : racks, casiers..." aria-label="Zone dépôt">'+
 '<select id="s4-dir" aria-label="Type mouvement"><option>Entrée</option><option>Sortie</option></select>'+
 '<input id="s4-qty" required type="number" step="any" min="0.001" placeholder="Quantité" aria-label="Quantité">'+
 '<select id="s4-unit" aria-label="Unité"><option>u</option><option>t</option><option>m³</option><option>ml</option><option>kg</option></select>'+
 '<button type="submit" class="btn btn-primary">Enregistrer mouvement</button><button type="button" class="btn btn-secondary" id="s4-export">CSV</button></form>'+
 '<p id="s4-error" style="font-size:11px;color:#f0c5a2" aria-live="polite"></p>'+
 '<div style="overflow:auto"><table style="width:100%;font-size:11px"><thead><tr><th>Référence</th><th>Désignation</th><th>Emplacement</th><th>Solde local</th></tr></thead><tbody id="btp-v4-stock-table"></tbody></table></div><small id="btp-v4-stock-count" style="color:#b2d0bd"></small>');
 const fleetForm=$("btp-v4-fleet-form");
 fleetForm?.addEventListener("submit",e=>{e.preventDefault();
  try{const name=ensureId($("f4-name").value),type=$("f4-type").value.trim().slice(0,120),status=$("f4-status").value,site=$("f4-site").value.trim().slice(0,120),nextControl=$("f4-next").value;
   if(!type)throw Error("Type de matériel obligatoire");
   const list=get(FLEET),index=list.findIndex(x=>x.name===name);
   const record={name,type,site,status,nextControl,updatedAt:stamp(),source:"saisie locale"};
   if(index>=0)list[index]=record;else list.push(record);
   save(FLEET,list);fleetForm.reset();$("f4-error").textContent="Matériel enregistré localement (saisie à vérifier).";renderFleet();
  }catch(err){$("f4-error").textContent=err.message}
 });
 const stockForm=$("btp-v4-stock-form");
 stockForm?.addEventListener("submit",e=>{e.preventDefault();
  try{
   const ref=ensureId($("s4-ref").value),desc=$("s4-desc").value.trim().slice(0,120),zone=$("s4-zone").value.trim().slice(0,120),
    direction=$("s4-dir").value,quantity=positive($("s4-qty").value),unit=$("s4-unit").value;
   if(!zone||!desc)throw Error("Désignation et zone requises");
   const existing=get(STOCK),balance=existing.filter(r=>r.ref===ref&&r.zone===zone&&r.unit===unit).reduce((v,r)=>v+(r.direction==="Entrée"?r.quantity:-r.quantity),0);
   if(direction==="Sortie"&&quantity>balance)throw Error("Sortie supérieure au stock saisi dans cette zone (solde "+fr(balance)+" "+unit+").");
   existing.push({ref,desc,zone,direction,quantity,unit,date:today(),timestamp:stamp(),project:(localStorage.getItem("btp_project_active_v1")||"")});
   save(STOCK,existing);stockForm.reset();$("s4-error").textContent="Mouvement enregistré dans le journal local.";renderStock();
  }catch(err){$("s4-error").textContent=err.message}
 });
 $("btp-v4-fleet-table")?.addEventListener("change",e=>{const name=e.target.dataset.fleetStatus;if(!name)return;
  const list=get(FLEET),row=list.find(r=>r.name===name);if(!row)return;row.status=e.target.value;row.updatedAt=stamp();
  try{save(FLEET,list);renderFleet()}catch(err){$("f4-error").textContent=err.message}
 });
 $("btp-v4-fleet-table")?.addEventListener("click",e=>{const b=e.target.closest("[data-fleet-remove]");if(!b)return;
  const name=b.dataset.fleetRemove;if(!confirm("Retirer « "+name+" » du registre local ?"))return;
  try{save(FLEET,get(FLEET).filter(x=>x.name!==name));renderFleet()}catch(err){$("f4-error").textContent=err.message}
 });
 $("f4-export")?.addEventListener("click",()=>fdownload("btp-flotte-locale.csv",rowsToCSV([["name","Référence"],["type","Type"],["site","Affectation"],["status","Statut"],["nextControl","Contrôle prévu"],["updatedAt","Date mise à jour"]],get(FLEET))));
 $("s4-export")?.addEventListener("click",()=>fdownload("btp-stock-mouvements.csv",rowsToCSV([["ref","Référence"],["desc","Désignation"],["zone","Zone"],["direction","Mouvement"],["quantity","Quantité"],["unit","Unité"],["date","Date"],["project","Projet"]],get(STOCK))));
 renderFleet();renderStock();
 window.addEventListener("storage",e=>{if(e.key===FLEET)renderFleet();if(e.key===STOCK)renderStock()});
}
window.openDepotEntryV4=function(){if(!$("btp-v4-stock"))init();$("btp-v4-stock")?.scrollIntoView({behavior:"smooth",block:"center"});$("s4-ref")?.focus()};
window.openFleetEntryV4=function(){if(!$("btp-v4-fleet"))init();$("btp-v4-fleet")?.scrollIntoView({behavior:"smooth",block:"center"});$("f4-name")?.focus()};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
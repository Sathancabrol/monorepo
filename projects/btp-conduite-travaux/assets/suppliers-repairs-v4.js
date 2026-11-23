/* BTP Studio v4 — supplier directory with manual local data, not web-verified ratings. */
(function(){
"use strict";
const KEY="btp_suppliers_local_v4",el=id=>document.getElementById(id),fmt=n=>Number(n).toLocaleString("fr-FR",{maximumFractionDigits:0});
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function read(){try{const rows=JSON.parse(localStorage.getItem(KEY)||"[]");return Array.isArray(rows)?rows:[]}catch(e){return []}}
function write(rows){if(rows.length>1000)throw Error("Maximum 1000 fournisseurs");localStorage.setItem(KEY,JSON.stringify(rows))}
function csv(v){let s=String(v??"");if(/^[=+\-@\t\r]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"'}
function downloadCSV(){
 const cols=[["name","Société"],["type","Spécialité"],["city","Ville"],["contact","Contact"],["delay","Délai indicatif en jours"],["notes","Notes"],["updatedAt","Modifié UTC"]];
 const out=[cols.map(x=>csv(x[1])).join(";"),...read().map(r=>cols.map(x=>csv(r[x[0]])).join(";"))].join("\r\n");
 const u=URL.createObjectURL(new Blob(["\uFEFF"+out],{type:"text/csv;charset=utf-8"})),a=document.createElement("a");a.href=u;a.download="btp-fournisseurs-locaux.csv";a.click();setTimeout(()=>URL.revokeObjectURL(u),3000)
}
function show(){
 const body=el("s4-supplier-body");if(!body)return;
 const q=(el("s4-supplier-filter")?.value||"").toLowerCase();
 const rows=read().filter(r=>(r.name+" "+r.type+" "+r.city).toLowerCase().includes(q));
 body.innerHTML=rows.map(r=>'<tr><td>'+esc(r.name)+'</td><td>'+esc(r.type)+'</td><td>'+esc(r.city)+'</td><td>'+esc(r.contact)+'</td><td>'+fmt(r.delay||0)+' j</td>'+
 '<td><button class="btn btn-secondary" type="button" data-supplier-edit="'+esc(r.name)+'">Modifier</button><button class="btn btn-secondary" type="button" data-supplier-remove="'+esc(r.name)+'">Retirer</button></td></tr>').join("")||
 '<tr><td colspan="6" style="text-align:center;padding:15px">Aucun fournisseur saisi localement. Les partenaires historiques sont uniquement des exemples.</td></tr>';
 const count=el("s4-supplier-status");if(count)count.textContent=rows.length+" fiche(s) locale(s) affichée(s)";
}
function clear(){el("s4-supplier-form")?.reset();el("s4-supplier-id").value="";}
function init(){
 const tab=el("tab-procurement");if(!tab||el("btp-v4-suppliers"))return;
 const section=document.createElement("section");section.id="btp-v4-suppliers";section.style.cssText="padding:15px;border:1px solid #65888388;background:#142a2f;border-radius:12px;margin:0 0 15px;color:#e2f4e7";
 section.innerHTML='<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:9px"><div><div style="font-size:10px;font-weight:900;color:#bce985;letter-spacing:.12em">FOURNISSEURS · SAISIES LOCALES</div><h3 style="margin:5px 0;font-size:18px">Créer et suivre un vrai annuaire</h3><p style="font-size:11px;color:#bed4c7">Les fiches ci-dessous sont les tiennes. Les notes, distances et prix de l’ancien catalogue ne sont pas des offres confirmées.</p></div><button type="button" id="s4-supplier-export" class="btn btn-secondary">Exporter CSV</button></div>'+
 '<form id="s4-supplier-form" style="display:flex;flex-wrap:wrap;gap:7px;margin:12px 0">'+
 '<input id="s4-supplier-id" type="hidden"><input id="s4-supplier-name" required maxlength="140" placeholder="Entreprise / fournisseur" aria-label="Nom fournisseur">'+
 '<input id="s4-supplier-type" required maxlength="120" placeholder="Métier / spécialité" aria-label="Spécialité">'+
 '<input id="s4-supplier-city" maxlength="120" placeholder="Ville" aria-label="Ville">'+
 '<input id="s4-supplier-contact" maxlength="180" placeholder="Contact (optionnel)" aria-label="Contact">'+
 '<label style="font-size:11px">Délai indicatif (j) <input id="s4-supplier-delay" type="number" min="0" max="3650" value="0"></label>'+
 '<input id="s4-supplier-notes" maxlength="500" placeholder="Conditions / remarques" aria-label="Remarques">'+
 '<button type="submit" class="btn btn-primary">Enregistrer</button><button type="button" id="s4-supplier-clear" class="btn btn-secondary">Vider</button></form>'+
 '<label style="font-size:11px;color:#c6dacc">Recherche <input id="s4-supplier-filter" type="search" placeholder="Nom, type ou ville" style="margin-left:8px"></label>'+
 '<div style="overflow:auto;margin-top:11px"><table style="font-size:11px;width:100%"><thead><tr><th>Société</th><th>Spécialité</th><th>Ville</th><th>Contact</th><th>Délai saisi</th><th>Actions</th></tr></thead><tbody id="s4-supplier-body"></tbody></table></div>'+
 '<p id="s4-supplier-status" role="status" style="font-size:11px;color:#bce985"></p>';
 tab.insertBefore(section,tab.firstChild);
 el("s4-supplier-form").addEventListener("submit",e=>{
  e.preventDefault();try{
   const oldName=el("s4-supplier-id").value,name=el("s4-supplier-name").value.trim(),type=el("s4-supplier-type").value.trim(),delay=Number(el("s4-supplier-delay").value);
   if(!name||!type||!Number.isFinite(delay)||delay<0||delay>3650)throw Error("Nom, spécialité et délai valide requis");
   const list=read(),record={name:name.slice(0,140),type:type.slice(0,120),city:el("s4-supplier-city").value.trim().slice(0,120),
    contact:el("s4-supplier-contact").value.trim().slice(0,180),notes:el("s4-supplier-notes").value.trim().slice(0,500),delay,updatedAt:new Date().toISOString()};
   if(oldName){const i=list.findIndex(v=>v.name===oldName);if(i<0)throw Error("Fiche d'origine introuvable");list.splice(i,1)}
   const existing=list.findIndex(v=>v.name===record.name);if(existing>=0)list[existing]=record;else list.push(record);
   write(list);clear();show();
  }catch(err){el("s4-supplier-status").textContent="Non enregistré : "+err.message}
 });
 el("s4-supplier-body").addEventListener("click",e=>{
  const edit=e.target.closest("[data-supplier-edit]"),del=e.target.closest("[data-supplier-remove]");
  if(edit){const r=read().find(v=>v.name===edit.dataset.supplierEdit);if(!r)return;
   for(const [i,val] of [["name",r.name],["type",r.type],["city",r.city],["contact",r.contact],["delay",r.delay],["notes",r.notes]])el("s4-supplier-"+i).value=val;
   el("s4-supplier-id").value=r.name;el("s4-supplier-name").focus();}
  if(del&&confirm("Supprimer cette fiche de fournisseur du navigateur ?")){try{write(read().filter(v=>v.name!==del.dataset.supplierRemove));show()}catch(err){el("s4-supplier-status").textContent=err.message}}
 });
 el("s4-supplier-clear").onclick=clear;el("s4-supplier-export").onclick=downloadCSV;
 el("s4-supplier-filter").addEventListener("input",show);
 window.addEventListener("storage",e=>{if(e.key===KEY)show()});show();
}
window.openSupplierEntryV4=function(){if(!el("btp-v4-suppliers"))init();el("btp-v4-suppliers")?.scrollIntoView({behavior:"smooth",block:"start"});el("s4-supplier-name")?.focus()};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
"use strict";
const test=require("node:test"),assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const src=f=>fs.readFileSync(path.join(root,f),"utf8");
// The calculation file contains a browser adapter after the pure UMD export.
// Supply a minimal window before loading it; no browser event/DOM is executed.
const oldWindow=global.window;
global.window={};
const calc=require("../assets/calculs-repairs-v4.js");
global.window=oldWindow;

test("Hydraulique : DN300 K100 pente1.5% à pleine section",()=>{
 const r=calc.hydraulic(300,100,1.5,100);
 assert.ok(Math.abs(r.qLs-153.9638855)<0.0001);
 assert.equal(r.qLs,r.qFullLs);
 assert.ok(r.vMps>0);
});
test("Hydraulique : 50% de remplissage fournit 50% du débit pleine section",()=>{
 const full=calc.hydraulic(300,100,1.5,100),half=calc.hydraulic(300,100,1.5,50);
 assert.ok(Math.abs(half.qLs/full.qLs-.5)<1e-8);
});
test("Hydraulique : le diamètre et la pente agissent sur le débit",()=>{
 assert.ok(calc.hydraulic(400,100,1.5,50).qLs>calc.hydraulic(300,100,1.5,50).qLs);
 assert.ok(calc.hydraulic(300,100,2,50).qLs>calc.hydraulic(300,100,1,50).qLs);
});
test("Ruissellement brut : 2.5ha, C=.5, pluie45mm =562.5 m3",()=>{
 const r=calc.basin(2.5,.5,45,2);
 assert.equal(r.grossRunoffM3,562.5);assert.equal(r.allowedLs,5);
});
test("Chute de tension simplifiée : mono 230V 1800W cuivre 250m S6",()=>{
 const r=calc.electric(1800,250,6,"cuivre","mono");
 assert.ok(Math.abs(r.currentA-7.8260869565)<.001);
 assert.ok(Math.abs(r.dropV-14.6739130434)<.001);
 assert.ok(Math.abs(r.dropPct-6.3799621928)<.001);
});
test("L'augmentation de la section réduit la chute de tension",()=>{
 assert.ok(calc.electric(1800,250,10,"cuivre","mono").dropPct<calc.electric(1800,250,6,"cuivre","mono").dropPct);
});
test("Refus des entrées hors domaine",()=>{
 assert.throws(()=>calc.hydraulic(0,100,1,50),/Diamètre/);
 assert.throws(()=>calc.basin(2,1.5,45,2),/Coefficient/);
 assert.throws(()=>calc.electric(1800,250,0,"cuivre","mono"),/Section/);
});
test("Tous les correctifs V4 existent et sont syntaxiquement valides",()=>{
 const names=["calculs-repairs-v4","registres-repairs-v4","bruckner-repairs-v4","interactions-repairs-v4","navigation-repairs-v4","operations-repairs-v4","archives-repairs-v4"];
 for(const name of names)assert.doesNotThrow(()=>new vm.Script(src("assets/"+name+".js"),{filename:name}));
});
test("L'index conserve 23 modules et référence exactement 7 correctifs V4",()=>{
 const html=src("index.html"),views=[...html.matchAll(/\bid="tab-([a-z0-9_]+)"/g)].map(x=>x[1]);
 assert.equal(views.length,23);assert.equal(new Set(views).size,23);
 const files=["calculs-repairs-v4","registres-repairs-v4","bruckner-repairs-v4","interactions-repairs-v4","navigation-repairs-v4","operations-repairs-v4","archives-repairs-v4"];
 for(const name of files)assert.equal(html.split('src="assets/'+name+'.js"').length-1,1,name);
});
test("Boutons d'ajout engin, stock, chantier et archivage ne sont plus des alertes fictives",()=>{
 const html=src("index.html");
 for(const call of ["openDepotEntryV4()","openFleetEntryV4()","openArchiveUploaderV4()","window.location.href='chantier-studio.html'"])assert.ok(html.includes(call),call);
 assert.doesNotMatch(html,/alert\('Fiche engin TP ouverte|alert\('Formulaire de création de nouveau marché public ouvert/);
});
test("La nav corrige les sous-vues supplémentaires plutôt que les masquer",()=>{
 const source=src("assets/navigation-repairs-v4.js");
 for(const id of ["tech-hydraulique-view","tech-gtr-view","tech-bruckner-view","tech-reseauxsecs-view","planning-intemperies-view"])assert.ok(source.includes(id),id);
});

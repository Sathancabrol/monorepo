"use strict";
const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const read=p=>fs.readFileSync(path.join(root,p),"utf8");
const main=read("index.html"),work=read("chantier-studio.html"),js=read("assets/project-workspace.js");
const views=["cockpit","company","depot","projects_hub","planning","simulator","fleet","catalog","hr","opbtp","safety","rdc","compagnon_mobile","obsidian","schemas","sdp","benchmark","procurement","ledger","docs","archives","atelier_3d","fiches_taches"];

test("23 routes historiques et enrichies subsistent sans doublon",()=>{
 const ids=[...main.matchAll(/\bid="tab-([a-z0-9_]+)"/g)].map(m=>m[1]);
 assert.equal(ids.length,23);assert.deepEqual(new Set(ids),new Set(views));
});

test("le gestionnaire projet est intégré au hub",()=>{
 assert.match(main,/id="tab-projects_hub"/);
 assert.match(main,/src="chantier-studio.html"/);
 assert.match(main,/données locales|données fictives/i);
});

test("tous les composants statiques du gestionnaire sont locaux",()=>{
 const refs=[...work.matchAll(/<(?:script|link)[^>]*(?:src|href)="([^"]+)"/g)].map(m=>m[1]);
 assert.ok(refs.includes("assets/project-core-v1.js"));
 assert.ok(refs.includes("assets/project-workspace.js"));
 for(const ref of refs)assert.ok(fs.existsSync(path.join(root,ref)),ref+" manquant");
 assert.ok(!refs.some(v=>/^https?:\/\//.test(v)));
});

test("chaque identifiant de formulaire utilisé existe dans la page",()=>{
 const refs=[...js.matchAll(/\bel\("([^"]+)"\)/g)].map(m=>m[1]);
 const ids=new Set([...work.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
 const missing=[...new Set(refs)].filter(id=>!ids.has(id));
 assert.deepEqual(missing,[]);
});

test("les identifiants HTML dans le nouvel écran sont uniques",()=>{
 const ids=[...work.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(ids.length,new Set(ids).size);
});

test("tous les scripts V3 et les nouveaux scripts sont syntaxiquement valides",()=>{
 const scripts=["assets/workbench-v3.js","assets/workflow-v3.js","assets/project-context.js","assets/project-workspace.js","assets/project-core-v1.js","assets/diagnostics-v3.js"];
 for(const file of scripts)assert.doesNotThrow(()=>new vm.Script(read(file),{filename:file}));
});

test("l'interface d'origine reste syntaxiquement valide",()=>{
 const inline=[...main.matchAll(/<script>([\s\S]*?)<\/script>/g)];
 assert.ok(inline.length>=1);
 for(const piece of inline)assert.doesNotThrow(()=>new vm.Script(piece[1]));
});

test("la navigation vers le chantier n'utilise pas de service payant",()=>{
 assert.doesNotMatch(work,/https?:\/\/(?:api\.|openrouter|openai|stripe|paypal)/i);
 assert.doesNotMatch(js,/\bfetch\s*\(/);
});

test("les composants V3 sont chargés une seule fois",()=>{
 for(const ref of ["assets/workbench-v3.js","assets/workflow-v3.js","assets/project-context.js"]){
  assert.equal(main.split('src="'+ref+'"').length-1,1);
 }
});

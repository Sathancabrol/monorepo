/* Run: node tests/legacy-registers-v1.test.cjs — no npm dependencies. */
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),assert=require("node:assert/strict");
const source=fs.readFileSync(path.join(__dirname,"../assets/legacy-registers-v1.js"),"utf8");
const nodes=new Map(),values={"new-bl-num":"BL-01","new-bl-date":"2026-11-23T08:30","new-bl-qte":"28.4","new-bl-fournisseur":"Centrale exemple","new-bl-materiau":"BBSG 0/10","new-intemp-date":"2026-11-23","new-intemp-type":"Pluie"};
const node=id=>{if(!nodes.has(id))nodes.set(id,{value:values[id]||"",textContent:"",children:[],style:{},classList:{add(){},remove(){}},replaceChildren(){this.children=[]},appendChild(c){this.children.push(c)},click(){},remove(){}});return nodes.get(id)};
const memory={},alerts=[],blobs=[];
const document={readyState:"complete",getElementById:node,createElement:()=>node("generated-"+Math.random()),body:{appendChild(){}}};
const window={document,localStorage:{getItem:k=>memory[k],setItem:(k,v)=>memory[k]=v},alert:x=>alerts.push(x),openModal(){},closeModal(){},URL:{createObjectURL:b=>{blobs.push(b);return "blob:test"},revokeObjectURL(){}}};
class BlobMock{constructor(parts,options){this.parts=parts;this.options=options}}
vm.runInNewContext(source,{window,Blob:BlobMock});
const preventDefault=()=>{};
window.saveNewLivraison({preventDefault});
assert.equal(window.BTPRegisterRepair.read().deliveries.length,1);
assert.equal(node("kpi-livraison-enrobes").textContent,"28.40 t");
window.saveNewLivraison({preventDefault});assert.equal(alerts.length,1);
node("new-bl-num").value="BL-02";node("new-bl-qte").value="-5";
window.saveNewLivraison({preventDefault});assert.equal(window.BTPRegisterRepair.read().deliveries.length,1);
window.saveNewIntemperie({preventDefault});assert.equal(window.BTPRegisterRepair.read().weather.length,1);
assert.match(node("kpi-intemperies-depassement").textContent,/CCAP/);
window.exportLivraisonsCSV();window.exportIntemperiesCSV();
assert.equal(blobs.length,2);
assert.match(blobs[0].parts.join(""),/BL-01/);
assert.match(blobs[1].parts.join(""),/Non validé/);
console.log("9 assertions: OK — DOM mock, not browser E2E.");

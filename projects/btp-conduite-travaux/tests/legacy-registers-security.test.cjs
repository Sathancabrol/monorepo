/* Regression tests for date and CSV defenses in legacy-registers-v1.js.
 * Run: node tests/legacy-registers-security.test.cjs
 * The module is evaluated with a fake DOM; no browser or npm dependency. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");
const source=fs.readFileSync(path.join(__dirname,"../assets/legacy-registers-v1.js"),"utf8");
const dates=[["2026-02-28",true],["2026-02-30",false],["2024-02-29",true],["2026-13-01",false],["2026-11-23T19:45",true],["2026-11-23T25:45",false],["2026-11-23x",false]];
const storage=new Map(),fields=new Map(),downloads=[];
const doc={readyState:"loading",addEventListener(){},getElementById(id){return fields.get(id)||null},createElement(tag){if(tag==="a")return {click(){downloads.push(this)},remove(){}};return {textContent:"",style:{},appendChild(){}}},body:{appendChild(){}}};
const root={document:doc,localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},URL:{createObjectURL(blob){root.lastBlob=blob;return "blob:test"},revokeObjectURL(){}},alert(){}};
vm.runInNewContext(source,{window:root,Blob,console});
function field(id,value){fields.set(id,{value})}
field("new-bl-num","BL-1");field("new-bl-date","2026-02-30T12:30");field("new-bl-qte","20");
root.saveNewLivraison({preventDefault(){}});assert.equal(root.BTPRegisterRepair.read().deliveries.length,0);
field("new-bl-date","2026-11-23T12:30");field("new-bl-qte","");
root.saveNewLivraison({preventDefault(){}});assert.equal(root.BTPRegisterRepair.read().deliveries.length,0);
field("new-bl-qte","20");field("new-bl-num",'=HYPERLINK("https://bad")');
root.saveNewLivraison({preventDefault(){}});assert.equal(root.BTPRegisterRepair.read().deliveries.length,1);
root.exportLivraisonsCSV();assert.equal(downloads.length,1);
(async()=>{const csv=await root.lastBlob.text();assert.match(csv,/"'=HYPERLINK\(""https:\/\/bad""\)"/);console.log("PASS: invalid date, blank quantity, valid delivery, CSV formula neutralized");})().catch(e=>{console.error(e);process.exitCode=1});

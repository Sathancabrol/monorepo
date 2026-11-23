/* Run: node tests/diagnostics-module-attribution.test.cjs
   Tests only the structural audit, never claims business/UI certification. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/diagnostics-v3.js'), 'utf8');
const scripts = source.replace('function display(){', 'window.__runBtpAudit = run;\nfunction display(){');
assert.notEqual(scripts, source, 'Test injection marker must exist');
const moduleIds = ['cockpit', 'planning'];
function node(id, handler, moduleId) {
  return {id, tagName:'BUTTON', getAttribute(k){return k==='onclick'?handler:null;},
    closest(){return moduleId?{id:'tab-'+moduleId}:null;}};
}
const buttons = [
 node('planning-good', 'window.knownHandler()', 'planning'),
 node('planning-bad', 'window.missingHandler()', 'planning'),
 node('cockpit-bad', 'window.otherMissing()', 'cockpit'),
 node('global-bad', 'window.globalMissing()', null)
];
const panels = Object.fromEntries(moduleIds.map(id=>['tab-'+id,{
  querySelector(sel){return sel==='.btp-wb-hub'?{}:null;},
  querySelectorAll(sel){return sel==='button,input,select,textarea,canvas,iframe'?buttons.filter(x=>x.closest()?.id==='tab-'+id):[];}
}]));
const document = {
 readyState:'loading',
 querySelectorAll(sel){return sel==='*'?buttons:sel==='[id]'?buttons:[];},
 getElementById(id){return panels[id]||null;},
 addEventListener(){}
};
const window = {addEventListener(){}, knownHandler(){}};
vm.runInNewContext(scripts, {window,document,Date,JSON,Set,Array,Object,String,Blob:class{},URL:{}}, {timeout:1000});
const audit=window.__runBtpAudit();
assert.equal(audit.total,23);
assert.equal(audit.unresolved_inline_handlers.length,3);
assert.equal(audit.modules.find(m=>m.id==='planning').unresolved_handler_count,1);
assert.equal(audit.modules.find(m=>m.id==='cockpit').unresolved_handler_count,1);
assert.equal(audit.unresolved_inline_handlers.filter(x=>x.module_id===null).length,1);
assert.equal(audit.modules.find(m=>m.id==='planning').functional_validation,'not_proven');
assert.equal(audit.modules.find(m=>m.id==='planning').structural_status,'wired');
console.log('PASS: 7 structural diagnostic assertions');

'use strict';
// Géométrie pure : longueurs en m, surfaces en m², volumes en m³.
function positive(value,label,allowZero=false){if(typeof value!=='number'||!Number.isFinite(value)||(allowZero?value<0:value<=0))throw new RangeError(label+': valeur invalide');return value;}
function earthwork({area,depth}){return positive(area,'Surface')*positive(depth,'Profondeur');}
function trench({bottomWidth,depth,slope=0,length}){positive(bottomWidth,'Largeur');positive(depth,'Profondeur');positive(slope,'Talus',true);positive(length,'Longueur');const topWidth=bottomWidth+2*slope*depth,section=(bottomWidth+topWidth)*depth/2;return {topWidth,section,volume:section*length};}
function pavement({area,layers}){positive(area,'Surface');if(!Array.isArray(layers)||!layers.length)throw new RangeError('Couches requises');return layers.map((layer,i)=>({name:String(layer.name||'Couche '+(i+1)),volume:area*positive(layer.thickness,'Épaisseur')}));}
function duration({quantity,rate,setupDays=0,weatherDays=0}){positive(quantity,'Quantité');positive(rate,'Rendement');positive(setupDays,'Installation',true);positive(weatherDays,'Aléas',true);return {productionDays:quantity/rate,totalDays:quantity/rate+setupDays+weatherDays};}
module.exports={earthwork,trench,pavement,duration};

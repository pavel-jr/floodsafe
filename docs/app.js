'use strict';
const byId = id => document.getElementById(id);
const weights = {flood_exposure:.35,sewage_exposure:.30,water_vulnerability:.20,pipe_vulnerability:.15};
const labels = {flood_exposure:'Flood exposure',sewage_exposure:'Sewage exposure',water_vulnerability:'Water-source vulnerability',pipe_vulnerability:'Pipe vulnerability'};
const colors = {High:'#dc2626',Elevated:'#d58b08',Lower:'#16803c'};
let data, map, markers, ranked=[], selected='Nahariya';
function predictSeverity(model, row, month, type) {
  const x=[row.latitude,row.longitude,month].map((v,i)=>(v-model.mean[i])/model.scale[i]);
  ['Israel',type].forEach((value,i)=>model.categories[i].forEach(category=>x.push(Number(category===value))));
  const logits=model.coefficients.map((coef,i)=>coef.reduce((s,w,j)=>s+w*x[j],model.intercept[i]));
  return model.classes[logits.indexOf(Math.max(...logits))];
}
function scoreRows(rows, multiplier) {
 return rows.map(row=>{
  const r={...row,flood_exposure:Math.min(100,row.flood_exposure*multiplier)};
  const entries=Object.entries(weights).map(([key,w])=>[key,r[key]*w]);
  r.priority_score=entries.reduce((s,e)=>s+e[1],0)*r.flood_exposure/100;
  // Python rounds the final score to one decimal place.
  r.priority_score=Math.round(r.priority_score*10)/10;
  r.tier=r.priority_score>60?'High':r.priority_score>30?'Elevated':'Lower';
  r.main_driver=entries.reduce((best,e)=>e[1]>best[1]?e:best)[0];return r;
 }).sort((a,b)=>b.priority_score-a.priority_score);
}
function inspect(){
 const row=ranked.find(r=>r.location===selected);
 byId('location').value=selected;
 byId('name').textContent=selected;
 byId('score').textContent=row.priority_score.toFixed(1)+' / 100';
 byId('score').style.color=colors[row.tier];
 byId('tier').textContent=row.tier+' sampling priority';
 byId('factors').replaceChildren();
 Object.keys(weights).forEach(key=>{
  const el=document.createElement('div');el.className='factor';
  el.textContent=labels[key]+': '+row[key].toFixed(0);
  const track=document.createElement('div'),bar=document.createElement('span');
  bar.style.width=row[key]+'%';track.append(bar);el.append(track);byId('factors').append(el);
 });
 byId('action').textContent=row.tier==='High'?'Suggested demo action: prioritise sampling and inspect exposed infrastructure.':'Suggested demo action: consider this location in the sampling plan.';
 const prediction=predictSeverity(data.model,row,Number(byId('month').value),byId('type').value);
 byId('prediction').textContent=selected+': '+prediction+' flood severity (historical classifier output).';
}
function render(){
 const multiplier=Number(byId('rain').value);
 byId('rainValue').textContent=multiplier.toFixed(2)+'×';ranked=scoreRows(data.locations,multiplier);
 byId('high').textContent=ranked.filter(r=>r.tier==='High').length;
 byId('queue').replaceChildren();
 ranked.forEach(row=>{
  const tr=document.createElement('tr');
  [row.location,row.priority_score.toFixed(1),row.tier,labels[row.main_driver]].forEach(value=>{const td=document.createElement('td');td.textContent=value;tr.append(td);});
  tr.onclick=()=>{selected=row.location;inspect();};byId('queue').append(tr);
 });
 if(markers){markers.clearLayers();ranked.forEach(row=>{
  const marker=L.circleMarker([row.latitude,row.longitude],{radius:8+row.priority_score/12,color:colors[row.tier],fillOpacity:.65}).addTo(markers);
  marker.bindTooltip(row.location+' · '+row.priority_score+' · '+row.tier);
  marker.on('click',()=>{selected=row.location;inspect();});
 });}
 inspect();
}
async function start(){
 data=await(await fetch('data.json')).json();
 for(let m=1;m<=12;m++){const o=new Option(new Date(2026,m-1,1).toLocaleString('en',{month:'long'}),m);byId('month').add(o);}byId('month').value=10;
 data.locations.forEach(row=>byId('location').add(new Option(row.location,row.location)));
 byId('location').onchange=()=>{selected=byId('location').value;inspect();};
 byId('rain').oninput=render;byId('month').onchange=inspect;byId('type').onchange=inspect;
 byId('events').textContent=data.report.unique_flood_events;
 const r=data.report;
 byId('metrics').textContent=`Chronological test: ${r.train_events} training / ${r.test_events} test events. Accuracy ${(r.model.accuracy*100).toFixed(1)}% vs ${(r.majority_baseline.accuracy*100).toFixed(1)}% majority baseline. Weak performance; unsuitable for operational predictions.`;
 if(typeof L!=='undefined'){
  map=L.map('map').setView([31.6,35.05],7);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',maxZoom:18}).addTo(map);markers=L.layerGroup().addTo(map);
 }else{byId('map').textContent='Map library unavailable. Use the location selector and sampling queue below.';}
 byId('download').onclick=()=>{
  const keys=['location','priority_score','tier',...Object.keys(weights)];
  const csv=[keys.join(','),...ranked.map(r=>keys.map(k=>r[k]).join(','))].join('\n');
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));const a=document.createElement('a');a.href=url;a.download='simulated_sampling_priorities.csv';a.click();URL.revokeObjectURL(url);
 };
 render();byId('status').textContent='Scenario ready · all contamination priorities are simulated';
}
if(typeof document!=='undefined')start().catch(error=>{byId('status').textContent='Could not load demo: '+error.message;byId('status').className='error';});
if(typeof module!=='undefined')module.exports={predictSeverity,scoreRows};

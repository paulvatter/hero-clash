import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hero Clash", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:#07071a;font-family:'Segoe UI',sans-serif;color:#fff;
     user-select:none;overflow:hidden;touch-action:none}
#wrap{display:flex;flex-direction:column;width:100vw;height:100vh}

/* ── HUD ── */
#hud{display:flex;align-items:center;gap:6px;padding:5px 10px;
     background:rgba(0,0,0,.75);border-bottom:1px solid rgba(255,255,255,.08);flex-shrink:0}
.hname{font-size:13px;font-weight:700;color:#FFD700;min-width:70px}
.hpbar{flex:1;height:8px;background:rgba(255,255,255,.12);border-radius:4px;overflow:hidden}
.hpfill{height:100%;border-radius:4px;transition:width .15s;background:#4CAF50}

/* ── Skill bar ── */
#skbar-wrap{display:flex;gap:4px;padding:3px 10px;background:rgba(0,0,0,.5);
            border-bottom:1px solid rgba(255,255,255,.06);flex-shrink:0;flex-wrap:wrap;align-items:center}
.skbtn{padding:2px 7px;border-radius:5px;border:1.5px solid rgba(255,255,255,.18);
       background:rgba(255,255,255,.05);color:#eee;font-size:9px;font-weight:700;
       cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:1px}
.skbtn.ready{border-color:#FFD700;color:#FFD700}
.skbtn.off{opacity:.38}

/* ── Canvas area ── */
#cvwrap{position:relative;flex:1;overflow:hidden}
canvas{display:block;width:100%;height:100%;touch-action:none}

/* ── Focus banner ── */
#focusbanner{position:absolute;inset:0;background:rgba(0,0,0,.55);
             display:flex;align-items:center;justify-content:center;
             cursor:pointer;z-index:20}
#focusbanner span{background:#FFD700;color:#1a1000;font-size:14px;font-weight:900;
                  padding:10px 24px;border-radius:9px;pointer-events:none;text-align:center}

/* ── In-game message ── */
#msg{position:absolute;top:36%;left:50%;transform:translate(-50%,-50%);
     font-size:28px;font-weight:900;color:#FFD700;text-shadow:2px 2px 0 #c60;
     pointer-events:none;text-align:center;transition:opacity .3s;
     white-space:nowrap;z-index:10}

/* ── Hero selection screen ── */
#sel{position:absolute;inset:0;background:rgba(5,5,20,.97);
     display:flex;flex-direction:column;align-items:center;
     padding:12px;overflow-y:auto;z-index:30}
#sel h2{font-size:22px;font-weight:900;color:#FFD700;letter-spacing:2px;margin-bottom:4px}
#sel .hint{font-size:9px;color:#888;margin-bottom:8px;text-align:center}
#hgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;
       width:100%;max-width:700px;margin-bottom:7px}
.hcard{background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.1);
       border-radius:7px;padding:6px 3px;text-align:center;cursor:pointer;
       transition:transform .1s,border-color .1s}
.hcard:hover,.hcard:active{transform:scale(1.04);border-color:rgba(255,255,255,.3)}
.hcard.sel{border-color:#FFD700;background:rgba(255,215,0,.1)}
.hcard .ci{font-size:20px}
.hcard .cn{font-size:8px;font-weight:700;margin-top:2px}
.hcard .cr{font-size:7px;color:#aaa}
#ptxt{font-size:9px;color:#ccc;text-align:center;min-height:18px;
      margin-bottom:7px;max-width:600px;padding:0 8px}
#gobtn{font-size:13px;font-weight:900;padding:8px 24px;background:#FFD700;
       color:#1a1000;border:none;border-radius:8px;cursor:pointer;opacity:.4;pointer-events:none}
#gobtn.active{opacity:1;pointer-events:auto}

/* ══════════════════════════════════════════
   MOBILE CONTROLS
   ══════════════════════════════════════════ */
#mobile-controls{
  position:absolute;inset:0;pointer-events:none;z-index:15;
  display:none; /* shown only on touch devices */
}

/* Joystick (bottom-left) */
#joystick-zone{
  position:absolute;left:16px;bottom:16px;
  width:120px;height:120px;
  pointer-events:all;
}
#joystick-base{
  position:absolute;inset:0;
  border-radius:50%;background:rgba(255,255,255,.12);
  border:2px solid rgba(255,255,255,.25);
}
#joystick-knob{
  position:absolute;
  width:48px;height:48px;
  border-radius:50%;
  background:rgba(255,255,255,.45);
  border:2px solid rgba(255,255,255,.7);
  top:50%;left:50%;
  transform:translate(-50%,-50%);
  transition:background .1s;
}

/* Right-side action buttons */
#action-buttons{
  position:absolute;right:14px;bottom:14px;
  display:grid;
  grid-template-columns:52px 52px;
  grid-template-rows:52px 52px 52px;
  gap:6px;
  pointer-events:all;
}
.act-btn{
  border-radius:50%;border:2px solid rgba(255,255,255,.3);
  background:rgba(0,0,0,.5);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:10px;font-weight:700;color:#eee;cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  transition:background .08s,border-color .08s;
  line-height:1.2;
}
.act-btn:active,.act-btn.pressed{background:rgba(255,255,255,.25);}
.act-btn .bi{font-size:18px;line-height:1}
/* Shoot button — larger, centre-right */
#btn-shoot{
  grid-column:1/3;grid-row:1/2;
  border-radius:28px;width:100%;height:100%;
  border-color:#ff5252;background:rgba(200,0,0,.35);
  font-size:12px;
}
#btn-shoot:active,#btn-shoot.pressed{background:rgba(200,0,0,.7);}
#star-display{font-size:18px;font-weight:700;color:#ffd700;display:flex;align-items:center;gap:6px;}
#star-count{font-size:24px;line-height:1;}
/* Skill buttons */
#btn-s1{grid-column:1;grid-row:2;border-color:#FFD700;color:#FFD700}
#btn-s2{grid-column:2;grid-row:2;border-color:#ab47bc;color:#e1bee7}
#btn-s3{grid-column:1;grid-row:3;border-color:#29b6f6;color:#b3e5fc}
#btn-s4{grid-column:2;grid-row:3;border-color:#66bb6a;color:#c8e6c9}
.act-btn.sk-off{opacity:.35}
</style>
</head>
<body>
<div id="wrap">
  <!-- HUD -->
  <div id="hud">
    <span class="hname" id="hname">—</span>
    <div class="hpbar"><div class="hpfill" id="hpfill"></div></div>
    <span id="hptxt" style="font-size:10px;color:#aaa;min-width:50px">100/100</span>
    <span style="font-size:10px;color:#aaa;display:flex;gap:5px">
      <span>⭐<span id="score">0</span></span>
      <span id="star-display">🌟<span id="star-count">0</span></span>
      <span>W<span id="wave">1</span>/3</span>
      <span>👾<span id="ecount">0</span></span>
    </span>
    <button onclick="openSel()" style="margin-left:auto;font-size:9px;font-weight:700;padding:2px 7px;border-radius:5px;border:1px solid rgba(255,255,255,.15);background:transparent;color:#777;cursor:pointer">↺ Held</button>
    <button id="toggle-mobile" onclick="applyMobileMode(!isMobile)" title="Mobile/PC umschalten" style="font-size:11px;padding:2px 7px;border-radius:5px;border:1px solid rgba(255,255,255,.15);background:transparent;color:#aaa;cursor:pointer">📱</button>
  </div>

  <!-- Skill bar (desktop) -->
  <div id="skbar-wrap">
    <span style="font-size:9px;color:#555">WASD · LMB zielen · RMB schiessen · 1-4</span>
    <div style="margin-left:auto;display:flex;gap:4px" id="skbar"></div>
  </div>

  <!-- Game canvas -->
  <div id="cvwrap">
    <canvas id="cv" tabindex="0"></canvas>
    <div id="focusbanner"><span>▶ Tippen / Klicken zum Spielen</span></div>
    <div id="msg" style="opacity:0"></div>

    <!-- Mobile controls overlay -->
    <div id="mobile-controls">
      <div id="joystick-zone">
        <div id="joystick-base"></div>
        <div id="joystick-knob"></div>
      </div>
      <div id="action-buttons">
        <button class="act-btn" id="btn-shoot"><span class="bi">🔫</span>Schiessen</button>
        <button class="act-btn" id="btn-s1"><span class="bi">?</span>[1]</button>
        <button class="act-btn" id="btn-s2"><span class="bi">?</span>[2]</button>
        <button class="act-btn" id="btn-s3"><span class="bi">?</span>[3]</button>
        <button class="act-btn" id="btn-s4"><span class="bi">?</span>[4]</button>
      </div>
    </div>

    <!-- Hero selection -->
    <div id="sel">
      <h2>⚡ HERO CLASH ⚡</h2>
      <div class="hint">Wähle deinen Helden · Mobile: Joystick + Tasten · PC: WASD, LMB zielen, RMB schiessen</div>
      <div id="hgrid"></div>
      <div id="ptxt">Wähle einen Helden</div>
      <button id="gobtn" onclick="startGame()">⚡ Spiel starten</button>
    </div>
  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════
// SETUP
// ═══════════════════════════════════════════════════════
const CV=document.getElementById('cv');
const C=CV.getContext('2d');
let W,H;

function resizeCanvas(){
  const wrap=document.getElementById('cvwrap');
  W=wrap.clientWidth; H=wrap.clientHeight;
  CV.width=W; CV.height=H;
}
window.addEventListener('resize',()=>{resizeCanvas();if(G&&G.p)cam.x=G.p.wx-W/2,cam.y=G.p.wy-H/2;});
resizeCanvas();

const WW=2400,WH=1800,MAX_WAVES=3;

// ═══════════════════════════════════════════════════════
// TOUCH DETECTION — show mobile controls
// ═══════════════════════════════════════════════════════
// Robust mobile detection:
// - matchMedia pointer:coarse = real touch device (finger, not mouse)
// - We never auto-switch on first touchstart (hybrid laptops have touch too)
// - User can manually toggle with the button in HUD
let isMobile = window.matchMedia('(pointer: coarse)').matches;

function applyMobileMode(on) {
  isMobile = on;
  document.getElementById('mobile-controls').style.display = on ? 'block' : 'none';
  document.getElementById('skbar-wrap').style.display    = on ? 'none'  : 'flex';
}
applyMobileMode(isMobile);

// ═══════════════════════════════════════════════════════
// JOYSTICK
// ═══════════════════════════════════════════════════════
const jZone=document.getElementById('joystick-zone');
const jKnob=document.getElementById('joystick-knob');
const JOY_R=36; // max radius knob travels
let joyVec={x:0,y:0}; // normalised -1..1
let joyActive=false;
let joyId=null;
let joyOrigin={x:0,y:0};

function joyStart(cx,cy){
  const rect=jZone.getBoundingClientRect();
  joyOrigin={x:rect.left+rect.width/2, y:rect.top+rect.height/2};
  joyActive=true;
  joyMove(cx,cy);
}
function joyMove(cx,cy){
  let dx=cx-joyOrigin.x, dy=cy-joyOrigin.y;
  const len=Math.hypot(dx,dy);
  if(len>JOY_R){dx=dx/len*JOY_R;dy=dy/len*JOY_R;}
  jKnob.style.transform=`translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
  joyVec={x:dx/JOY_R, y:dy/JOY_R};
}
function joyEnd(){
  joyActive=false;joyVec={x:0,y:0};
  jKnob.style.transform='translate(-50%,-50%)';
}

jZone.addEventListener('touchstart',e=>{
  e.preventDefault();const t=e.changedTouches[0];joyId=t.identifier;joyStart(t.clientX,t.clientY);
},{passive:false});
jZone.addEventListener('touchmove',e=>{
  e.preventDefault();
  for(const t of e.changedTouches)if(t.identifier===joyId)joyMove(t.clientX,t.clientY);
},{passive:false});
jZone.addEventListener('touchend',e=>{
  for(const t of e.changedTouches)if(t.identifier===joyId){joyEnd();joyId=null;}
},{passive:false});

// ═══════════════════════════════════════════════════════
// MOBILE SHOOT BUTTON (auto-aims at nearest enemy)
// ═══════════════════════════════════════════════════════
let mobileShoot=false;
const btnShoot=document.getElementById('btn-shoot');
btnShoot.addEventListener('touchstart',e=>{e.preventDefault();mobileShoot=true;btnShoot.classList.add('pressed');},{passive:false});
btnShoot.addEventListener('touchend',e=>{e.preventDefault();mobileShoot=false;btnShoot.classList.remove('pressed');},{passive:false});

// Mobile skill buttons
[1,2,3,4].forEach(i=>{
  const b=document.getElementById('btn-s'+i);
  b.addEventListener('touchstart',e=>{e.preventDefault();useSkill(i-1);b.classList.add('pressed');},{passive:false});
  b.addEventListener('touchend',e=>{e.preventDefault();b.classList.remove('pressed');},{passive:false});
});

// ═══════════════════════════════════════════════════════
// DESKTOP FOCUS / INPUT
// ═══════════════════════════════════════════════════════
const banner=document.getElementById('focusbanner');
function gainFocus(){CV.focus();banner.style.display='none';}
CV.addEventListener('click',gainFocus);
banner.addEventListener('click',gainFocus);
CV.addEventListener('blur',()=>{
  if(G&&!G.gameOver&&!G.won&&document.getElementById('sel').style.display==='none'&&!isMobile){
    banner.style.display='flex';if(G.keys)G.keys={};mDown.l=false;mDown.r=false;
  }
});
CV.addEventListener('focus',()=>{banner.style.display='none';});
window.addEventListener('blur',()=>{if(G&&G.keys)G.keys={};mDown.l=false;mDown.r=false;});
window.addEventListener('visibilitychange',()=>{if(document.hidden&&G&&G.keys){G.keys={};mDown.l=false;mDown.r=false;}});

let mX=0,mY=0,aimAng=0,mDown={l:false,r:false},cam={x:0,y:0};
CV.addEventListener('mousemove',e=>{const rc=CV.getBoundingClientRect();mX=e.clientX-rc.left;mY=e.clientY-rc.top;});
CV.addEventListener('mousedown',e=>{e.preventDefault();gainFocus();if(e.button===0)mDown.l=true;if(e.button===2)mDown.r=true;});
CV.addEventListener('mouseup',e=>{if(e.button===0)mDown.l=false;if(e.button===2)mDown.r=false;});
CV.addEventListener('contextmenu',e=>e.preventDefault());
CV.addEventListener('keydown',e=>{
  if(!G||!G.keys)return;G.keys[e.key]=true;
  if(e.key==='1')useSkill(0);if(e.key==='2')useSkill(1);
  if(e.key==='3')useSkill(2);if(e.key==='4')useSkill(3);
  if([' ','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))e.preventDefault();
});
CV.addEventListener('keyup',e=>{if(G&&G.keys)G.keys[e.key]=false;});

// ═══════════════════════════════════════════════════════
// WORLD GENERATION
// ═══════════════════════════════════════════════════════
function noise2D(x,y,s){return(Math.sin(x*.017*s)*Math.cos(y*.013*s)+Math.sin(x*.031*s+1.2)*Math.cos(y*.027*s+0.8))*.5+.5}
let terrain=[],wObjs=[],terrainCanvas=null;

function genWorld(){
  wObjs=[];terrain=[];
  const R=(a,b)=>a+Math.random()*(b-a),RI=(a,b)=>Math.floor(R(a,b+1));
  for(let tx=0;tx<WW;tx+=40)for(let ty=0;ty<WH;ty+=40){
    const n=noise2D(tx,ty,1);
    terrain.push({x:tx,y:ty,col:n<.32?'#1a472a':n<.55?'#2d6a4f':n<.72?'#40916c':'#52b788'});
  }
  for(let i=0;i<6;i++){const h2=Math.random()>.5,pos=RI(100,h2?WH-100:WW-100);wObjs.push({type:'path',horiz:h2,pos,width:22+Math.random()*12});}
  for(let i=0;i<12;i++){const rx=R(40,70),ry=R(28,50);wObjs.push({type:'water',wx:R(rx,WW-rx),wy:R(ry,WH-ry),rx,ry});}
  for(let i=0;i<80;i++)wObjs.push({type:'rock',wx:R(30,WW-30),wy:R(30,WH-30),r:R(8,18),angle:R(0,Math.PI),color:'#6b6560',lit:'#9e9590'});
  for(let i=0;i<150;i++)wObjs.push({type:'bush',wx:R(20,WW-20),wy:R(20,WH-20),r:R(9,15),color:'#1b4332',lit:'#2d6a4f'});
  for(let i=0;i<200;i++){const r=R(18,32);wObjs.push({type:'tree',wx:R(r,WW-r),wy:R(r,WH-r),r,color:['#1b4332','#2d6a4f','#1a3a2a','#14532d','#166534'][RI(0,4)]});}
  for(let i=0;i<22;i++){const w=R(45,90),h=R(40,70);wObjs.push({type:'building',wx:R(w/2+30,WW-w/2-30),wy:R(h/2+30,WH-h/2-30),w,h,color:['#4a4a5a','#5a4a3a','#3a3a4a','#6a5a4a','#3d3d3d'][RI(0,4)]});}
  for(let i=0;i<30;i++)wObjs.push({type:'lamp',wx:R(20,WW-20),wy:R(20,WH-20)});
  for(let i=0;i<18;i++){const h2=Math.random()>.5,x=R(50,WW-50),y=R(50,WH-50),len=R(60,160);wObjs.push({type:'fence',x,y,len,horiz:h2});}
}
function isSolid(x,y,r){
  r=r||12;
  for(const o of wObjs){
    if(o.type==='tree'&&Math.hypot(x-o.wx,y-o.wy)<o.r*.65+r*.5)return true;
    if(o.type==='rock'&&Math.hypot(x-o.wx,y-o.wy)<o.r+r*.4)return true;
    if(o.type==='building'&&Math.abs(x-o.wx)<o.w/2+r&&Math.abs(y-o.wy)<o.h/2+r)return true;
    if(o.type==='water'&&((x-o.wx)/o.rx)**2+((y-o.wy)/o.ry)**2<1)return true;
  }
  return x<20||x>WW-20||y<20||y>WH-20;
}

// ═══════════════════════════════════════════════════════
// HEROES
// ═══════════════════════════════════════════════════════
const HEROES=[
  {name:'Starlance',icon:'🦸',role:'Krieger',hcol:'#3949ab',bpCol:'#c5cae9',hp:100,spd:2.8,bColor:'#FFD700',bDmg:18,bSpd:9,passive:'Jeder 3. Schuss kritisch +50%',
   skills:[{name:'Schildwall',icon:'🛡️',key:'1',cd:0,maxCd:300,use:g=>{g.p.shielded=150;showMsg('🛡️ Schildwall!')}},{name:'Sternstoß',icon:'🌟',key:'2',cd:0,maxCd:180,use:g=>burst(5,'#FFD700',22)},{name:'Nova',icon:'💥',key:'3',cd:0,maxCd:420,use:g=>doAoe(110,55,'#FFD700')},{name:'Heilung',icon:'💊',key:'4',cd:0,maxCd:360,use:g=>{g.p.hp=Math.min(g.p.maxHp,g.p.hp+25);showMsg('💊 +25 HP!')}}],init:s=>{s.critCount=0}},
  {name:'Pyra',icon:'🔥',role:'Angriff',hcol:'#bf360c',bpCol:'#ffccbc',hp:85,spd:3.1,bColor:'#ff5722',bDmg:22,bSpd:10,passive:'Schüsse verbrennen Feinde',
   skills:[{name:'Hitzeschild',icon:'♨️',key:'1',cd:0,maxCd:280,use:g=>{g.p.shielded=180;showMsg('♨️ Hitzeschild!')}},{name:'Feuerball',icon:'🌋',key:'2',cd:0,maxCd:150,use:g=>bigShot('#ff1744',40,6)},{name:'Feuerwand',icon:'🔴',key:'3',cd:0,maxCd:320,use:g=>doAoe(85,40,'#ff5722')},{name:'Inferno',icon:'☄️',key:'4',cd:0,maxCd:500,use:g=>doAoe(170,80,'#ff1744')}],init:s=>{}},
  {name:'Volt',icon:'⚡',role:'Schnell',hcol:'#f57f17',bpCol:'#fff9c4',hp:80,spd:4.2,bColor:'#fdd835',bDmg:14,bSpd:13,passive:'Schnellster Held',
   skills:[{name:'Dash',icon:'💨',key:'1',cd:0,maxCd:200,use:g=>{g.p.dodgeCd=100;showMsg('💨 Dash!')}},{name:'Salve',icon:'🌩️',key:'2',cd:0,maxCd:120,use:g=>burst(8,'#fdd835',14)},{name:'Donnerkreis',icon:'🔵',key:'3',cd:0,maxCd:260,use:g=>radial(12,'#fdd835',14)},{name:'Sturm',icon:'🌪️',key:'4',cd:0,maxCd:400,use:g=>radial(20,'#fffde7',18)}],init:s=>{s.dodgeCd=0}},
  {name:'Glacius',icon:'❄️',role:'Kontrolle',hcol:'#0277bd',bpCol:'#b3e5fc',hp:90,spd:2.6,bColor:'#81d4fa',bDmg:16,bSpd:8,passive:'Treffer verlangsamen Feinde',
   skills:[{name:'Eisschild',icon:'🧊',key:'1',cd:0,maxCd:260,use:g=>{g.p.shielded=160;showMsg('🧊 Eisschild!')}},{name:'Eissalve',icon:'❄️',key:'2',cd:0,maxCd:140,use:g=>burst(5,'#81d4fa',16)},{name:'Blizzard',icon:'🌨️',key:'3',cd:0,maxCd:320,use:g=>doFreezeAll()},{name:'Eisfeld',icon:'💎',key:'4',cd:0,maxCd:420,use:g=>doAoe(120,60,'#29b6f6')}],init:s=>{}},
  {name:'Terra',icon:'🌿',role:'Tank',hcol:'#2e7d32',bpCol:'#c8e6c9',hp:150,spd:2.2,bColor:'#a5d6a7',bDmg:20,bSpd:7,passive:'Regen 1 HP/s, viel Leben',
   skills:[{name:'Panzer',icon:'🪨',key:'1',cd:0,maxCd:320,use:g=>{g.p.shielded=240;g.p.armor=true;showMsg('🪨 Wurzelpanzer!')}},{name:'Stein',icon:'🪨',key:'2',cd:0,maxCd:160,use:g=>bigShot('#8d6e63',35,5)},{name:'Ranken',icon:'🌿',key:'3',cd:0,maxCd:280,use:g=>doAoe(90,45,'#66bb6a')},{name:'Erdbeben',icon:'🌍',key:'4',cd:0,maxCd:480,use:g=>doAoe(160,80,'#66bb6a')}],init:s=>{s.regenTimer=0}},
  {name:'Phantom',icon:'👻',role:'Assassin',hcol:'#6a1b9a',bpCol:'#e1bee7',hp:75,spd:3.5,bColor:'#ce93d8',bDmg:28,bSpd:11,passive:'30% Chance Treffer zu ghosten',
   skills:[{name:'Unsichtbar',icon:'🌫️',key:'1',cd:0,maxCd:300,use:g=>{g.p.invisible=180;showMsg('🌫️ Unsichtbar!')}},{name:'Blitz',icon:'👻',key:'2',cd:0,maxCd:140,use:g=>burst(4,'#e040fb',30)},{name:'Seelenraub',icon:'💜',key:'3',cd:0,maxCd:300,use:g=>doDrain()},{name:'Geistersturm',icon:'🌑',key:'4',cd:0,maxCd:440,use:g=>radial(16,'#ce93d8',28)}],init:s=>{}},
  {name:'Graviton',icon:'🌀',role:'Kontrolle',hcol:'#283593',bpCol:'#c5cae9',hp:88,spd:2.7,bColor:'#9fa8da',bDmg:17,bSpd:9,passive:'AOE saugt Feinde an',
   skills:[{name:'Schwarzes Loch',icon:'🕳️',key:'1',cd:0,maxCd:280,use:g=>doBlackHole()},{name:'Puls',icon:'🔵',key:'2',cd:0,maxCd:130,use:g=>burst(4,'#7986cb',17)},{name:'Gravitonsog',icon:'🛸',key:'3',cd:0,maxCd:380,use:g=>doBlackHole()},{name:'Zeitwelle',icon:'⏳',key:'4',cd:0,maxCd:460,use:g=>doFreezeAll()}],init:s=>{}},
  {name:'Solara',icon:'☀️',role:'Support',hcol:'#e65100',bpCol:'#fff8e1',hp:90,spd:2.9,bColor:'#ffe082',bDmg:16,bSpd:10,passive:'+20% Schaden wenn HP > 70%',
   skills:[{name:'Lichtschild',icon:'💛',key:'1',cd:0,maxCd:260,use:g=>{g.p.shielded=150;showMsg('💛 Lichtschild!')}},{name:'Lichtstrahl',icon:'🌞',key:'2',cd:0,maxCd:110,use:g=>doLaser()},{name:'Sonnenwelle',icon:'✨',key:'3',cd:0,maxCd:300,use:g=>doAoe(95,50,'#ffb300')},{name:'Supernova',icon:'🌟',key:'4',cd:0,maxCd:500,use:g=>doAoe(210,100,'#FFD700')}],init:s=>{}},
  {name:'Stahlherz',icon:'🦾',role:'Tank',hcol:'#37474f',bpCol:'#eceff1',hp:140,spd:2.3,bColor:'#cfd8dc',bDmg:24,bSpd:8,passive:'Metallkörper: -3 Schaden, kein Rückstoß',
   skills:[{name:'Titanpanzer',icon:'🛡️',key:'1',cd:0,maxCd:280,use:g=>{g.p.shielded=300;g.p.armor=true;showMsg('🛡️ Titanpanzer!')}},{name:'Stahlwalze',icon:'⚙️',key:'2',cd:0,maxCd:160,use:g=>bigShot('#b0bec5',40,5)},{name:'Metallsturm',icon:'💠',key:'3',cd:0,maxCd:320,use:g=>radial(10,'#cfd8dc',24)},{name:'Stahlsturm',icon:'⚙️',key:'4',cd:0,maxCd:420,use:g=>doAoe(140,70,'#90a4ae')}],init:s=>{}},
  {name:'Nox',icon:'🌑',role:'Dunkel',hcol:'#4527a0',bpCol:'#d1c4e9',hp:82,spd:3.1,bColor:'#b39ddb',bDmg:20,bSpd:10,passive:'Unter 40% HP: +40% Schaden',
   skills:[{name:'Schattenform',icon:'👁️',key:'1',cd:0,maxCd:260,use:g=>{g.p.invisible=150;showMsg('👁️ Schattenform!')}},{name:'Dunkelwelle',icon:'🖤',key:'2',cd:0,maxCd:140,use:g=>burst(5,'#7c4dff',20)},{name:'Schattensturm',icon:'🌑',key:'3',cd:0,maxCd:300,use:g=>radial(14,'#7c4dff',20)},{name:'Apokalypse',icon:'💀',key:'4',cd:0,maxCd:500,use:g=>doAoe(190,95,'#7c4dff')}],init:s=>{}}
];

// ═══════════════════════════════════════════════════════
// GAME STATE
// ═══════════════════════════════════════════════════════
let G={},selIdx=null,animId=null;

function openSel(){
  if(animId){cancelAnimationFrame(animId);animId=null;}
  mDown.l=false;mDown.r=false;if(G&&G.keys)G.keys={};
  joyEnd();mobileShoot=false;
  document.getElementById('sel').style.display='flex';
  buildGrid();
}
function buildGrid(){
  const g=document.getElementById('hgrid');g.innerHTML='';
  HEROES.forEach((h,i)=>{
    const cc=document.createElement('div');cc.className='hcard';if(i===selIdx)cc.classList.add('sel');
    cc.innerHTML='<div class="ci">'+h.icon+'</div><div class="cn">'+h.name+'</div><div class="cr">'+h.role+'</div>';
    cc.onclick=()=>{document.querySelectorAll('.hcard').forEach(x=>x.classList.remove('sel'));cc.classList.add('sel');selIdx=i;document.getElementById('ptxt').textContent='⚡ '+h.passive;document.getElementById('gobtn').classList.add('active');};
    g.appendChild(cc);
  });
}
function startGame(){
  if(selIdx===null)return;
  document.getElementById('sel').style.display='none';
  if(!isMobile){gainFocus();}
  else{banner.style.display='none';}
  initGame(selIdx);
}

function bakeTerrainCanvas(){
  terrainCanvas=document.createElement('canvas');terrainCanvas.width=WW;terrainCanvas.height=WH;
  const tc=terrainCanvas.getContext('2d');
  tc.fillStyle='#2d6a4f';tc.fillRect(0,0,WW,WH);
  terrain.forEach(t=>{tc.fillStyle=t.col;tc.fillRect(t.x,t.y,41,41);});
  wObjs.filter(o=>o.type==='path').forEach(o=>{
    tc.fillStyle='#8B7355';if(o.horiz)tc.fillRect(0,o.pos-o.width/2,WW,o.width);else tc.fillRect(o.pos-o.width/2,0,o.width,WH);
    tc.fillStyle='#9E8B6A';for(let i=0;i<(o.horiz?WW:WH);i+=14){const px=o.horiz?i:o.pos+(Math.random()-.5)*o.width*.7,py=o.horiz?o.pos+(Math.random()-.5)*o.width*.7:i;tc.beginPath();tc.arc(px,py,1.5,0,Math.PI*2);tc.fill();}
  });
  wObjs.filter(o=>o.type==='water').forEach(o=>{
    const g2=tc.createRadialGradient(o.wx,o.wy,0,o.wx,o.wy,Math.max(o.rx,o.ry));
    g2.addColorStop(0,'#1565c0');g2.addColorStop(.7,'#1976d2');g2.addColorStop(1,'#0d47a1');
    tc.fillStyle=g2;tc.beginPath();tc.ellipse(o.wx,o.wy,o.rx,o.ry,0,0,Math.PI*2);tc.fill();
    tc.strokeStyle='#42a5f5';tc.lineWidth=1.5;tc.stroke();
    tc.strokeStyle='rgba(255,255,255,.15)';tc.lineWidth=1;
    for(let r=10;r<Math.min(o.rx,o.ry)*.7;r+=15){tc.beginPath();tc.ellipse(o.wx,o.wy,r,r*.6,0,0,Math.PI*2);tc.stroke();}
  });
  wObjs.filter(o=>o.type==='fence').forEach(o=>{
    tc.strokeStyle='#795548';tc.lineWidth=2;tc.beginPath();
    if(o.horiz){tc.moveTo(o.x,o.y);tc.lineTo(o.x+o.len,o.y);}else{tc.moveTo(o.x,o.y);tc.lineTo(o.x,o.y+o.len);}tc.stroke();
    tc.fillStyle='#6d4c41';for(let i=0;i<=o.len;i+=18){const px=o.horiz?o.x+i:o.x,py=o.horiz?o.y:o.y+i;tc.fillRect(px-2,py-5,4,10);}
  });
}

function initGame(idx){
  const hero=HEROES[idx];hero.skills.forEach(sk=>sk.cd=0);
  genWorld();bakeTerrainCanvas();
  let px=WW/2,py=WH/2;while(isSolid(px,py,20)){px+=30;py+=30;}
  G={hero,p:{wx:px,wy:py,hp:hero.hp,maxHp:hero.hp,spd:hero.spd,
    shielded:0,invisible:0,armor:false,regenTimer:0,shotCd:0,
    critCount:0,dodgeCd:0,legAng:0,walkAnim:0,moving:false},
    bullets:[],enemies:[],particles:[],keys:{},wave:1,score:0,stars:0,hits:0,damageTaken:0,gameOver:false,won:false};
  hero.init(G);cam.x=px-W/2;cam.y=py-H/2;
  spawnWave(1);buildSkBar();updateMobileSkillLabels();updateHud();
  if(animId)cancelAnimationFrame(animId);loop();
}

function buildSkBar(){
  const sb=document.getElementById('skbar');sb.innerHTML='';
  G.hero.skills.forEach((sk,i)=>{
    const b=document.createElement('button');b.className='skbtn ready';b.id='sk'+i;
    b.addEventListener('mousedown',e=>{e.preventDefault();useSkill(i);if(!isMobile)gainFocus();});
    b.innerHTML='<span style="font-size:12px">'+sk.icon+'</span><span>['+sk.key+'] '+sk.name+'</span><span id="scd'+i+'" style="font-size:9px;opacity:.7">Bereit</span>';
    sb.appendChild(b);
  });
}

function updateMobileSkillLabels(){
  if(!G||!G.hero)return;
  G.hero.skills.forEach((sk,i)=>{
    const b=document.getElementById('btn-s'+(i+1));
    if(b)b.innerHTML='<span class="bi">'+sk.icon+'</span>['+sk.key+']';
  });
}

function spawnWave(w){
  const types=['grunt','tank','fast','shooter'],count=3+w*2;
  for(let i=0;i<count;i++){
    let ex,ey,tries=0;
    do{const ang=Math.random()*Math.PI*2,d=260+Math.random()*200;ex=G.p.wx+Math.cos(ang)*d;ey=G.p.wy+Math.sin(ang)*d;ex=Math.max(30,Math.min(WW-30,ex));ey=Math.max(30,Math.min(WH-30,ey));tries++;}while(isSolid(ex,ey,12)&&tries<25);
    const t=types[Math.floor(Math.random()*types.length)],hp=(t==='tank'?30:12)+w*3;
    G.enemies.push({wx:ex,wy:ey,hp,maxHp:hp,spd:t==='fast'?1.4:0.8,type:t,
      shotTimer:t==='shooter'?180:99999,frozen:0,burned:0,legAng:0,walkAnim:0,
      col:t==='grunt'?'#c62828':t==='tank'?'#546e7a':t==='fast'?'#e65100':'#6a1b9a'});
  }
}

function loop(){update();draw();if(!G.gameOver&&!G.won)animId=requestAnimationFrame(loop);else{draw();showMsg(G.won?`🏆 EPISCHER SIEG! ${'⭐'.repeat(G.stars)}`:'💀 NIEDERLAGE!');setTimeout(openSel,2500);}}

// ═══════════════════════════════════════════════════════
// UPDATE — combined PC + Mobile input
// ═══════════════════════════════════════════════════════
function findNearest(){
  if(!G.enemies.length)return null;
  return G.enemies.reduce((a,b)=>Math.hypot(G.p.wx-a.wx,G.p.wy-a.wy)<Math.hypot(G.p.wx-b.wx,G.p.wy-b.wy)?a:b);
}

function update(){
  const p=G.p,h=G.hero;
  let dx=0,dy=0;
  const spd=p.spd*(p.dodgeCd>0?1.9:1);

  // ── Movement: keyboard OR joystick ──
  if(isMobile){
    dx=joyVec.x*spd; dy=joyVec.y*spd;
  } else {
    if(G.keys['a']||G.keys['A']||G.keys['ArrowLeft'])dx-=spd;
    if(G.keys['d']||G.keys['D']||G.keys['ArrowRight'])dx+=spd;
    if(G.keys['w']||G.keys['W']||G.keys['ArrowUp'])dy-=spd;
    if(G.keys['s']||G.keys['S']||G.keys['ArrowDown'])dy+=spd;
    if(dx&&dy){dx*=.707;dy*=.707;}
  }

  p.moving=!!(dx||dy);
  if(p.moving){p.walkAnim+=.2;p.legAng=Math.sin(p.walkAnim)*.45;}
  else{p.legAng*=.8;p.walkAnim*=.9;}

  const nx=Math.max(20,Math.min(WW-20,p.wx+dx)),ny=Math.max(20,Math.min(WH-20,p.wy+dy));
  if(!isSolid(nx,ny,14)){p.wx=nx;p.wy=ny;}else if(!isSolid(nx,p.wy,14)){p.wx=nx;}else if(!isSolid(p.wx,ny,14)){p.wy=ny;}

  cam.x+=(p.wx-W/2-cam.x)*.1;cam.y+=(p.wy-H/2-cam.y)*.1;
  cam.x=Math.max(0,Math.min(WW-W,cam.x));cam.y=Math.max(0,Math.min(WH-H,cam.y));

  // ── Aim: mouse OR nearest enemy (mobile) ──
  if(isMobile){
    const near=findNearest();
    if(near)aimAng=Math.atan2(near.wy-p.wy,near.wx-p.wx);
  } else {
    aimAng=Math.atan2(mY-(p.wy-cam.y),mX-(p.wx-cam.x));
  }

  // ── Shoot: RMB or mobile shoot button ──
  if(p.shotCd>0)p.shotCd--;
  const wantsShoot=isMobile?mobileShoot:mDown.r;
  if(wantsShoot&&p.shotCd<=0){firePlayerBullet();p.shotCd=18;}

  if(p.shielded>0)p.shielded--;if(p.invisible>0)p.invisible--;if(p.shielded===0)p.armor=false;
  if(p.dodgeCd>0)p.dodgeCd--;
  if(h.name==='Terra'){p.regenTimer++;if(p.regenTimer>=60){p.regenTimer=0;p.hp=Math.min(p.maxHp,p.hp+1);}}

  // Update skill cooldowns + button states
  h.skills.forEach((sk,i)=>{
    if(sk.cd>0){
      sk.cd--;
      // desktop buttons
      const b=document.getElementById('sk'+i),s=document.getElementById('scd'+i);
      if(b){b.classList.toggle('ready',sk.cd===0);b.classList.toggle('off',sk.cd>0);}
      if(s)s.textContent=sk.cd===0?'Bereit':Math.ceil(sk.cd/60)+'s';
      // mobile buttons
      const mb=document.getElementById('btn-s'+(i+1));
      if(mb){mb.classList.toggle('sk-off',sk.cd>0);}
    } else {
      const mb=document.getElementById('btn-s'+(i+1));
      if(mb)mb.classList.remove('sk-off');
    }
  });

  // Bullets
  G.bullets=G.bullets.filter(b=>{
    b.wx+=Math.cos(b.ang)*b.spd;b.wy+=Math.sin(b.ang)*b.spd;
    if(b.wx<0||b.wx>WW||b.wy<0||b.wy>WH)return false;
    if(isSolid(b.wx,b.wy,3))return false;
    if(b.friendly){
      let hit=false;
      for(let i=G.enemies.length-1;i>=0;i--){
        const e=G.enemies[i];
        if(Math.hypot(b.wx-e.wx,b.wy-e.wy)<14){
          let dmg=b.dmg;
          if(h.name==='Nox'&&p.hp/p.maxHp<.4)dmg=Math.round(dmg*1.4);
          if(h.name==='Solara'&&p.hp/p.maxHp>.7)dmg=Math.round(dmg*1.2);
          if(b.burn)e.burned=120;if(b.slow)e.frozen=120;
          e.hp-=dmg;parts(e.wx,e.wy,b.col,5);
          G.hits++;
          if(!b.pierce)hit=true;if(e.hp<=0){G.score+=10;G.enemies.splice(i,1);}if(hit)break;
        }
      }
      return !hit;
    }else{
      if(Math.hypot(b.wx-p.wx,b.wy-p.wy)<14){
        if(p.invisible>0){}
        else if(p.shielded>0){parts(p.wx,p.wy,'#29b6f6',6);}
        else{let dmg=Math.round(p.maxHp/16);if(h.name==='Stahlherz')dmg=Math.max(0,dmg-3);if(h.name==='Phantom'&&Math.random()<.3)return false;G.damageTaken+=dmg;p.hp-=dmg;parts(p.wx,p.wy,'#ff5252',5);}
        return false;
      }
      return true;
    }
  });

  G.enemies.forEach(e=>{
    if(e.frozen>0){e.frozen--;return;}
    const ang=Math.atan2(p.wy-e.wy,p.wx-e.wx);
    const nx2=e.wx+Math.cos(ang)*e.spd,ny2=e.wy+Math.sin(ang)*e.spd;
    if(!isSolid(nx2,ny2,10)){e.wx=nx2;e.wy=ny2;}else if(!isSolid(nx2,e.wy,10)){e.wx=nx2;}else if(!isSolid(e.wx,ny2,10)){e.wy=ny2;}
    e.walkAnim=(e.walkAnim||0)+.18;e.legAng=Math.sin(e.walkAnim)*.4;
    if(e.burned>0){e.burned--;if(e.burned%20===0){e.hp-=3;parts(e.wx,e.wy,'#ff7043',2);}}
    if(e.type==='shooter'){e.shotTimer--;if(e.shotTimer<=0){e.shotTimer=180+Math.random()*120;G.bullets.push({wx:e.wx,wy:e.wy,ang,spd:2.2,dmg:3,friendly:false,col:'#ef5350'});}}
    if(Math.hypot(e.wx-p.wx,e.wy-p.wy)<16){
      if(p.invisible>0)return;if(p.shielded>0){parts(p.wx,p.wy,'#29b6f6',5);return;}
      let dmg=Math.round(p.maxHp/16);if(h.name==='Stahlherz')dmg=Math.max(0,dmg-3);if(h.name==='Phantom'&&Math.random()<.3)return;
      G.damageTaken+=dmg;p.hp-=dmg;parts(p.wx,p.wy,'#ff5252',4);
    }
  });
  G.enemies=G.enemies.filter(e=>e.hp>0);
  G.particles=G.particles.filter(pt=>{pt.wx+=pt.vx;pt.wy+=pt.vy;pt.life--;pt.vx*=.88;pt.vy*=.88;return pt.life>0;});
  if(p.hp<=0){p.hp=0;G.gameOver=true;}
  if(G.enemies.length===0){G.wave++;if(G.wave>MAX_WAVES){G.stars=calculateStars();G.won=true;return;}showMsg('Welle '+G.wave+'/'+MAX_WAVES+'!');spawnWave(G.wave);p.hp=Math.min(p.maxHp,p.hp+20);}
  updateHud();
}

function calculateStars(){
  if(!G) return 0;
  const hitScore=Math.min(1, G.hits/20);
  const defenseScore=1-Math.min(1, G.damageTaken/(G.p.maxHp*1.5));
  const stars=Math.round(1+hitScore+defenseScore);
  return Math.max(1, Math.min(3, stars));
}

function firePlayerBullet(){
  const p=G.p,h=G.hero;let dmg=h.bDmg;
  if(h.name==='Starlance'){p.critCount++;if(p.critCount>=3){dmg=Math.round(dmg*1.5);p.critCount=0;}}
  G.bullets.push({wx:p.wx,wy:p.wy,ang:aimAng,spd:h.bSpd,dmg,friendly:true,col:h.bColor,burn:h.name==='Pyra',slow:h.name==='Glacius'});
}

// ═══════════════════════════════════════════════════════
// DRAW
// ═══════════════════════════════════════════════════════
function sxf(x){return x-cam.x;}function syf(y){return y-cam.y;}
function darken(hex,f){let r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);return'rgba('+Math.round(r*f)+','+Math.round(g*f)+','+Math.round(b*f)+',1)';}

function drawTerrain(){if(terrainCanvas)C.drawImage(terrainCanvas,cam.x,cam.y,W,H,0,0,W,H);else{C.fillStyle='#2d6a4f';C.fillRect(0,0,W,H);}}

function drawStaticObjs(){
  const vis=wObjs.filter(o=>o.type!=='path'&&o.type!=='water'&&o.type!=='fence'&&sxf(o.wx||o.x)>-100&&sxf(o.wx||o.x)<W+100&&syf(o.wy||o.y)>-100&&syf(o.wy||o.y)<H+100);
  vis.sort((a,b)=>(a.wy||a.y||0)-(b.wy||b.y||0));
  vis.forEach(o=>{
    const ox=sxf(o.wx),oy=syf(o.wy);
    if(o.type==='lamp'){C.strokeStyle='#546e7a';C.lineWidth=3;C.beginPath();C.moveTo(ox,oy+14);C.lineTo(ox,oy-28);C.stroke();C.beginPath();C.moveTo(ox,oy-28);C.lineTo(ox+10,oy-32);C.stroke();C.fillStyle='#fff9c4';C.beginPath();C.arc(ox+10,oy-33,4,0,Math.PI*2);C.fill();C.fillStyle='rgba(255,249,196,.18)';C.beginPath();C.arc(ox+10,oy-33,18,0,Math.PI*2);C.fill();}
    else if(o.type==='rock'){C.fillStyle='rgba(0,0,0,.22)';C.beginPath();C.ellipse(ox+3,oy+4,o.r*1.1,o.r*.55,.2,0,Math.PI*2);C.fill();C.fillStyle=o.color;C.beginPath();C.ellipse(ox,oy,o.r,o.r*.7,o.angle,0,Math.PI*2);C.fill();C.fillStyle=o.lit;C.beginPath();C.ellipse(ox-o.r*.25,oy-o.r*.2,o.r*.55,o.r*.3,o.angle-.3,0,Math.PI*2);C.fill();}
    else if(o.type==='bush'){C.fillStyle='rgba(0,0,0,.2)';C.beginPath();C.ellipse(ox+2,oy+4,o.r*.9,o.r*.4,0,0,Math.PI*2);C.fill();C.fillStyle=o.color;C.beginPath();C.arc(ox-o.r*.3,oy,o.r*.75,0,Math.PI*2);C.fill();C.beginPath();C.arc(ox+o.r*.3,oy+1,o.r*.7,0,Math.PI*2);C.fill();C.fillStyle=o.lit;C.beginPath();C.arc(ox,oy-o.r*.3,o.r*.55,0,Math.PI*2);C.fill();}
    else if(o.type==='tree'){
      C.fillStyle='rgba(0,0,0,.2)';C.beginPath();C.ellipse(ox+o.r*.4,oy+o.r*.6,o.r*.9,o.r*.35,.2,0,Math.PI*2);C.fill();
      const trunkW=Math.max(5,o.r*.28),trunkH=o.r*.9;
      const tg=C.createLinearGradient(ox-trunkW,oy,ox+trunkW,oy);tg.addColorStop(0,'#4e342e');tg.addColorStop(.4,'#6d4c41');tg.addColorStop(1,'#4e342e');
      C.fillStyle=tg;C.fillRect(ox-trunkW/2,oy-trunkH,trunkW,trunkH+8);
      C.strokeStyle='#4e342e';C.lineWidth=2;C.beginPath();C.moveTo(ox-trunkW/2,oy);C.lineTo(ox-trunkW/2-6,oy+6);C.stroke();C.beginPath();C.moveTo(ox+trunkW/2,oy);C.lineTo(ox+trunkW/2+6,oy+6);C.stroke();
      for(let l=2;l>=0;l--){const ly=oy-trunkH-l*o.r*.45,lr=o.r*(1-.15*l);C.fillStyle=l===0?'#1b4332':l===1?o.color:'#40916c';C.beginPath();C.arc(ox,ly,lr,0,Math.PI*2);C.fill();C.fillStyle=l===2?'#2d6a4f':'#52b788';C.beginPath();C.arc(ox-lr*.35,ly-lr*.2,lr*.55,0,Math.PI*2);C.fill();C.beginPath();C.arc(ox+lr*.25,ly-lr*.35,lr*.45,0,Math.PI*2);C.fill();}
    }
    else if(o.type==='building'){
      C.fillStyle='rgba(0,0,0,.28)';C.fillRect(ox-o.w/2+6,oy-o.h/2+6,o.w,o.h);
      const wg=C.createLinearGradient(ox-o.w/2,oy,ox+o.w/2,oy);wg.addColorStop(0,darken(o.color,.7));wg.addColorStop(.5,o.color);wg.addColorStop(1,darken(o.color,.85));
      C.fillStyle=wg;C.fillRect(ox-o.w/2,oy-o.h/2,o.w,o.h);C.fillStyle=darken(o.color,.6);C.fillRect(ox-o.w/2,oy-o.h/2,o.w,o.h*.28);
      const wCols=Math.max(2,Math.floor(o.w/20)),wRows=Math.max(1,Math.floor(o.h*.55/18));
      for(let r=0;r<wRows;r++)for(let cc=0;cc<wCols;cc++){const wx2=ox-o.w/2+10+(cc*(o.w-20)/(wCols-1||1)),wy2=oy-o.h/2+o.h*.35+r*18;C.fillStyle='rgba(180,200,255,.5)';C.fillRect(wx2-4,wy2-5,8,9);}
      C.fillStyle='#3e2723';C.fillRect(ox-5,oy+o.h/2-18,10,18);
    }
  });
}

function drawAvatar(wx2,wy2,facing,hcol,bpCol,inv,shielded,legAng,icon){
  C.save();C.translate(wx2,wy2);if(inv)C.globalAlpha=.3;
  C.fillStyle='rgba(0,0,0,.25)';C.beginPath();C.ellipse(0,14,13,5,0,0,Math.PI*2);C.fill();
  const fL=Math.cos(facing)<0;
  C.save();C.translate(-4,6);C.rotate(legAng*.8);C.fillStyle='#37474f';C.fillRect(-3,0,6,13);C.fillStyle='#1a1a1a';C.fillRect(-4,12,8,5);C.restore();
  C.save();C.translate(4,6);C.rotate(-legAng*.8);C.fillStyle='#263238';C.fillRect(-3,0,6,13);C.fillStyle='#1a1a1a';C.fillRect(-4,12,8,5);C.restore();
  C.save();if(fL)C.scale(-1,1);
  C.fillStyle=hcol+'99';C.beginPath();C.moveTo(-2,-6);C.bezierCurveTo(-14,2,-12,14,-8,16);C.lineTo(-2,14);C.closePath();C.fill();
  const tg=C.createLinearGradient(-8,-6,8,-6);tg.addColorStop(0,darken(hcol,.7));tg.addColorStop(.5,hcol);tg.addColorStop(1,darken(hcol,.8));
  C.fillStyle=tg;C.beginPath();C.roundRect(-7,-6,14,16,3);C.fill();
  C.fillStyle='rgba(255,255,255,.5)';C.beginPath();C.arc(0,1,4,0,Math.PI*2);C.fill();C.fillStyle='rgba(255,255,255,.9)';C.beginPath();C.arc(0,1,2,0,Math.PI*2);C.fill();
  C.save();const armAng=fL?Math.PI-facing:facing;C.rotate(armAng);C.fillStyle=hcol;C.fillRect(6,-3,11,6);C.fillStyle=darken(hcol,.7);C.fillRect(14,-2,6,4);C.fillStyle=bpCol;C.beginPath();C.arc(6,0,4,0,Math.PI*2);C.fill();C.restore();
  C.fillStyle=hcol;C.fillRect(-16,-4,10,6);C.restore();
  C.fillStyle='#ffcc80';C.fillRect(-3,-7,6,4);C.fillStyle='#ffcc80';C.beginPath();C.arc(0,-15,8,0,Math.PI*2);C.fill();
  const md=fL?-1:1;C.fillStyle=hcol+'dd';C.beginPath();C.roundRect(md>0?-2:-7,-19,8,6,2);C.fill();
  C.fillStyle='#fff';C.beginPath();C.arc(md*3,-16,2,0,Math.PI*2);C.fill();C.fillStyle='#111';C.beginPath();C.arc(md*3,-16,1,0,Math.PI*2);C.fill();
  C.fillStyle='#3e2723';C.beginPath();C.arc(0,-22,5,Math.PI,0);C.fill();
  C.font='13px serif';C.textAlign='center';C.textBaseline='middle';C.fillText(icon,0,-34);
  if(shielded>0){C.globalAlpha=inv?.3:1;C.strokeStyle='rgba(41,182,246,.7)';C.lineWidth=2;C.beginPath();C.arc(0,-6,22,0,Math.PI*2);C.stroke();C.strokeStyle='rgba(41,182,246,.2)';C.lineWidth=6;C.stroke();}
  C.restore();
}

function drawEnemy(e){
  const ox=sxf(e.wx),oy=syf(e.wy);C.save();C.translate(ox,oy);
  const frozen=e.frozen>0,legA=e.legAng||0,col=frozen?'#81d4fa':e.col;if(frozen)C.globalAlpha=.8;
  C.fillStyle='rgba(0,0,0,.22)';C.beginPath();C.ellipse(0,12,11,4,0,0,Math.PI*2);C.fill();
  C.fillStyle='#212121';C.save();C.translate(-4,5);C.rotate(legA*.8);C.fillRect(-3,0,5,12);C.restore();C.save();C.translate(4,5);C.rotate(-legA*.8);C.fillRect(-2,0,5,12);C.restore();
  C.fillStyle='#000';C.save();C.translate(-4,5);C.rotate(legA*.8);C.fillRect(-4,11,7,4);C.restore();C.save();C.translate(4,5);C.rotate(-legA*.8);C.fillRect(-3,11,7,4);C.restore();
  if(e.type==='tank'){C.fillStyle=col;C.fillRect(-9,-7,18,16);C.fillStyle='rgba(0,0,0,.35)';C.fillRect(-9,-7,18,5);}
  else if(e.type==='shooter'){C.fillStyle=col;C.beginPath();C.roundRect(-7,-7,14,14,3);C.fill();C.fillStyle='#333';C.fillRect(7,-2,12,4);}
  else{C.fillStyle=col;C.beginPath();C.roundRect(-7,-7,14,14,2);C.fill();}
  C.fillStyle='#b71c1c';C.fillRect(-3,-8,6,3);C.fillStyle=frozen?'#e3f2fd':'#c62828';C.beginPath();C.arc(0,-14,6,0,Math.PI*2);C.fill();
  C.fillStyle='#fff';C.beginPath();C.arc(-2,-15,1.5,0,Math.PI*2);C.fill();C.beginPath();C.arc(3,-15,1.5,0,Math.PI*2);C.fill();
  C.fillStyle='#f00';C.beginPath();C.arc(-2,-15,.8,0,Math.PI*2);C.fill();C.beginPath();C.arc(3,-15,.8,0,Math.PI*2);C.fill();
  C.fillStyle='rgba(0,0,0,.55)';C.fillRect(-10,-26,20,4);C.fillStyle=e.hp/e.maxHp>.5?'#4caf50':'#ef5350';C.fillRect(-10,-26,20*(e.hp/e.maxHp),4);
  C.restore();
}

function draw(){
  C.clearRect(0,0,W,H);drawTerrain();drawStaticObjs();
  G.particles.forEach(pt=>{C.globalAlpha=pt.life/pt.maxLife;C.beginPath();C.arc(sxf(pt.wx),syf(pt.wy),pt.r,0,Math.PI*2);C.fillStyle=pt.col;C.fill();C.globalAlpha=1;});
  G.bullets.forEach(b=>{
    const bx=sxf(b.wx),by=syf(b.wy);if(bx<-10||bx>W+10||by<-10||by>H+10)return;
    C.save();C.translate(bx,by);C.rotate(b.ang);C.fillStyle=b.col;
    if(b.pierce){C.fillRect(-11,-4,22,8);}else{C.beginPath();C.ellipse(0,0,8,4,0,0,Math.PI*2);C.fill();}
    C.globalAlpha=.25;C.beginPath();C.arc(0,0,10,0,Math.PI*2);C.fillStyle=b.col;C.fill();C.restore();
  });
  [...G.enemies].sort((a,b)=>a.wy-b.wy).forEach(e=>{if(sxf(e.wx)>-50&&sxf(e.wx)<W+50&&syf(e.wy)>-50&&syf(e.wy)<H+50)drawEnemy(e);});
  const p=G.p;
  drawAvatar(sxf(p.wx),syf(p.wy),aimAng,G.hero.hcol,G.hero.bpCol,p.invisible>0,p.shielded,p.legAng,G.hero.icon);
  // aim line (desktop only)
  if(!isMobile&&mDown.l){C.save();C.strokeStyle=G.hero.bColor;C.lineWidth=1;C.globalAlpha=.25;C.setLineDash([5,6]);C.beginPath();C.moveTo(sxf(p.wx),syf(p.wy));C.lineTo(sxf(p.wx)+Math.cos(aimAng)*300,syf(p.wy)+Math.sin(aimAng)*300);C.stroke();C.restore();}
  // crosshair (desktop only)
  if(!isMobile){C.save();C.strokeStyle=mDown.l?G.hero.bColor:'rgba(255,255,255,.4)';C.lineWidth=1.5;C.beginPath();C.arc(mX,mY,7,0,Math.PI*2);C.stroke();C.beginPath();C.moveTo(mX-11,mY);C.lineTo(mX+11,mY);C.moveTo(mX,mY-11);C.lineTo(mX,mY+11);C.stroke();C.restore();}
  // minimap
  const mmw=80,mmh=60,mmx=W-mmw-8,mmy=8;
  C.fillStyle='rgba(0,0,0,.6)';C.fillRect(mmx,mmy,mmw,mmh);C.strokeStyle='rgba(255,255,255,.18)';C.lineWidth=1;C.strokeRect(mmx,mmy,mmw,mmh);C.fillStyle='#2d6a4f';C.fillRect(mmx+1,mmy+1,mmw-2,mmh-2);
  wObjs.filter(o=>o.type==='water').forEach(o=>{C.fillStyle='#1565c0';C.beginPath();C.ellipse(mmx+o.wx/WW*mmw,mmy+o.wy/WH*mmh,o.rx/WW*mmw*2,o.ry/WH*mmh*2,0,0,Math.PI*2);C.fill();});
  G.enemies.forEach(e=>{C.fillStyle=e.col;C.beginPath();C.arc(mmx+e.wx/WW*mmw,mmy+e.wy/WH*mmh,2,0,Math.PI*2);C.fill();});
  C.fillStyle='#FFD700';C.beginPath();C.arc(mmx+p.wx/WW*mmw,mmy+p.wy/WH*mmh,3,0,Math.PI*2);C.fill();
  C.strokeStyle='rgba(255,255,255,.3)';C.lineWidth=.8;C.strokeRect(mmx+cam.x/WW*mmw,mmy+cam.y/WH*mmh,W/WW*mmw,H/WH*mmh);
}

// ═══════════════════════════════════════════════════════
// SKILL HELPERS
// ═══════════════════════════════════════════════════════
function burst(n,col,dmg){for(let i=0;i<n;i++){const sp=(Math.random()-.5)*.35;G.bullets.push({wx:G.p.wx,wy:G.p.wy,ang:aimAng+sp,spd:G.hero.bSpd+1,dmg,friendly:true,col});}}
function bigShot(col,dmg,spd){G.bullets.push({wx:G.p.wx,wy:G.p.wy,ang:aimAng,spd,dmg,friendly:true,col,pierce:true});}
function radial(n,col,dmg){for(let i=0;i<n;i++){G.bullets.push({wx:G.p.wx,wy:G.p.wy,ang:(i/n)*Math.PI*2,spd:G.hero.bSpd,dmg,friendly:true,col});}}
function doAoe(rng,dmg,col){const p=G.p;G.enemies.forEach(e=>{if(Math.hypot(p.wx-e.wx,p.wy-e.wy)<rng){if(G.hero.name==='Graviton'){const a=Math.atan2(p.wy-e.wy,p.wx-e.wx);e.wx+=Math.cos(a)*25;e.wy+=Math.sin(a)*25;}e.hp-=dmg;parts(e.wx,e.wy,col,8);}});G.enemies=G.enemies.filter(e=>{if(e.hp<=0){G.score+=10;return false;}return true;});for(let i=0;i<20;i++){const a=Math.random()*Math.PI*2;parts(p.wx+Math.cos(a)*rng*.5,p.wy+Math.sin(a)*rng*.5,col,1);}}
function doFreezeAll(){G.enemies.forEach(e=>{e.frozen=240;parts(e.wx,e.wy,'#b3e5fc',7);});showMsg('❄️ Alle eingefroren!');}
function doBlackHole(){const p=G.p;G.enemies.forEach(e=>{const a=Math.atan2(p.wy-e.wy,p.wx-e.wx);e.wx+=Math.cos(a)*50;e.wy+=Math.sin(a)*50;e.hp-=35;parts(e.wx,e.wy,'#7986cb',6);});G.enemies=G.enemies.filter(e=>{if(e.hp<=0){G.score+=10;return false;}return true;});}
function doDrain(){const p=G.p;let tot=0;G.enemies.forEach(e=>{if(Math.hypot(p.wx-e.wx,p.wy-e.wy)<90){e.hp-=35;tot+=17;parts(e.wx,e.wy,'#ce93d8',5);}});G.enemies=G.enemies.filter(e=>{if(e.hp<=0){G.score+=10;return false;}return true;});p.hp=Math.min(p.maxHp,p.hp+tot);if(tot)showMsg('💜 +'+tot+' HP!');}
function doLaser(){const p=G.p;for(let d=0;d<230;d+=8){const lx=p.wx+Math.cos(aimAng)*d,ly=p.wy+Math.sin(aimAng)*d;G.enemies.forEach(e=>{if(Math.hypot(lx-e.wx,ly-e.wy)<12){e.hp-=4;parts(lx,ly,'#ffe082',2);}});}G.enemies=G.enemies.filter(e=>{if(e.hp<=0){G.score+=10;return false;}return true;});}
function parts(wx2,wy2,col,n){for(let i=0;i<n;i++){const a=Math.random()*Math.PI*2,s=1+Math.random()*2.5;G.particles.push({wx:wx2,wy:wy2,vx:Math.cos(a)*s,vy:Math.sin(a)*s,r:1.5+Math.random()*3,col,life:10+Math.random()*15,maxLife:18});}}
function showMsg(t){const m=document.getElementById('msg');m.textContent=t;m.style.opacity='1';clearTimeout(G._mt);G._mt=setTimeout(()=>m.style.opacity='0',1400);}
function updateHud(){
  const p=G.p;
  document.getElementById('hpfill').style.width=(p.hp/p.maxHp*100)+'%';
  document.getElementById('hptxt').textContent=Math.max(0,Math.round(p.hp))+'/'+p.maxHp;
  document.getElementById('score').textContent=G.score;
  document.getElementById('star-count').textContent=G.stars;
  document.getElementById('wave').textContent=G.wave;
  document.getElementById('ecount').textContent=G.enemies.length;
  document.getElementById('hname').textContent=G.hero.icon+' '+G.hero.name;
  const pct=p.hp/p.maxHp;
  document.getElementById('hpfill').style.background=pct>.5?'#4CAF50':pct>.25?'#ffb300':'#ef5350';
}
function useSkill(i){if(!G||G.gameOver||G.won)return;const sk=G.hero.skills[i];if(sk.cd>0)return;sk.use(G);if(sk.maxCd>0)sk.cd=sk.maxCd;}
buildGrid();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=750, scrolling=False)
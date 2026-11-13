// Loads the built game with no internet, starts it, and checks the 3D world is running with no errors.
//   cd tests && node smoke.js
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const ctx=await b.newContext({viewport:{width:1300,height:900},offline:true});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push('PAGE '+e.message));
await p.goto('file://'+__dirname+'/../index.html');await p.waitForTimeout(3500);
console.log('title:',await p.title());
await p.click('#playBtn');await p.waitForTimeout(2500);
console.log('3D engine loaded:',await p.evaluate(()=>!!window.THREE),'| game running:',await p.evaluate(()=>!!window.__ueg),'| cash:',await p.$eval('#hMoney',e=>e.textContent));
await p.screenshot({path:'smoke.png'});
console.log('errors',JSON.stringify(errs));await b.close();})();

// Actual Sports view + Boost CSS; Dialog and API are controlled browser fixtures.
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const apps = path.resolve(__dirname, '../../../..');
(async()=>{
 const browser=await chromium.launch({args:['--no-sandbox']});
 try {
  for(const width of [1440,390]){
   const page=await browser.newPage({viewport:{width,height:950}}); page.setDefaultTimeout(10000);
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.setContent('<style>*{box-sizing:border-box}body{margin:12px;font-family:sans-serif}.table{width:100%;border-collapse:collapse}.table-bordered td,.table-bordered th{border:1px solid #ddd;padding:10px}button{cursor:pointer}.modal-fixture{position:fixed;inset:12px;background:white;border:1px solid #aaa;padding:16px;z-index:10000;overflow:auto}.modal-fixture label{display:block}.modal-fixture input,.modal-fixture textarea{max-width:100%}.modal-fixture dl{overflow-wrap:anywhere}</style><main class="ing-console-page" style="--ing-line:#d6e0ea;--ing-ink:#1f3749;--ing-soft:#eef5f9"><aside class="ing-console-sidebar">Sports</aside><section class="ing-console-main"><div class="ing-console-content" id="host"></div></section></main>');
   await page.addStyleTag({path:path.join(apps,'erp_boost/erp_boost/erp_boost/page/boost_console/boost_console.css')});
   await page.addScriptTag({path:path.join(apps,'frappe/frappe/public/js/lib/jquery/jquery.min.js')});
   await page.evaluate(fields=>{
    window.registrationFields=fields;
    window.__=(s,a=[])=>s.replace(/\{(\d+)\}/g,(_,i)=>a[i]);window.calls=[];window.messages=[];
    window.records=[{name:'REG-1',full_name:'Sample Player',status:'Pending',can_review:true,company:'Academy',program:'PROGRAM',requested_pathway:'Foundations',submitted_on:'2026-11-03 10:00:00.123456',first_name:'Sample',last_name:'Player',contact_email:'sample.player@example.invalid',guardian_name:'Sample Guardian',guardian_email:'guardian@example.invalid',guardian_phone:'08000000000',home_address:'Training Road, Academy District\nSecond address line',medical_notes:'A long synthetic note for testing readable multi-line content and narrow screen wrapping.',medical_consent:1,media_consent:0,terms_accepted:1},
      {name:'REG-READ',full_name:'Read Only',status:'Pending',can_review:false,requested_pathway:'Foundations'},
      {name:'REG-ACCEPTED',full_name:'Accepted Player',status:'Accepted',can_review:false},
      {name:'REG-REJECTED',full_name:'Rejected Player',status:'Rejected',can_review:false}];
    window.frappe={boost_console_views:{},provide(){},router:{slug:s=>s.toLowerCase().replaceAll(' ','-')},datetime:{get_today:()=> '2026-11-03',str_to_user:s=>s},model:{can_read:()=>true},msgprint:s=>messages.push(s),
     call:async({method,args={}})=>{
      const action=method.split('.').at(-1);calls.push({action,args});
      if(action==='list_registrations')return {message:records.filter(r=>r.status===args.status).map(r=>({...r}))};
      const row=records.find(r=>r.name===args.name);
      if(action==='get_registration')return {message:{registration:{...row},can_review:row.can_review,possible_matches:[{name:'PLAYER-MATCH',full_name:'Possible Match',birth_date:'2012-01-01'}],fields:registrationFields}};
      if(action==='accept_registration'){row.status='Accepted';row.can_review=false;row.player='PLAYER-NEW';return {message:row.player};}
      if(action==='reject_registration'){row.status='Rejected';row.can_review=false;row.rejection_reason=args.reason;return {message:row.name};}
      throw Error('Unexpected API '+action);
     },ui:{Dialog:class{
      constructor(options){this.options=options;this.fields_dict={};this.el=document.createElement('section');this.el.className='modal-fixture';this.el.role='dialog';const h=document.createElement('h2');h.textContent=options.title;this.el.append(h);
       for(const df of options.fields){const wrap=document.createElement('div');const field={df,$wrapper:$(wrap)};if(df.fieldtype!=='HTML'){const label=document.createElement('label');label.textContent=df.label;const input=document.createElement(df.fieldtype==='Small Text'?'textarea':'input');input.name=df.fieldname;input.value=df.default||'';label.append(input);wrap.append(label);field.input=input;}this.fields_dict[df.fieldname]=field;this.el.append(wrap);}
       this.primary=document.createElement('button');this.primary.textContent=options.primary_action_label||'Close';this.primary.addEventListener('click',()=>{const values={};for(const [key,f] of Object.entries(this.fields_dict)){if(f.input){if(f.df.reqd&&!f.input.value)return;values[key]=f.input.value;}}if(options.primary_action)options.primary_action(values);else this.hide();});this.el.append(this.primary);
      }
      get_value(key){return this.fields_dict[key].input.value;}set_value(key,value){this.fields_dict[key].input.value=value;}get_primary_btn(){return $(this.primary);}show(){document.body.append(this.el);}hide(){this.el.remove();}
     }}};
   }, JSON.parse(fs.readFileSync(path.join(apps,'sports_app/sports_app/registration_fields.json'),'utf8')));
   await page.addScriptTag({path:path.join(apps,'sports_app/sports_app/public/js/registrations.js')});
   await page.evaluate(async()=>{window.view=frappe.boost_console_views['sports_app:registrations']();await view.mount({container:document.getElementById('host'),signal:new AbortController().signal});});
   assert.equal(await page.locator('.ing-console-table').count(),1);
   assert.equal(await page.getByRole('heading',{name:'Enrollments',exact:true}).count(),1);
   await page.getByRole('button',{name:'Sort by Player',exact:true}).click();
   assert.equal(await page.evaluate(()=>calls.filter(c=>c.action==='list_registrations').at(-1).args.sort_by),'full_name');
   await page.getByRole('button',{name:'Actions for enrollment REG-READ',exact:true}).click();
   assert.deepEqual(await page.locator('.sports-registration-menu.is-open [role=menuitem]').allTextContents(),['View']);
   await page.keyboard.press('Escape');
   await page.getByRole('button',{name:'Actions for enrollment REG-1',exact:true}).focus();await page.keyboard.press('ArrowDown');
   assert.deepEqual(await page.locator('.sports-registration-menu.is-open [role=menuitem]').allTextContents(),['View','Accept enrollment','Reject enrollment']);
   const box=await page.locator('.sports-registration-menu.is-open .dropdown-menu').boundingBox();assert(box.x>=0&&box.x+box.width<=width+1);
   await page.keyboard.press('Enter');
   await page.getByRole('dialog').waitFor();assert.match(await page.getByRole('dialog').innerText(),/Sample Player/);
   for(const heading of ['Application summary','Admission review','Billing and payment','Player details','Parent / guardian','Emergency contact (if different)','Consent choices']) assert.equal(await page.getByRole('heading',{name:heading,exact:true}).count(),1,heading);
   const columns=await page.locator('.sports-enrollment-profile .enrollment-grid').first().evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').length);
   assert.equal(columns,width>640?2:1);
   assert.equal(await page.locator('.sports-enrollment-profile .enrollment-field').filter({hasText:'Photo and video permission recorded'}).locator('dd').innerText(),'No');
   assert.equal(await page.locator('.sports-enrollment-profile').evaluate(el=>el.scrollWidth<=el.clientWidth),true);
   await page.getByRole('dialog').screenshot({path:`/tmp/sports-enrollment-review-${width}.png`});
   assert.equal(await page.locator('.ing-console-table').count(),1,'View must retain underlying list');
   await page.evaluate(()=>document.querySelector('.modal-fixture').remove());
   await page.getByRole('button',{name:'Actions for enrollment REG-1',exact:true}).click();
   await page.getByRole('menuitem',{name:'Accept enrollment',exact:true}).click();
   await page.getByRole('dialog').waitFor();assert.match(await page.getByRole('dialog').innerText(),/Possible Match/);
   assert.equal(await page.evaluate(()=>calls.filter(c=>c.action==='accept_registration').length),0,'opening menu/dialog must not accept');
   await page.getByRole('button',{name:'Accept and create player',exact:true}).click();
   await page.waitForFunction(()=>records[0].status==='Accepted'&&document.querySelector('[role=dialog]')?.innerText.includes('Accepted'));
   assert.equal(await page.getByRole('button',{name:'Actions for enrollment REG-1',exact:true}).count(),0,'accepted row leaves pending list');
   await page.evaluate(()=>document.querySelector('.modal-fixture').remove());
   await page.getByLabel('Enrollment status',{exact:true}).selectOption('Accepted');
   await page.getByRole('button',{name:'Actions for enrollment REG-1',exact:true}).click();
   assert.deepEqual(await page.locator('.sports-registration-menu.is-open [role=menuitem]').allTextContents(),['View']);
   await page.getByLabel('Enrollment status',{exact:true}).selectOption('Pending');
   // Simulate a concurrent acceptance after list rendering; no stale review dialog.
   await page.evaluate(()=>{records[1].can_review=true;});await page.getByRole('button',{name:'Refresh enrollments'}).click();
   await page.evaluate(()=>{records[1].status='Accepted';records[1].can_review=false;});
   await page.getByRole('button',{name:'Actions for enrollment REG-READ',exact:true}).click();
   await page.getByRole('menuitem',{name:'Accept enrollment',exact:true}).click();
   await page.waitForFunction(()=>messages.length===1);assert.equal(await page.getByRole('dialog').count(),0);
   // Reject path still requires a reason and an explicit confirmation.
   await page.evaluate(()=>{records[1].status='Pending';records[1].can_review=true;});await page.getByRole('button',{name:'Refresh enrollments'}).click();
   await page.getByRole('button',{name:'Actions for enrollment REG-READ',exact:true}).click();await page.getByRole('menuitem',{name:'Reject enrollment',exact:true}).click();
   await page.getByRole('button',{name:'Reject enrollment',exact:true}).click();
   assert.equal(await page.evaluate(()=>calls.filter(c=>c.action==='reject_registration').length),0);
   await page.getByLabel('Reason',{exact:true}).fill('Not eligible for selected pathway');await page.getByRole('button',{name:'Reject enrollment',exact:true}).click();
   await page.waitForFunction(()=>records[1].status==='Rejected');
   assert.equal(await page.evaluate(()=>calls.filter(c=>c.action==='reject_registration').at(-1).args.reason),'Not eligible for selected pathway');
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   await page.evaluate(()=>view.unmount());assert.equal(await page.getByRole('dialog').count(),0);assert.deepEqual(errors,[]);
   await page.close();
  }
  console.log('PASS desktop/phone registration view: invoice CSS, reference menu, keyboard/viewport, modal View, permission/status gating, explicit Accept/Reject with matches/reason, stale record guard, list refresh/sort and unmount cleanup (Dialog/API stubbed)');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

/* Private Sports relationship workspace; logging does not send correspondence. */
frappe.provide("frappe.boost_console_views");
frappe.boost_console_views["sports_app:relations"] = () => {
 let host,signal,company,kind="Sports Organization",search="",rating="",country="",emailOnly=false,relationship="",sortBy="",sortOrder="asc",start=0,generation=0;
 const dialogs=new Set();
 const call=async(method,args={})=>(await frappe.call({method:`sports_app.relations_api.${method}`,args})).message;
 const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
 const button=(text,action,primary=false)=>{const b=node('button',__(text),`btn btn-sm btn-${primary?'primary':'default'}`);b.type='button';b.addEventListener('click',action,{signal});return b;};
 function open(doctype,name){
  const route=`/app/${frappe.router.slug(doctype)}/${name?encodeURIComponent(name):'new'}${name?'':'?company='+encodeURIComponent(company)}`;
  const dialog=new frappe.ui.Dialog({title:__(name?"Relationship record":"New relationship record"),size:'extra-large',fields:[{fieldtype:'HTML',fieldname:'form'}],primary_action_label:__('Open Full View'),primary_action:()=>window.open(route,'_blank','noopener')});
  const frame=node('iframe',null,'ing-console-preview');frame.title=__(doctype);frame.src=route;frame.style.width='100%';frame.style.height='70vh';
  dialog.fields_dict.form.$wrapper.empty().append(frame);dialog.$wrapper.on('hidden.bs.modal',()=>{dialogs.delete(dialog);if(!signal.aborted)render();});dialogs.add(dialog);dialog.show();
 }
 async function render(){
  const token=++generation;const data=await call('list_records',{doctype:kind,company,search,rating,country,start,has_email:emailOnly?1:0,relationship,sort_by:sortBy,sort_order:sortOrder});
  if(signal.aborted||token!==generation)return;company=data.company;sortBy=data.sort_by||sortBy;host.replaceChildren();
  host.append(node('h3',__('Clubs & Partners')),node('p',__('Private relationship directory, opportunities and correspondence logs. Ratings are staff-assessed priority, not club performance. Logging never sends email or shares player information. Published emails are not delivery-tested or confirmed recruitment contacts.'),'text-muted'));
  const tabs=node('div');tabs.style.cssText='display:flex;flex-wrap:wrap;gap:8px;margin:12px 0';
  for(const [dt,label]of[['Sports Organization','Organizations'],['Sports Opportunity','Opportunities'],['Sports Interaction','Correspondence']])tabs.append(button(label,()=>{kind=dt;search="";rating="";country="";relationship="";emailOnly=false;sortBy="";sortOrder="asc";start=0;render();},kind===dt));host.append(tabs);
  const filters=node('div');filters.style.cssText='display:flex;flex-wrap:wrap;gap:8px;margin:12px 0';
  const input=node('input',null,'form-control');input.type='search';const searchLabel=kind==='Sports Organization'?'Organization or email':'Search records';input.placeholder=__(searchLabel);input.setAttribute('aria-label',__(searchLabel));input.value=search;input.style.maxWidth='280px';input.addEventListener('change',()=>{search=input.value;start=0;render();},{signal});filters.append(input);
  if(kind==='Sports Organization'){
   for(const [label,values,current,update]of[['Priority',['All priorities','Unrated','1','2','3','4','5'],rating,v=>rating=v],['Country',['All countries',...(data.countries||[])],country,v=>country=v],['Relationship',['All relationships','Prospect','Contacted','Active','Paused','Closed'],relationship,v=>relationship=v]]){
    const select=node('select',null,'form-control');select.style.width='auto';select.setAttribute('aria-label',__(label));for(const [i,value]of values.entries()){const option=node('option',__(value));option.value=i?value:'';select.append(option);}select.value=current;select.addEventListener('change',()=>{update(select.value);start=0;render();},{signal});filters.append(select);
   }
  }
  if(kind==='Sports Organization'){
   const label=node('label');label.style.cssText='display:flex;align-items:center;gap:6px;margin:0';const check=node('input');check.type='checkbox';check.checked=emailOnly;check.addEventListener('change',()=>{emailOnly=check.checked;start=0;render();},{signal});label.append(check,document.createTextNode(__('With email only')));filters.append(label);
  }
  filters.append(button('Search',()=>{search=input.value;start=0;render();}),button('Clear filters',()=>{search='';rating='';country='';relationship='';emailOnly=false;start=0;render();}),button('New record',()=>open(kind,null),true),button('Refresh',render));host.append(filters);
  if(!data.rows.length)host.append(node('p',__('No matching relationship records.')));
  const wrap=node('div',null,'ing-console-table-wrap');wrap.style.cssText='max-width:100%;overflow-x:auto';wrap.tabIndex=0;wrap.setAttribute('role','region');wrap.setAttribute('aria-label',__('Relationship records table'));
  const table=node('table',null,'table table-bordered ing-console-table');table.style.minWidth=kind==='Sports Organization'?'1050px':'700px';table.style.width='100%';
  const headers=kind==='Sports Organization'?['Organization','Country','Sport','Priority','Relationship','Public email','Email purpose','Action']:kind==='Sports Opportunity'?['Opportunity','Organization','Type','Status','Next follow-up','Action']:['Subject','Organization','Type','Occurred on','Next follow-up','Action'];
  const sortFields=kind==='Sports Organization'?['organization_name','country','sport','priority_rating','relationship_status','public_email','email_purpose']:kind==='Sports Opportunity'?['title',null,'opportunity_type','status','next_follow_up']:['subject',null,'interaction_type','occurred_on','next_follow_up'];
  const head=node('thead'),headRow=node('tr');for(const [index,label]of headers.entries()){
   const th=node('th');th.scope='col';const field=sortFields[index];
   if(field){const active=sortBy===field;th.setAttribute('aria-sort',active?(sortOrder==='asc'?'ascending':'descending'):'none');
    const control=button(label+(active?(sortOrder==='asc'?' ↑':' ↓'):' ↕'),()=>{sortOrder=sortBy===field&&sortOrder==='asc'?'desc':'asc';sortBy=field;start=0;render();});
    control.title=__('Sort by ')+__(label);control.setAttribute('aria-label',__('Sort by ')+__(label));control.style.cssText='font:inherit;color:inherit;background:transparent;border:0;padding:0;text-align:left;white-space:nowrap';th.append(control);
   }else th.textContent=__(label);headRow.append(th);
  }head.append(headRow);table.append(head);
  const body=node('tbody');
  const webLink=(label,url)=>{if(!/^https?:\/\//i.test(url||''))return node('span',__(label));const a=node('a',__(label));a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;};
  for(const r of data.rows){const row=node('tr');const values=kind==='Sports Organization'?[r.organization_name,r.country,r.sport,r.priority_rating,r.relationship_status]:kind==='Sports Opportunity'?[r.title,r.organization_label||r.organization,r.opportunity_type,r.status,r.next_follow_up]:[r.subject,r.organization_label||r.organization,r.interaction_type,r.occurred_on,r.next_follow_up];
   for(const [i,value]of values.entries()){const td=node('td',value||'—');if(i===0&&kind==='Sports Organization'&&r.team_category){const detail=node('small',r.team_category,'text-muted');detail.style.display='block';td.append(detail);}row.append(td);}
   if(kind==='Sports Organization'){
    const email=node('td');
    if(r.public_email){const a=node('a',r.public_email);a.href='mailto:'+r.public_email;email.append(a);if(r.email_source_url){const source=node('small');source.style.display='block';source.append(webLink('Published source',r.email_source_url),document.createTextNode(r.email_checked_on?' · '+r.email_checked_on:''));email.append(source);}}
    else{email.append(node('span',__('Not published / not yet sourced'),'text-muted'));if(r.contact_page){const p=node('div');p.append(webLink('Contact page',r.contact_page));email.append(p);}}
    if(r.contact_notes&&!r.contact_notes.startsWith('Published business address;')){const note=node('small',r.contact_notes,'text-muted');note.style.cssText='display:block;max-width:300px';email.append(note);}
    row.append(email,node('td',r.email_purpose||'—'));
   }
   const action=node('td');action.append(button('View / edit',()=>open(kind,r.name)));row.append(action);for(const [i,cell]of [...row.cells].entries()){cell.style.cssText='padding:10px 12px;white-space:normal;vertical-align:top;min-width:90px';if(i===0)cell.style.minWidth='180px';if(kind==='Sports Organization'&&i===5)cell.style.minWidth='260px';}body.append(row);
  }table.append(body);wrap.append(table);host.append(wrap);
  const pager=node('div');pager.style.cssText='display:flex;gap:8px;margin-top:16px';if(start)pager.append(button('Previous',()=>{start=Math.max(0,start-30);render();}));if(data.has_more)pager.append(button('Next',()=>{start+=30;render();}));host.append(pager);
 }
 return {async mount(options){host=options.container;signal=options.signal;company=options.context.company;await render();},unmount(){generation++;for(const d of dialogs)d.hide();dialogs.clear();}};
};

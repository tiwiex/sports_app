/* Sports-owned sidebar presentation; no changes to Boost routing or permissions. */
(() => {
 if (window.__sportsConsoleNavigation) return;
 window.__sportsConsoleNavigation = true;
 const style = document.createElement('style');
 style.textContent = `
 .sports-console-navigation .ing-console-nav-group{border-radius:8px;padding:6px;border:1px solid rgba(191,219,254,.22)}
 .sports-console-navigation .ing-console-nav-group-title{padding:10px 12px;border-radius:6px;font-weight:800;letter-spacing:.04em;line-height:1.4;margin-bottom:6px}
 .sports-console-navigation .sports-nav-extension{background:rgba(6,78,59,.3);border-color:rgba(110,231,183,.65)}
 .sports-console-navigation .sports-nav-extension .ing-console-nav-group-title{background:#065f46;color:#ecfdf5;box-shadow:inset 4px 0 #6ee7b7}
 .sports-console-navigation .sports-nav-boost{background:rgba(30,64,175,.1);border-color:rgba(147,197,253,.55)}
 .sports-console-navigation .sports-nav-boost>.ing-console-nav-group-title{background:#1e40af;color:#eff6ff;box-shadow:inset 4px 0 #93c5fd}
 .sports-console-navigation .sports-boost-sections{padding:4px 4px 4px 12px}
 .sports-console-navigation .sports-boost-sections[hidden]{display:none}
 .sports-console-navigation .sports-nav-core{border:0;background:transparent;box-shadow:none;padding:0}
 .sports-console-navigation .sports-nav-core .ing-console-nav-group-title{background:transparent;color:#bfdbfe;box-shadow:none;font-size:.75rem;padding:8px 10px;margin-bottom:2px;letter-spacing:.02em}
 .sports-console-navigation .ing-console-nav-items{margin-left:12px;padding-left:8px;border-left:1px solid rgba(191,219,254,.4)}
 .sports-console-navigation .ing-console-nav-item{padding-left:16px;line-height:1.5}
 .sports-console-navigation .sports-nav-extension .ing-console-nav-item{color:#ecfdf5}
 .sports-console-navigation .sports-nav-extension .ing-console-nav-item.is-active{background:#d1fae5;color:#064e3b;box-shadow:inset 3px 0 #10b981}
 .sports-console-navigation .ing-console-nav-group-title:focus-visible,.sports-console-navigation .ing-console-nav-item:focus-visible{outline:2px solid #facc15;outline-offset:2px}
 `;
 document.head.append(style);
 let boostExpanded = true;
 function arrange() {
  for (const menu of document.querySelectorAll('.ing-console-nav-groups')) {
   let boost = menu.querySelector(':scope > .sports-nav-boost');
   const nested = boost?.querySelector('.sports-boost-sections');
   const groups = [...menu.children].flatMap(el => el === boost ? [...nested.children] : [el]).filter(el => el.classList.contains('ing-console-nav-group'));
   const keys = el => [...el.querySelectorAll('[data-view]')].map(item => String(item.dataset.view));
   const sports = groups.filter(el => keys(el).some(key => key.startsWith('sports_app:')));
   if (!sports.length) {
    if (boost) { for (const group of [...nested.children]) menu.insertBefore(group,boost); boost.remove(); }
    menu.classList.remove('sports-console-navigation');
    groups.forEach(el => el.classList.remove('sports-nav-extension','sports-nav-core'));
    continue;
   }
   const core = groups.filter(el => !keys(el).some(key => key.includes(':')));
   menu.classList.add('sports-console-navigation');
   for (const group of groups) {
    group.classList.toggle('sports-nav-extension', sports.includes(group));
    group.classList.toggle('sports-nav-core', core.includes(group));
   }
   // Stable provider order; move existing nodes to retain host handlers/state.
   let anchor = menu.firstElementChild;
   for (const group of sports) {
    if (group !== anchor) menu.insertBefore(group,anchor);
    anchor = group.nextElementSibling;
   }
   if (core.length) {
    if (!boost) {
     boost = document.createElement('section'); boost.className = 'ing-console-nav-group sports-nav-boost';
     const button = document.createElement('button'); button.type = 'button'; button.className = 'ing-console-nav-group-title'; button.dataset.sportsBoostToggle = '1';
     const label = document.createElement('span'); label.textContent = typeof window.__ === 'function' ? window.__('Boost') : 'Boost';
     const caret = document.createElement('span'); caret.className = 'ing-console-nav-caret'; caret.setAttribute('aria-hidden','true');
     const content = document.createElement('div'); content.className = 'sports-boost-sections';
     const toggle = () => { button.setAttribute('aria-expanded',String(boostExpanded)); caret.textContent = boostExpanded ? '−' : '+'; content.hidden = !boostExpanded; };
     button.addEventListener('click',() => { boostExpanded = !boostExpanded; toggle(); });
     button.append(label,caret); boost.append(button,content); toggle(); menu.append(boost);
    }
    const content = boost.querySelector('.sports-boost-sections');
    for (const group of core) if (group.parentElement !== content) content.append(group);
   } else if (boost) boost.remove();
  }
 }
 let scheduled = false;
 function schedule() {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { scheduled = false; arrange(); });
 }
 const relevant = node => node.nodeType === 1 && (node.matches('.ing-console-nav-groups') || node.closest('.ing-console-nav-groups') || node.querySelector('.ing-console-nav-groups'));
 const start = () => {
  new MutationObserver(records => {
   if (records.some(record => relevant(record.target) || [...record.addedNodes,...record.removedNodes].some(relevant))) schedule();
  }).observe(document.body,{childList:true,subtree:true});
  schedule();
 };
 if (document.body) start();
 else document.addEventListener('DOMContentLoaded',start,{once:true});
})();

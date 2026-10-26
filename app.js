var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Mobile menu
var burger=document.getElementById('burger'),links=document.getElementById('navLinks');
if(burger){
  burger.addEventListener('click',function(){var o=links.classList.toggle('open');burger.setAttribute('aria-expanded',o);});
  links.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){links.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
}

// Nav solid on scroll + parallax band
var nav=document.getElementById('nav'),pbg=document.getElementById('parallaxBg'),ticking=false;
function onScroll(){
  nav.classList.toggle('scrolled',window.scrollY>40);
  if(!reduce&&pbg){var r=pbg.parentElement.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight){pbg.style.transform='translate3d(0,'+((r.top-innerHeight/2)*-0.16)+'px,0)';}}
  ticking=false;
}
window.addEventListener('scroll',function(){if(!ticking){requestAnimationFrame(onScroll);ticking=true;}},{passive:true});
onScroll();

// Open now badge from their real hours (Mon to Fri 8am to 4.30pm, NZ time)
(function(){
  var badges=document.querySelectorAll('[data-open-badge]');if(!badges.length)return;
  try{
    var parts=new Intl.DateTimeFormat('en-NZ',{timeZone:'Pacific/Auckland',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());
    var get=function(t){var p=parts.find(function(x){return x.type===t;});return p?p.value:'';};
    var day=get('weekday'),mins=(+get('hour')%24)*60+(+get('minute'));
    var weekday=['Mon','Tue','Wed','Thu','Fri'].indexOf(day)>-1,open=weekday&&mins>=480&&mins<990;
    var text=open?'Open now':(weekday&&mins<480?'Opens 8am today':(day==='Fri'||day==='Sat'||day==='Sun'?'Opens Monday 8am':'Opens 8am tomorrow'));
    badges.forEach(function(b){b.textContent=text;b.classList.toggle('is-open',open);b.hidden=false;});
  }catch(e){}
})();

// Count-up
function fmt(n){return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g,',');}
function countUp(el){
  var end=+el.getAttribute('data-count'),dec=+(el.getAttribute('data-dec')||0);
  if(reduce){el.textContent=dec?end.toFixed(dec):fmt(end);return;}
  var t0=null;
  function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/1600,1),v=end*(1-Math.pow(1-p,3));el.textContent=dec?v.toFixed(dec):fmt(Math.round(v));if(p<1)requestAnimationFrame(step);}
  requestAnimationFrame(step);
}

// Scroll reveals, staggered within each parent
document.querySelectorAll('.reveal').forEach(function(el){if(el.querySelector('img'))el.classList.remove('reveal');});
var targets=document.querySelectorAll('.reveal');
if('IntersectionObserver' in window&&!reduce){
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting)return;
      var el=e.target,sibs=Array.prototype.filter.call(el.parentElement.children,function(c){return c.matches('.reveal,.wipe,.wipe-up');});
      var d=(Math.min(6,Math.max(0,sibs.indexOf(el)))*0.08)+'s',img=el.querySelector(':scope>img');
      if(img){img.style.transitionDelay=d+',0s';img.addEventListener('transitionend',function(){img.style.transitionDelay='';},{once:true});}
      else{el.style.transitionDelay=d;}
      el.classList.add('in');
      el.querySelectorAll('[data-count]').forEach(countUp);
      io.unobserve(el);
    });
  },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  targets.forEach(function(el){io.observe(el);});
}else{
  targets.forEach(function(el){el.classList.add('in');});
  document.querySelectorAll('[data-count]').forEach(countUp);
}

// Gallery lightbox
var lb=document.getElementById('lightbox');
if(lb&&lb.showModal){
  var lbImg=lb.querySelector('img'),lbCap=lb.querySelector('p');
  document.querySelectorAll('.masonry figure').forEach(function(f){
    f.setAttribute('tabindex','0');f.setAttribute('role','button');
    function open(){var i=f.querySelector('img');lbImg.src=i.getAttribute('data-full')||i.currentSrc||i.src;lbImg.alt=i.alt;lbCap.textContent=(f.querySelector('figcaption')||{}).textContent||'';lb.showModal();}
    f.addEventListener('click',open);
    f.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open();}});
  });
  lb.querySelector('button').addEventListener('click',function(){lb.close();});
  lb.addEventListener('click',function(e){if(e.target===lb)lb.close();});
}

var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();

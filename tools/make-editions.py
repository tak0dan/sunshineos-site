#!/usr/bin/env python3
"""Generates the "All editions" subpages (editions/index.html and uk/editions/index.html) from the look of the main pages:
the same <style>, header and footer are taken from index.html and uk/index.html, so a design change on the main page shows up here
after re-running this script. The content comes from editions.json (what each edition is, its screenshots) and release.json
(the builds), both read by the page in the browser: a new edition needs only an entry in editions.json and a release.
usage: python3 tools/make-editions.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent

L = {
 "en": {"title": "All editions", "intro": "Sunshine OS comes in editions. An edition is a line of the distribution; the channel says how finished a build is.",
        "chan": "<b>Release</b> is tested and safe to install. <b>Beta</b> is close to release and open for testing. <b>Testing</b> is experimental and can break.",
        "main": "Main edition", "download": "Download", "sha": "SHA-256", "builds": "Builds", "none": "No build of this edition has been published yet.",
        "warn": "Not a release: it can break. Do not install it on a machine you rely on.", "back": "Back to the main page", "load": "Loading the editions…",
        "fail": "The list of editions could not be loaded.", "all": "All files", "desc": "All editions of Sunshine OS with screenshots and downloads.", "x": "GB", "mb": "MB",
        "lang": "uk", "home": "../", "assets": "../assets/", "data": "../", "switch": "../uk/editions/", "nav_end": "Install"},
 "uk": {"title": "Усі збірки", "intro": "Sunshine OS має кілька збірок. Збірка — це окрема гілка дистрибутива; канал показує, наскільки готова конкретна версія.",
        "chan": "<b>Release</b> — перевірена, її безпечно встановлювати. <b>Beta</b> — близька до релізу, відкрита для тестування. <b>Testing</b> — експериментальна й може ламатися.",
        "main": "Основна збірка", "download": "Завантажити", "sha": "SHA-256", "builds": "Версії", "none": "Для цієї збірки ще нічого не опубліковано.",
        "warn": "Це не реліз: вона може ламатися. Не встановлюйте її на комп'ютер, на який покладаєтеся.", "back": "На головну сторінку", "load": "Завантажуємо збірки…",
        "fail": "Не вдалося завантажити список збірок.", "all": "Усі файли", "desc": "Усі збірки Sunshine OS зі знімками екрана й завантаженнями.", "x": "ГБ", "mb": "МБ",
        "lang": "en", "home": "../", "assets": "../../assets/", "data": "../../", "switch": "../../editions/", "nav_end": "Встановити"},
}

def build(code):
    t = L[code]
    src = (root / ("index.html" if code == "en" else "uk/index.html")).read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", src, re.S).group(0)
    header = re.search(r"<header class=\"nav\".*?</header>", src, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
    fonts = re.search(r"<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">.*?rel=\"stylesheet\">", src, re.S).group(0)
    themescript = re.search(r"<script>\ntry\{var t=localStorage.*?</script>", src, re.S).group(0)
    def fix(h):
        h = re.sub(r'(href|src)="(?:\.\./)?assets/', lambda m: '%s="%s' % (m.group(1), t["assets"]), h)
        h = h.replace('href="#', 'href="../#')
        h = h.replace('class="nav" id="nav"', 'class="nav solid" id="nav"')
        h = h.replace('href="uk/" hreflang="uk"', 'href="%s" hreflang="uk"' % t["switch"]) if code == "en" else h.replace('href="../" hreflang="en"', 'href="%s" hreflang="en"' % t["switch"])
        return h
    header, footer = fix(header), fix(footer)
    footer = re.sub(r"<canvas id=\"fpx\"[^>]*></canvas>", "", footer)
    page = f'''<!doctype html>
<html lang="{'en' if code == 'en' else 'uk'}" data-theme="sunrise">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t["title"]} · Sunshine OS</title>
<meta name="description" content="{t["desc"]}">
<meta property="og:site_name" content="Sunshine OS">
<meta property="og:title" content="{t["title"]} · Sunshine OS">
<meta name="theme-color" content="#0e0a1a">
<link rel="icon" type="image/png" href="{t["assets"]}favicon.png">
{fonts}
{themescript}
{style}
<style>
.ed{{border-top:1px solid var(--border-subtle);padding:40px 0}}
.ed:first-of-type{{border-top:0}}
.ed h2{{display:flex;flex-wrap:wrap;align-items:center;gap:12px;font-size:28px;font-weight:600;letter-spacing:-.02em}}
.chip{{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;font-weight:500;padding:3px 10px;border:1px solid var(--border-strong);color:var(--text-secondary)}}
.chip.main{{background:var(--brand);color:var(--brand-ink);border-color:var(--brand)}}
.chip.Testing,.chip.Beta{{border-color:color-mix(in srgb,var(--brand) 60%,transparent);color:var(--brand)}}
.ed .tg{{margin-top:8px;color:var(--text);font-size:16px}}
.ed .ab{{margin-top:12px;max-width:46rem;color:var(--text-secondary);font-size:15px;line-height:1.7}}
.ed .wr{{margin-top:12px;max-width:46rem;font-size:14px;color:var(--text-secondary);border-left:2px solid var(--brand);padding-left:12px}}
.ed .shots{{margin-top:24px}}
.bl{{list-style:none;margin:24px 0 0;padding:0;border-top:1px solid var(--border-subtle)}}
.bl li{{display:grid;gap:12px;padding:16px 0;border-bottom:1px solid var(--border-subtle);align-items:center}}
@media(min-width:768px){{.bl li{{grid-template-columns:1fr auto}}}}
.bl .mt{{font-size:13px;color:var(--text-muted,var(--text-secondary))}}
.bl .mt code{{font-size:12px}}
.intro{{max-width:46rem;color:var(--text-secondary);font-size:16px;line-height:1.7}}
.intro+.intro{{margin-top:12px}}
.back{{display:inline-block;margin-bottom:24px;color:var(--text-secondary);font-size:14px}}
</style>
</head>
<body>
{header}
<main id="main">
<div class="inner">
  <a class="back" href="{t["home"]}#install">&larr; {t["back"]}</a>
  <h1 class="h" style="font-size:36px;font-weight:600;letter-spacing:-.03em">{t["title"]}</h1>
  <p class="intro" style="margin-top:16px">{t["intro"]}</p>
  <p class="intro">{t["chan"]}</p>
  <div id="eds" style="margin-top:32px"><p class="intro">{t["load"]}</p></div>
</div>
</main>
{footer}
<script>
(function(){{
"use strict";
var LANG="{code}",D="{t["data"]}",A="{t["assets"]}";
var T={{download:"{t["download"]}",sha:"{t["sha"]}",none:"{t["none"]}",warn:"{t["warn"]}",main:"{t["main"]}",builds:"{t["builds"]},",fail:"{t["fail"]}",gb:" {t["x"]}",mb:" {t["mb"]}",all:"{t["all"]}"}};
var $=function(s){{return document.querySelector(s)}},$$=function(s){{return Array.prototype.slice.call(document.querySelectorAll(s))}};
function esc(s){{return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;")}}
function mb(n){{return n>1e9?(n/1e9).toFixed(2)+T.gb:Math.round(n/1e6)+T.mb}}
function fd(s){{try{{return new Date(s).toLocaleDateString(LANG==="uk"?"uk":"en",{{year:"numeric",month:"long",day:"numeric"}})}}catch(e){{return s}}}}
/* theme: same choice as on the main page */
var themes=["sunrise","noon","ember","dusk","midnight"],ti=0;
function setTheme(t){{ti=themes.indexOf(t);document.documentElement.dataset.theme=t;try{{localStorage.setItem("sunshine-theme",t)}}catch(e){{}}}}
var saved=null;try{{saved=localStorage.getItem("sunshine-theme")}}catch(e){{}}
setTheme(themes.indexOf(saved)>-1?saved:"sunrise");
function next(){{setTheme(themes[(ti+1)%themes.length])}}
if($("#cycle"))$("#cycle").onclick=next;if($("#cycle2"))$("#cycle2").onclick=next;
$("#menub").onclick=function(){{var o=$("#menu").classList.toggle("open");this.setAttribute("aria-expanded",o)}};
/* editions: what they are (editions.json) + their builds (release.json) */
function link(r){{return (!r.edition||r.edition==="Sol")&&r.channel==="Release"?r.url:r.url+"?edition="+encodeURIComponent(r.edition||"Sol")+"&channel="+encodeURIComponent(r.channel)}}
Promise.all([fetch(D+"editions.json",{{cache:"no-cache"}}).then(function(r){{return r.json()}}),fetch(D+"release.json",{{cache:"no-cache"}}).then(function(r){{return r.json()}})])
.then(function(x){{
  var eds=x[0].editions||[],rels=(x[1].releases||[]).filter(function(r){{return r.url&&(r.parts||[]).length}}),out="";
  eds.forEach(function(e){{
    var mine=rels.filter(function(r){{return (r.edition||"Sol")===e.name}});
    mine.sort(function(a,b){{return String(b.date).localeCompare(String(a.date))||String(b.version).localeCompare(String(a.version),undefined,{{numeric:true}})}});
    var seen={{}},list=mine.filter(function(r){{if(seen[r.channel])return false;seen[r.channel]=1;return true}});
    var order={{Release:0,Beta:1,Testing:2}};list.sort(function(a,b){{return order[a.channel]-order[b.channel]}});
    var tx=function(o){{return o&&(o[LANG]||o.en)||""}};
    var shots=(e.screenshots||[]).map(function(s){{return '<figure class="shot"><img src="'+esc(D+s.src)+'" alt="'+esc(e.name+": "+tx(s.caption))+'" loading="lazy"><figcaption><b>'+esc(tx(s.caption))+'</b><span>'+esc(e.name)+'</span></figcaption></figure>'}}).join("");
    var builds=list.length?list.map(function(r,i){{
      var sz=r.parts.reduce(function(a,p){{return a+(p.size||0)}},0);
      return '<li><div><strong>'+esc(e.name)+" "+esc(r.version)+'</strong> <span class="chip '+esc(r.channel)+'">'+esc(r.channel)+'</span><div class="mt">'+esc(fd(r.date))+" · "+esc(mb(sz))+" · "+T.sha+' <span title="'+esc(r.sha256)+'">'+esc((r.sha256||"").slice(0,12))+'…</span><br><code>'+esc(r.file)+'</code></div></div>'+
        '<a class="btn '+(i===0?"primary":"secondary")+'" href="'+esc(link(r))+'"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20.25 14.75V20.25H3.75V14.75M12 3.75L12 14M8.5 11.5L12 15L15.5 11.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"/></svg>'+T.download+'</a></li>'}}).join(""):'<li><span class="mt">'+T.none+'</span></li>';
    var testing=!list.some(function(r){{return r.channel==="Release"}});
    out+='<section class="ed" id="'+esc(e.name.toLowerCase())+'"><h2>'+esc(e.name)+(e.main?' <span class="chip main">'+T.main+'</span>':"")+'</h2><p class="tg">'+esc(tx(e.tagline))+'</p><p class="ab">'+esc(tx(e.about))+'</p>'+
      (testing&&list.length?'<p class="wr">'+T.warn+'</p>':"")+(shots?'<div class="shots">'+shots+'</div>':"")+'<ul class="bl">'+builds+'</ul></section>';
  }});
  $("#eds").innerHTML=out;
  if(location.hash){{var t=document.getElementById(location.hash.slice(1));if(t)t.scrollIntoView()}}
}}).catch(function(){{$("#eds").innerHTML='<p class="intro">'+T.fail+'</p>'}});
}})();
</script>
</body>
</html>
'''
    out = root / ("editions" if code == "en" else "uk/editions")
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print("wrote", out / "index.html", len(page), "bytes")

for c in ("en", "uk"):
    build(c)

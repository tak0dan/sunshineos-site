#!/usr/bin/env python3
"""Writes release.json from the releases of the Sunshine OS repository on GitHub, so nobody has to edit it after a release.

For every release that carries ISO parts (SunshineOS[-Edition]_<version>_<Release|Beta|Testing>_<date>.iso.partN) it lists the parts with their
sizes and the SHA-256 from the release's .sha256 file. The Cloudflare Worker (ISO download) and the download button of the website read this file.
Entries can also be DECLARED by hand in releases/declared.json (an ISO hosted anywhere, no GitHub Release needed); see docs in the Sunshine OS
repository: docs/RELEASING.md.
usage: gen-release-json.py [release.json]      env: GH_REPO (default tak0dan/SunshineOS), GITHUB_TOKEN (optional, raises the API limit),
                                                    DOWNLOAD_URL (the Worker address), DECLARED (path of the declaration file)"""
import json, os, re, sys, urllib.request

REPO = os.environ.get("GH_REPO", "tak0dan/SunshineOS")
DL = os.environ.get("DOWNLOAD_URL", "https://sunshineos-download.sunshineos.workers.dev/")
out = sys.argv[1] if len(sys.argv) > 1 else "release.json"
NAME = re.compile(r"^SunshineOS(?:-(?P<ed>[A-Za-z]+))?_(?P<ver>[0-9.]+)_(?P<ch>Release|Beta|Testing)_(?P<day>\d{4}-\d{2}-\d{2})\.iso$")

DECLARED = os.environ.get("DECLARED", "releases/declared.json")

def head_size(url):
    """Size in bytes of the file behind url (follows redirects); GitHub and most hosts answer HEAD with Content-Length."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "sunshineos-release-json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        n = r.headers.get("Content-Length")
    if not n: raise ValueError("no Content-Length from " + url)
    return int(n)

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": "sunshineos-release-json", "Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN") and "api.github.com" in url:
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    return b if binary else json.loads(b)

releases, page = [], 1
while True:
    chunk = get(f"https://api.github.com/repos/{REPO}/releases?per_page=100&page={page}")
    if not chunk: break
    releases += chunk; page += 1
    if len(chunk) < 100: break

entries = []
for r in releases:
    if r.get("draft"): continue
    parts = sorted((a for a in r.get("assets", []) if re.search(r"\.iso\.part\d+$", a["name"])),
                   key=lambda a: int(re.search(r"part(\d+)$", a["name"]).group(1)))
    if not parts: continue
    iso = re.sub(r"\.part\d+$", "", parts[0]["name"]); m = NAME.match(iso)
    if not m: continue
    sha = ""
    for a in r["assets"]:
        if a["name"] == iso + ".sha256":
            try: sha = get(a["browser_download_url"], True).decode().split()[0]
            except Exception as e: print("no checksum for", iso, e, file=sys.stderr)
    entries.append({"version": m["ver"], "edition": m["ed"] or "Sol", "channel": m["ch"], "date": m["day"], "tag": r["tag_name"], "file": iso,
                    "size": sum(a["size"] for a in parts), "sha256": sha, "url": DL,
                    "parts": [{"url": a["browser_download_url"], "size": a["size"]} for a in parts]})
# ---- declared entries: an ISO hosted anywhere, listed by writing it into releases/declared.json
#   { "releases": [ { "file": "SunshineOS_13.4.7.1.7_Release_2026-12-01.iso",        (required; same naming scheme as the others)
#                     "parts": ["https://host/x.iso.part1", "https://host/x.iso.part2"],   (required; one URL when the ISO is a single file)
#                     "sha256": "...",  or  "sha256_url": "https://host/x.iso.sha256",     (optional)
#                     "link": "https://host/page-about-this-release" } ] }                (optional: the page "All files" opens)
# Sizes are read from the hosts. An entry that cannot be read is skipped with a warning; it never breaks the others.
declared = []
if os.path.exists(DECLARED):
    try: declared = json.load(open(DECLARED)).get("releases", [])
    except Exception as e: print("releases/declared.json unreadable:", e, file=sys.stderr)
have = {e["file"] for e in entries}
for d in declared:
    try:
        iso = d["file"]; m = NAME.match(iso)
        if not m: raise ValueError("file name does not follow SunshineOS[-Edition]_<version>_<Release|Beta|Testing>_<date>.iso")
        urls = d["parts"]
        if isinstance(urls, str): urls = [urls]
        if not urls or not all(u.startswith("https://") for u in urls): raise ValueError("parts must be https URLs")
        sizes = [head_size(u) for u in urls]
        sha = d.get("sha256", "")
        if not sha and d.get("sha256_url"): sha = get(d["sha256_url"], True).decode().split()[0]
        if sha and not re.fullmatch(r"[0-9a-fA-F]{64}", sha): raise ValueError("sha256 is not 64 hex digits")
        if iso in have: print("declared entry", iso, "ignored: a GitHub release with that file name exists", file=sys.stderr); continue
        e = {"version": m["ver"], "edition": m["ed"] or "Sol", "channel": m["ch"], "date": m["day"], "tag": d.get("tag", ""), "file": iso,
             "size": sum(sizes), "sha256": sha.lower(), "url": DL, "parts": [{"url": u, "size": n} for u, n in zip(urls, sizes)]}
        if d.get("link"): e["link"] = d["link"]
        entries.append(e)
    except Exception as ex:
        print("declared entry skipped:", d.get("file", "?"), "-", ex, file=sys.stderr)
entries.sort(key=lambda e: (e["date"], [int(x) for x in e["version"].split(".")]), reverse=True)
if not entries: sys.exit("no release with ISO parts found: release.json left unchanged")
text = json.dumps({"releases": entries}, indent=2) + "\n"
if not os.path.exists(out) or open(out).read() != text:
    open(out, "w").write(text); print("release.json updated:", len(entries), "releases, newest", entries[0]["file"])
else:
    print("release.json already up to date")

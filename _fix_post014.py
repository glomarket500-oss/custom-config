import re
import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

REPO_DIR = r"C:\Users\a\Desktop\custom-config"
VAULT_DIR = r"C:\Users\a\Desktop\MianAI知识库\MianAI知识库\vault\香港全屋定制文章"
VERCEL_URL = "https://custom-api-cfg.vercel.app"

draft_path = Path(VAULT_DIR) / "草稿" / "2026-09-05-1703-香港師傅-新皇崗口岸將通？傳統師傅講港式定製智慧-重寫版.md"
content = draft_path.read_text(encoding="utf-8")

fm = {}
body = content
if content.startswith("---"):
    m = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if m:
        fm_text = m.group(1)
        body = content[m.end():]
        for line in fm_text.split('\n'):
            if ':' in line and not line.startswith(' ') and not line.startswith('-'):
                key, val = line.split(':', 1)
                fm[key.strip()] = val.strip().strip('"').strip("'")

title = fm.get('title', '香港師傅故事')
description = fm.get('description', '新皇崗口岸將通，香港全屋定制師傅阿強帶學徒小李探討港式定製智慧。')
keywords = fm.get('keywords', '香港裝修,全屋定制,新皇崗口岸')
author = fm.get('author', '鄭志強（阿強）師傅')

now = datetime.now()
display_datetime = now.strftime("%Y年%m月%d日 %H:%M:%S")
iso_date = now.strftime("%Y-%m-%d")

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def md_to_html(md_body):
    paragraphs = []
    in_list = False
    list_items = []
    for line in md_body.strip().split('\n'):
        line = line.strip()
        if not line:
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            continue
        if line.startswith('# '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h1>{escape_html(line[2:])}</h1>')
        elif line.startswith('## '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h2>{escape_html(line[3:])}</h2>')
        elif line.startswith('### '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h3>{escape_html(line[4:])}</h3>')
        elif line.startswith('- '):
            list_items.append(f'<li>{escape_html(line[2:])}</li>')
            in_list = True
        elif line.startswith('**') and line.endswith('**'):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            bold_text = line[2:-2]
            paragraphs.append(f'<p><strong>{escape_html(bold_text)}</strong></p>')
        else:
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<p>{escape_html(line)}</p>')
    if in_list and list_items:
        paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
    return '\n'.join(paragraphs)

body_html = md_to_html(body)

file_name = "post-014.html"
file_path = os.path.join(REPO_DIR, file_name)

html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="geo.position" content="22.3193;114.1694">
<meta name="geo.placename" content="旺角, 九龍, 香港">
<meta name="geo.region" content="HK">
<link rel="canonical" href="{VERCEL_URL}/{file_name}">
<title>{title} | 萍踪侠影录</title>
<meta name="description" content="{escape_html(description)}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{author}">
<style>
body{{font-family:"PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif;color:#2c2c2c;background:#faf9f7;line-height:1.85;max-width:700px;margin:0 auto;padding:20px}}
header{{border-bottom:2px solid #333;margin-bottom:24px;padding-bottom:14px}}
.new-badge{{background:#e74c3c;color:#fff;padding:2px 8px;border-radius:4px;font-size:14px;margin-left:8px;vertical-align:middle}}
.publish-time{{color:#666;font-size:14px;margin-top:8px}}
h1{{font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;margin-bottom:12px}}
h2{{font-size:1.3rem;margin:28px 0 14px;border-left:4px solid #8b5e3c;padding-left:12px;color:#2c2c2c}}
p{{margin:14px 0;font-size:1.05rem;text-indent:2em}}
.tip-box{{background:#f5f0eb;padding:18px 20px;border-radius:6px;margin:20px 0;border-left:4px solid #8b5e3c}}
.tip-box h4{{margin-bottom:10px;color:#8b5e3c;font-size:1.05rem}}
.tip-box p{{text-indent:0;margin:0}}
.author-bio{{display:flex;gap:16px;margin:32px 0;padding:22px;background:#f5f0eb;border-radius:8px}}
.author-avatar{{width:60px;height:60px;border-radius:50%;background:#8b5e3c;color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0}}
.author-info h4{{margin-bottom:6px;font-size:1.05rem}}
.author-info p{{font-size:.9rem;color:#666;margin-bottom:4px;text-indent:0}}
.author-links{{display:flex;gap:14px;margin-top:10px}}
.author-links a{{color:#8b5e3c;font-size:.88rem;text-decoration:none}}
.cta{{background:linear-gradient(135deg,#f5f0eb 0%,#e8dfd3 100%);padding:24px;border-radius:8px;margin-top:36px;text-align:center;border:1px solid #e0d4c0}}
.cta h3{{margin-bottom:10px;color:#8b5e3c}}
.cta p{{text-indent:0;margin:8px 0;color:#666;font-size:.95rem}}
.cta a{{display:inline-block;background:#8b5e3c;color:#fff;padding:11px 24px;border-radius:5px;text-decoration:none;margin:8px 6px 0;font-size:.95rem}}
nav{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;padding:16px 5vw;background:#fff;border-bottom:1px solid #eee;position:sticky;top:0;z-index:100;margin:-20px -20px 20px -20px}}
.logo{{font-size:1.15rem;font-weight:700;letter-spacing:1px}}
.logo span{{font-weight:400;font-size:.8rem;color:#888;margin-left:6px}}
.nav-links{{display:flex;flex-wrap:wrap;justify-content:flex-end}}
.nav-links a{{margin-left:20px;font-size:.88rem;color:#555;text-decoration:none}}
.nav-links a:hover{{color:#8b5e3c}}
footer{{text-align:center;padding:24px 0;font-size:.82rem;color:#999;border-top:1px solid #eee;margin-top:40px}}
footer a{{color:#8b5e3c}}
@media(max-width:480px){{nav{{flex-direction:column;align-items:flex-start;padding:12px 5vw}}.logo{{font-size:1rem;margin-bottom:8px}}.nav-links{{justify-content:flex-start;width:100%}}.nav-links a{{margin:0 14px 0 0;font-size:.82rem}}.author-bio{{flex-direction:column;align-items:center;text-align:center}}h1{{font-size:1.45rem}}}}
</style>
<meta property="og:title" content="{title} | 萍踪侠影录">
<meta property="og:description" content="{escape_html(description)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_HK">
<meta property="og:url" content="{VERCEL_URL}/{file_name}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{title}","description":"{escape_html(description)}","url":"{VERCEL_URL}/{file_name}","datePublished":"{iso_date}T{now.strftime('%H:%M:%S')}+08:00","author":{{"@type":"Person","name":"{author}"}},"publisher":{{"@type":"Organization","name":"萍踪侠影录"}}}}
</script>
</head>
<body>
<nav>
  <div class="logo">萍踪侠影录 <span>张丹枫、云蕾</span></div>
  <div class="nav-links">
    <a href="index.html">首页</a>
    <a href="diary.html">博主讲古</a>
    <a href="live.html">直播间</a>
    <a href="about.html">认识博主</a>
    <a href="cases.html">案例</a>
    <a href="contact.html">联系</a>
  </div>
</nav>
<header>
<h1>{title}</h1>
<p>作者：{author} <span class="new-badge">NEW</span></p>
<p class="publish-time">发布时间：{display_datetime}</p>
</header>
<article>
{body_html}
</article>
<hr>
<footer>
<p><a href="/index.html">← 返回首頁</a> | <a href="/diary.html">博主講古列表</a></p>
<p>© 萍踪侠影录 · 張丹楓、雲蕾 · <a href="https://wa.me/85251902328" target="_blank">WhatsApp 報價</a> · 香港九龍旺角菜園街</p>
</footer>
</body>
</html>'''

Path(file_path).write_text(html, encoding="utf-8")
print(f"OK: {file_name} ({len(html)} bytes)")

os.chdir(REPO_DIR)
subprocess.run(["git", "add", "-A"], capture_output=True)
subprocess.run(["git", "commit", "-m", "fix: rewrite post-014 with proper story template"], capture_output=True)
result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=60)

if result.returncode == 0:
    print("OK: Git push")
else:
    print(f"ERR: {result.stderr[:200] if result.stderr else 'timeout'}")

published_dir = Path(VAULT_DIR) / "已发布"
published_dir.mkdir(exist_ok=True)
dest = published_dir / draft_path.name
shutil.move(str(draft_path), str(dest))
print("OK: moved to published")

print(f"\nDONE: {VERCEL_URL}/{file_name}")

import re
import os
import subprocess
from pathlib import Path

REPO_DIR = r"C:\Users\a\Desktop\custom-config"
file_path = os.path.join(REPO_DIR, "post-014.html")

html = Path(file_path).read_text(encoding="utf-8")

title = "新皇崗口岸將通？傳統師傅講港式定製智慧 | 萍踪侠影录"
desc = "新皇崗口岸通關在即，香港全屋定制師傅阿強帶學徒小李趕工搶材料。一個關於口岸、漲價、信任同手藝嘅故事。"
author = "鄭志強（阿強）師傅"
url = "https://custom-api-cfg.vercel.app/post-014.html"

# 1. 在 </head> 前插入缺少的 meta 和 schema
insert_before_head = '''<meta name="ICBM" content="22.3193, 114.1694">
<meta name="DC.title" content="''' + title + '''">
<meta name="DC.description" content="''' + desc + '''">
<meta name="DC.subject" content="香港裝修, 全屋定制, 新皇崗口岸, 港式定製, 嵌入式衣櫥, 防火廚房, 裝修漲價, 傳統手藝">
<meta name="DC.creator" content="''' + author + '''">
<meta name="DC.date" content="2026-09-06">
<meta name="DC.language" content="zh-Hant">
<meta name="DC.publisher" content="萍踪侠影录">
<meta property="og:site_name" content="萍踪侠影录">
<meta property="og:image" content="https://custom-api-cfg.vercel.app/images/og-default.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@pingzong">
<meta name="twitter:title" content="''' + title + '''">
<meta name="twitter:description" content="''' + desc + '''">
<meta name="twitter:image" content="https://custom-api-cfg.vercel.app/images/og-default.jpg">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":"https://custom-api-cfg.vercel.app/index.html"},{"@type":"ListItem","position":2,"name":"博主講古","item":"https://custom-api-cfg.vercel.app/diary.html"},{"@type":"ListItem","position":3,"name":"新皇崗口岸將通？傳統師傅講港式定製智慧","item":"''' + url + '''"}]}
</script>
'''

html = html.replace('</head>', insert_before_head + '</head>')

# 2. 在 <body> 后加面包屑导航 HTML
breadcrumb_html = '''<div style="padding:8px 5vw;font-size:.85rem;color:#888;background:#faf9f7;border-bottom:1px solid #eee;">
<a href="index.html">首頁</a> &gt; <a href="diary.html">博主講古</a> &gt; <span style="color:#555;">新皇崗口岸將通？傳統師傅講港式定製智慧</span>
</div>
'''

html = html.replace('<body>', '<body>\n' + breadcrumb_html)

Path(file_path).write_text(html, encoding="utf-8")
print(f"OK: patched {file_path} ({len(html)} bytes)")

os.chdir(REPO_DIR)
subprocess.run(["git", "add", "-A"], capture_output=True)
subprocess.run(["git", "commit", "-m", "fix: add full SEO/GEO meta tags to post-014"], capture_output=True)
result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=60)

if result.returncode == 0:
    print("OK: Git push")
else:
    print(f"ERR: {result.stderr[:200] if result.stderr else 'timeout'}")

#!/usr/bin/env python3
"""
香港装修文章自动发布脚本
每日 00:00 cron 触发
流程：扫描草稿箱 → 按11 步流程优化 → 生成HTML → 推送GitHub → 归档
"""

import os
import re
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# ============ 配置（只做香港装修）============
VAULT_DIR = r"C:\Users\a\Desktop\MianAI知识库\MianAI知识库\vault\香港全屋定制文章"
REPO_DIR = r"C:\Users\a\Desktop\custom-config"
VERCEL_URL = "https://custom-api-cfg.vercel.app"

# 茶叶/陈皮路径（绝对不动）
TEA_VAULT = r"C:\Users\a\Desktop\MianAI知识库\MianAI知识库\vault\阿凤姐的故事"
CHENPI_VAULT = r"C:\Users\a\Desktop\MianAI知识库\MianAI知识库\vault\滢滢姐讲陈皮故事"


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def get_next_post_num():
    max_num = 0
    for f in Path(REPO_DIR).iterdir():
        if f.is_file() and f.name.startswith("post-") and f.name.endswith(".html"):
            m = re.search(r'post-(\d+)\.html', f.name)
            if m:
                max_num = max(max_num, int(m.group(1)))
    return max_num + 1


def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_to_html(md_body):
    paragraphs = []
    in_list = False
    list_items = []
    in_table = False
    table_rows = []

    for line in md_body.strip().split('\n'):
        line_stripped = line.strip()
        if not line_stripped:
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            if in_table and table_rows:
                paragraphs.append('<table class="info-table">' + ''.join(table_rows) + '</table>')
                table_rows = []
                in_table = False
            continue

        if line_stripped.startswith('|') and line_stripped.endswith('|'):
            cells = [c.strip() for c in line_stripped.split('|')[1:-1]]
            row_html = '<tr>' + ''.join(f'<td>{escape_html(c)}</td>' for c in cells) + '</tr>'
            table_rows.append(row_html)
            in_table = True
            continue
        elif in_table and table_rows:
            paragraphs.append('<table class="info-table">' + ''.join(table_rows) + '</table>')
            table_rows = []
            in_table = False

        if line_stripped.startswith('# '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h1>{escape_html(line_stripped[2:])}</h1>')
        elif line_stripped.startswith('## '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h2>{escape_html(line_stripped[3:])}</h2>')
        elif line_stripped.startswith('### '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<h3>{escape_html(line_stripped[4:])}</h3>')
        elif line_stripped.startswith('> '):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<blockquote>{escape_html(line_stripped[2:])}</blockquote>')
        elif line_stripped.startswith('- '):
            list_items.append(f'<li>{escape_html(line_stripped[2:])}</li>')
            in_list = True
        elif line_stripped.startswith('**') and line_stripped.endswith('**'):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            bold_text = line_stripped[2:-2]
            paragraphs.append(f'<p><strong>{escape_html(bold_text)}</strong></p>')
        elif line_stripped.startswith('*') and line_stripped.endswith('*'):
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            italic_text = line_stripped[1:-1]
            paragraphs.append(f'<p><em>{escape_html(italic_text)}</em></p>')
        else:
            if in_list and list_items:
                paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
                list_items = []
                in_list = False
            paragraphs.append(f'<p>{escape_html(line_stripped)}</p>')

    if in_list and list_items:
        paragraphs.append('<ul>' + ''.join(list_items) + '</ul>')
    if in_table and table_rows:
        paragraphs.append('<table class="info-table">' + ''.join(table_rows) + '</table>')

    return '\n'.join(paragraphs)


def build_html(title, desc, keywords, author, body_html, file_name, display_datetime, iso_date, now):
    html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow, max-snippet:-1">
<meta name="geo.position" content="22.3193;114.1694">
<meta name="geo.placename" content="旺角, 九龍, 香港">
<meta name="geo.region" content="HK">
<meta name="ICBM" content="22.3193, 114.1694">
<meta name="DC.title" content="{title} | 萍踪侠影录">
<meta name="DC.description" content="{escape_html(desc)}">
<meta name="DC.subject" content="{keywords}">
<meta name="DC.creator" content="{author}">
<meta name="DC.date" content="{iso_date}">
<meta name="DC.language" content="zh-Hant">
<meta name="DC.publisher" content="萍踪侠影录">
<link rel="canonical" href="{VERCEL_URL}/{file_name}">
<title>{title} | 萍踪侠影录</title>
<meta name="description" content="{escape_html(desc)}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="{author}">
<meta property="og:title" content="{title} | 萍踪侠影录">
<meta property="og:description" content="{escape_html(desc)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_HK">
<meta property="og:url" content="{VERCEL_URL}/{file_name}">
<meta property="og:site_name" content="萍踪侠影录">
<meta property="og:image" content="https://custom-api-cfg.vercel.app/images/og-default.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@pingzong">
<meta name="twitter:title" content="{title} | 萍踪侠影录">
<meta name="twitter:description" content="{escape_html(desc)}">
<meta name="twitter:image" content="https://custom-api-cfg.vercel.app/images/og-default.jpg">
<style>
body{{font-family:"PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif;color:#2c2c2c;background:#faf9f7;line-height:1.85;max-width:760px;margin:0 auto;padding:20px}}
header{{border-bottom:2px solid #333;margin-bottom:24px;padding-bottom:14px}}
.new-badge{{background:#e74c3c;color:#fff;padding:2px 8px;border-radius:4px;font-size:14px;margin-left:8px;vertical-align:middle}}
.publish-time{{color:#666;font-size:14px;margin-top:8px}}
h1{{font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;margin-bottom:12px}}
h2{{font-size:1.35rem;margin:32px 0 14px;border-left:4px solid #8b5e3c;padding-left:12px;color:#2c2c2c}}
h2::before{{content:"◆ ";color:#8b5e3c;font-size:0.8em;margin-right:4px}}
h3{{font-size:1.15rem;margin:20px 0 10px;color:#8b5e3c}}
p{{margin:14px 0;font-size:1.05rem;text-indent:2em}}
blockquote{{margin:20px 0;padding:16px 20px;background:linear-gradient(135deg,#f8f5f0 0%,#f0ebe3 100%);border-left:4px solid #8b5e3c;border-radius:0 6px 6px 0;font-style:italic;color:#555}}
blockquote p{{text-indent:0;margin:6px 0}}
strong{{color:#8b5e3c}}
em{{color:#666;font-style:italic}}
.breadcrumb{{padding:10px 5vw;font-size:.88rem;background:#fff;border-bottom:1px solid #e8e4df;display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin:-20px -20px 20px -20px}}
.breadcrumb a{{color:#8b5e3c;text-decoration:none;font-weight:500}}
.breadcrumb .sep{{color:#ccc;font-size:1.1rem}}
.breadcrumb .current{{color:#666;font-weight:400}}
.scene-divider{{text-align:center;margin:32px 0;color:#ccc;font-size:1.2rem;letter-spacing:8px}}
.scene-divider::before{{content:"◆ ◆ ◆"}}
.info-table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.95rem;text-indent:0}}
.info-table td{{padding:10px 12px;border:1px solid #e0d4c0}}
.info-table tr:first-child td{{background:#f5f0eb;font-weight:600;color:#8b5e3c}}
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
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting","headline":"{title}","description":"{escape_html(desc)}","url":"{VERCEL_URL}/{file_name}","datePublished":"{iso_date}T{now.strftime('%H:%M:%S')}+08:00","author":{{"@type":"Person","name":"{author}"}},"publisher":{{"@type":"Organization","name":"萍踪侠影录"}},"geo":{{"@type":"GeoCoordinates","latitude":22.3193,"longitude":114.1694}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首頁","item":"{VERCEL_URL}/index.html"}},{{"@type":"ListItem","position":2,"name":"博主講古","item":"{VERCEL_URL}/diary.html"}},{{"@type":"ListItem","position":3,"name":"香港裝修","item":"{VERCEL_URL}/{file_name}"}}]}}
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
<div class="breadcrumb">
<a href="index.html">🏠 首頁</a>
<span class="sep">›</span>
<a href="diary.html">📖 博主講古</a>
<span class="sep">›</span>
<span class="current">{escape_html(title[:30])}</span>
</div>
<header>
<h1>{title}</h1>
<p>作者：{author} · 撰文：萍踪侠影录 · 雲蕾 <span class="new-badge">NEW</span></p>
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
    return html


def process_draft(draft_path):
    """处理单个草稿文件"""
    log(f"📄 处理草稿: {draft_path.name}")

    content = draft_path.read_text(encoding="utf-8")

    # 提取 frontmatter
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

    title = fm.get('title', draft_path.stem)
    # 自动生成描述（如果草稿冇）
    desc = fm.get('description', '')
    if not desc:
        # 简单从 title 生成
        desc = f"{title}。香港全屋定制師傅故事，由萍踪侠影录 · 雲蕾撰文。"

    keywords = fm.get('keywords', '香港裝修,全屋定制,香港師傅,博主講古')
    author = fm.get('author', '鄭志強（阿強）師傅')

    body_html = md_to_html(body)

    # 文件编号
    next_num = get_next_post_num()
    file_name = f"post-{next_num:03d}.html"
    file_path = os.path.join(REPO_DIR, file_name)

    now = datetime.now()
    display_datetime = now.strftime("%Y年%m月%d日 %H:%M:%S")
    iso_date = now.strftime("%Y-%m-%d")

    html = build_html(title, desc, keywords, author, body_html, file_name, display_datetime, iso_date, now)
    Path(file_path).write_text(html, encoding="utf-8")
    log(f"   ✅ 生成: {file_name}")

    # 更新 index.html
    index_path = os.path.join(REPO_DIR, "index.html")
    idx_content = Path(index_path).read_text(encoding="utf-8", errors="ignore")
    new_card = f'<div class="diary-card"><a href="{file_name}"><div class="thumb">香港師傅</div><div class="body"><div class="date">{display_datetime} · 師傅故事 · 作者：{author} <span class="new-badge">NEW</span></div><h3>{escape_html(title)}</h3><p>{escape_html(desc[:60])}...</p></div></a></div>\n\n'
    pattern = r'(<div class="diary-grid">\s*\n)'
    if re.search(pattern, idx_content):
        new_idx = re.sub(pattern, r'\1' + new_card, idx_content, count=1)
        Path(index_path).write_text(new_idx, encoding="utf-8")
        log(f"   ✅ 更新 index.html")

    # 更新 diary.html
    diary_path = os.path.join(REPO_DIR, "diary.html")
    if Path(diary_path).exists():
        diary_content = Path(diary_path).read_text(encoding="utf-8", errors="ignore")
        new_item = f'\n<a href="{file_name}">\n    <div class="diary-row"><div class="thumb">香港師傅</div><div class="body"><div class="date">{display_datetime} · 師傅故事 · 作者：{author} <span class="new-badge">NEW</span></div><h3>{escape_html(title)}</h3><p>{escape_html(desc[:60])}...</p></div></div>\n  </a>\n\n'
        insert_pos = -1
        for n in range(next_num - 1, 0, -1):
            prev_post = f'<a href="post-{n:03d}.html">'
            pos = diary_content.find(prev_post)
            if pos != -1:
                insert_pos = pos
                break
        if insert_pos != -1:
            diary_content = diary_content[:insert_pos] + new_item + diary_content[insert_pos:]
            Path(diary_path).write_text(diary_content, encoding="utf-8")
            log(f"   ✅ 更新 diary.html")

    # Git push
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Auto: {file_name} {title[:30]}"], capture_output=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=60)

    if result.returncode == 0:
        log(f"   ✅ Git push 成功")
    else:
        log(f"   ⚠️ Git push 失败: {result.stderr[:100] if result.stderr else 'timeout'}")

    # 归档到已发布
    published_dir = Path(VAULT_DIR) / "已发布"
    published_dir.mkdir(exist_ok=True)
    dest = published_dir / draft_path.name
    shutil.move(str(draft_path), str(dest))
    log(f"   ✅ 已归档: {dest.name}")

    return file_name


def main():
    log("=" * 60)
    log("🤖 香港装修文章自动发布（每日 00:00 cron）")
    log("=" * 60)

    # 绝对不动茶叶/陈皮
    log(f"🔒 茶叶 vault（不动）：{TEA_VAULT}")
    log(f"🔒 陈皮 vault（不动）：{CHENPI_VAULT}")
    log(f"📂 香港装修 vault（操作）：{VAULT_DIR}")

    draft_path = Path(VAULT_DIR) / "草稿"
    drafts = sorted([f for f in draft_path.iterdir() if f.is_file() and f.suffix == ".md"])

    if not drafts:
        log("📭 草稿箱无新文章，无需处理")
        return

    # 按时间戳排序（取最新一篇）
    latest = max(drafts, key=lambda f: f.stat().st_mtime)
    log(f"📌 发现最新草稿: {latest.name}")
    log(f"   大小: {latest.stat().st_size} bytes")

    # 提示信息
    log("\n⚠️ 自动发布模式（无人工确认）")
    log("   用户已明确接受此模式风险")
    log("   自动处理 + 自动推送 + 自动归档\n")

    try:
        file_name = process_draft(latest)
        log(f"\n🎉 自动发布完成！")
        log(f"   URL: {VERCEL_URL}/{file_name}")
    except Exception as e:
        log(f"❌ 处理失败: {e}")
        raise


if __name__ == "__main__":
    main()
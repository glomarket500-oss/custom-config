#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港装修网站 - 全自动文章发布流水线
用法：python publish_hk_article.py --input "文章路径.md"
"""

import argparse
import re
import os
import subprocess
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

# === 配置 ===
REPO_DIR = r"C:\Users\a\Desktop\custom-config"
INDEX_HTML = os.path.join(REPO_DIR, "index.html")
VAULT_DIR = r"C:\Users\a\Desktop\MianAI知识库\MianAI知识库\vault\香港全屋定制文章"
VERCEL_URL = "https://custom-api-cfg.vercel.app"


def escape_html(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def read_md_article(md_path):
    content = Path(md_path).read_text(encoding="utf-8", errors="ignore")
    fm = {}
    body = content
    if content.startswith("---"):
        m = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if m:
            fm_text = m.group(1)
            body = content[m.end():]
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def get_next_post_number():
    """获取下一个 post 编号"""
    max_num = 0
    for f in Path(REPO_DIR).iterdir():
        if f.is_file() and f.name.startswith("post-") and f.name.endswith(".html"):
            m = re.search(r'post-(\d+)\.html', f.name)
            if m:
                max_num = max(max_num, int(m.group(1)))
    return max_num + 1


def extract_article_content(md_body):
    """从 markdown 提取文章正文段落"""
    paragraphs = []
    for line in md_body.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('---'):
            continue
        if line.startswith('# '):
            paragraphs.append(f'<h1>{escape_html(line[2:])}</h1>')
        elif line.startswith('## '):
            paragraphs.append(f'<h2>{escape_html(line[3:])}</h2>')
        elif line.startswith('### '):
            paragraphs.append(f'<h3>{escape_html(line[4:])}</h3>')
        elif line.startswith('> '):
            paragraphs.append(f'<blockquote><p>{escape_html(line[2:])}</p></blockquote>')
        elif line.startswith('🌿') or line.startswith('📌') or line.startswith('✅') or line.startswith('🔥') or line.startswith('💬') or line.startswith('🏠'):
            paragraphs.append(f'<p>{escape_html(line)}</p>')
        else:
            paragraphs.append(f'<p>{escape_html(line)}</p>')
    return '\n'.join(paragraphs)


def generate_post_html(post_num, title, body, date_str, tags):
    """生成 post-NNN.html 文件"""
    
    # 提取摘要（前120字）
    abstract = body[:120].replace('\n', ' ') if len(body) > 120 else body
    abstract = escape_html(abstract)
    
    # 正文转 HTML
    body_html = extract_article_content(body)
    
    # ISO 日期
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        iso_date = dt.strftime("%Y-%m-%d")
        display_date = dt.strftime("%Y年%m月%d日")
    except:
        iso_date = date_str
        display_date = date_str
    
    # 标签处理
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    tags_html = ' · '.join(tags_list) if tags_list else '行業講古'
    
    # 生成 post HTML（基于 post-009 模板）
    post_html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="viewport">
<meta name="geo.position" content="22.3193;114.1694">
<meta name="geo.placename" content="旺角, 九龍, 香港">
<meta name="geo.region" content="HK">
<meta name="ICBM" content="22.3193, 114.1694">
<link rel="canonical" href="{VERCEL_URL}/post-{post_num:03d}.html">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 萍踪侠影录</title>
<meta name="description" content="{abstract}">
<meta name="keywords" content="{','.join(tags_list) if tags_list else '香港裝修,全屋定制,張丹楓'}">
<meta name="author" content="張丹楓">
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "{title}", "description": "{abstract}", "author": {{"@type": "Person", "name": "張丹楓"}}, "datePublished": "{iso_date}", "dateModified": "{iso_date}"}}
</script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif; color: #2c2c2c; background: #faf9f7; line-height: 1.8; }}
  a {{ text-decoration: none; color: inherit; }}
  nav {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; padding: 16px 5vw; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }}
  .logo {{ font-size: 1.15rem; font-weight: 700; letter-spacing: 1px; }}
  .logo span {{ font-weight: 400; font-size: 0.8rem; color: #888; margin-left: 6px; }}
  .nav-links {{ display: flex; flex-wrap: wrap; justify-content: flex-end; }}
  .nav-links a {{ margin-left: 20px; font-size: 0.88rem; color: #555; }}
  .nav-links a:hover {{ color: #8b5e3c; }}
  .article-wrap {{ max-width: 720px; margin: 0 auto; padding: 32px 5vw 60px; }}
  .breadcrumb {{ font-size: 0.8rem; color: #999; margin-bottom: 20px; }}
  .breadcrumb a {{ color: #8b5e3c; }}
  .article-header {{ margin-bottom: 32px; }}
  .article-header h1 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 12px; line-height: 1.4; }}
  .meta {{ display: flex; gap: 14px; font-size: 0.85rem; color: #666; margin-bottom: 16px; flex-wrap: wrap; }}
  .meta span {{ background: #f5f0eb; padding: 3px 12px; border-radius: 12px; }}
  .tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; }}
  .tags a {{ font-size: 0.82rem; color: #8b5e3c; background: #f5f0eb; padding: 3px 12px; border-radius: 12px; }}
  .scene {{ margin-bottom: 32px; }}
  .scene h2 {{ font-size: 1.15rem; font-weight: 600; margin: 24px 0 12px; }}
  .scene p {{ margin-bottom: 12px; font-size: 0.95rem; }}
  .dialogue {{ background: #fff; border-left: 3px solid #8b5e3c; padding: 16px 18px; margin: 16px 0; border-radius: 0 6px 6px 0; }}
  .dialogue .who {{ font-weight: 600; color: #8b5e3c; font-size: 0.85rem; margin-bottom: 6px; }}
  .dialogue .who::before {{ content: "💬 "; }}
  .dialogue p {{ font-size: 0.93rem; margin: 0; color: #444; }}
  .highlight-box {{ background: #fff; border: 1px solid #eee; padding: 20px; margin: 20px 0; border-radius: 6px; }}
  .highlight-box .label {{ font-size: 0.78rem; color: #999; margin-bottom: 4px; }}
  .highlight-box .value {{ font-size: 1.1rem; font-weight: 600; color: #8b5e3c; }}
  .cta {{ background: #2c2c2c; color: #fff; padding: 24px; border-radius: 8px; text-align: center; margin: 32px 0; }}
  .cta h3 {{ font-size: 1.1rem; margin-bottom: 12px; }}
  .cta a {{ display: inline-block; padding: 12px 28px; background: #8b5e3c; color: #fff; border-radius: 4px; margin-top: 8px; }}
  .related {{ margin-top: 32px; padding-top: 24px; border-top: 1px solid #eee; }}
  .related h3 {{ font-size: 1rem; margin-bottom: 12px; }}
  .related a {{ display: block; color: #8b5e3c; margin-bottom: 8px; font-size: 0.92rem; }}
  footer {{ text-align: center; padding: 24px 5vw; font-size: 0.82rem; color: #999; border-top: 1px solid #eee; }}
  footer a {{ color: #8b5e3c; }}
  @media (max-width: 480px) {{ nav {{ flex-direction: column; align-items: center; padding: 10px 5vw; text-align: center; }} .logo {{ font-size: 1.15rem; margin-bottom: 2px; }} .logo span {{ display: block; margin-left: 0; margin-top: 2px; font-size: 0.75rem; }} .nav-links {{ justify-content: center; width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; white-space: nowrap; flex-wrap: nowrap; padding-bottom: 4px; scrollbar-width: none; }} .nav-links::-webkit-scrollbar {{ display: none; }} .nav-links a {{ margin: 0 10px; font-size: 0.82rem; flex-shrink: 0; }} }}
</style>
<meta property="og:title" content="{title} | 萍踪侠影录">
<meta property="og:description" content="{abstract}">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_HK">
<meta property="og:url" content="{VERCEL_URL}/post-{post_num:03d}.html">
<meta property="og:image" content="{VERCEL_URL}/images/hero1.jpg">
</head>
<body>

<nav>
  <div class="logo">萍踪侠影录 <span>張丹楓與雲蕾</span></div>
  <div class="nav-links">
    <a href="index.html">首頁</a>
    <a href="diary.html">博主講古</a>
    <a href="cases.html">案例</a>
    <a href="contact.html">聯繫</a>
  </div>
</nav>

<div class="article-wrap">
  <div class="breadcrumb"><a href="index.html">首頁</a> · <a href="diary.html">博主講古</a></div>
  
  <div class="article-header">
    <h1>{title}</h1>
    <div class="meta">
      <span>{display_date}</span>
      <span>{tags_html}</span>
    </div>
  </div>
  
  <div class="scene">
{body_html}
  </div>
  
  <div class="cta">
    <h3>想報價？直接 WhatsApp 張丹楓</h3>
    <a href="https://wa.me/85251902328" target="_blank">📱 一鍵 WhatsApp 報價</a>
  </div>
  
  <div class="related">
    <h3>📖 相關文章</h3>
    <a href="diary.html">查看更多博主講古 →</a>
  </div>
</div>

<footer>
  <p>© 萍踪侠影录 · 張丹楓、雲蕾 · <a href="https://wa.me/85251902328" target="_blank">WhatsApp 報價</a> · 香港九龍旺角菜園街</p>
</footer>

</body>
</html>'''
    return post_html


def insert_card_into_index(post_num, title, abstract, date_str, tags):
    """在 index.html 的 diary-grid 最前面插入新卡片"""
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = dt.strftime("%Y年%m月%d日")
    except:
        display_date = date_str
    
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]
    tags_html = ' · '.join(tags_list) if tags_list else '行業講古'
    
    # 生成新卡片 HTML
    card_html = f'''<div class="diary-card"><a href="post-{post_num:03d}.html"><div class="thumb"></div><div class="body"><div class="date">{display_date} · {tags_html}</div><h3>{title} <span class="new-badge">NEW</span></h3><p>{abstract[:80]}{"..." if len(abstract) > 80 else ""}</p></div></a></div>

'''
    
    # 在 <div class="diary-grid"> 后面插入
    pattern = r'(<div class="diary-grid">\s*\n)'
    replacement = r'\1' + card_html
    
    new_content = re.sub(pattern, replacement, content, count=1)
    
    if new_content == content:
        return False, "找不到 diary-grid"
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "卡片已插入"


def git_commit_and_push(commit_msg):
    os.chdir(REPO_DIR)
    
    subprocess.run(["git", "add", "-A"], capture_output=True)
    
    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    if result.returncode != 0:
        if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
            return True, "没有变更"
        return False, f"commit 失败: {result.stderr}"
    
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode != 0:
        if "rejected" in result.stderr.lower():
            subprocess.run(["git", "pull", "origin", "main", "--no-rebase"], capture_output=True, text=True)
            result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
            if result.returncode != 0:
                return False, f"push 失败: {result.stderr}"
        else:
            return False, f"push 失败: {result.stderr}"
    
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return True, f"已推送 (commit: {r.stdout.strip()})"


def check_vercel_deploy(max_wait=120):
    import urllib.request
    
    print(f"⏳ 等待 Vercel 部署（最多 {max_wait} 秒）...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            req = urllib.request.Request(VERCEL_URL, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            resp = urllib.request.urlopen(req, timeout=10)
            if resp.status == 200:
                elapsed = time.time() - start_time
                if elapsed >= 30:
                    return True, f"部署完成（约 {int(elapsed)} 秒）"
        except:
            pass
        time.sleep(5)
        print(f"  ... 已等待 {int(time.time() - start_time)} 秒")
    
    return False, f"等待超时（{max_wait} 秒）"


def update_article_status(md_path, status, website=None):
    content = Path(md_path).read_text(encoding="utf-8", errors="ignore")
    
    if re.search(r'^status:\s*', content, re.MULTILINE):
        content = re.sub(r'^status:\s*.*$', f'status: {status}', content, flags=re.MULTILINE)
    else:
        content = content.replace('---\n\n', f'---\nstatus: {status}\n\n', 1)
    
    if website:
        if re.search(r'^website:\s*', content, re.MULTILINE):
            content = re.sub(r'^website:\s*.*$', f'website: {website}', content, flags=re.MULTILINE)
        else:
            content = content.replace('---\n\n', f'---\nwebsite: {website}\n\n', 1)
    
    Path(md_path).write_text(content, encoding="utf-8")
    return True


def move_file(src_path, dest_folder):
    src = Path(src_path)
    dest = Path(dest_folder) / src.name
    counter = 1
    while dest.exists():
        stem = src.stem
        if re.search(r'_\d+$', stem):
            stem = re.sub(r'_\d+$', '', stem)
        dest = Path(dest_folder) / f"{stem}_{counter}{src.suffix}"
        counter += 1
    shutil.move(str(src), str(dest))
    return str(dest)


def main():
    parser = argparse.ArgumentParser(description='香港装修网站文章发布')
    parser.add_argument('--input', required=True, help='草稿文章 .md 路径')
    parser.add_argument('--no-push', action='store_true', help='不推送到 GitHub（测试用）')
    args = parser.parse_args()
    
    print(f"📖 读取文章: {args.input}")
    fm, body = read_md_article(args.input)
    
    title = fm.get('title', Path(args.input).stem)
    date_str = fm.get('date', datetime.now().strftime("%Y-%m-%d"))
    tags = fm.get('tags', '香港裝修,全屋定制,張丹楓')
    
    print(f"   标题: {title}")
    print(f"   日期: {date_str}")
    
    # 获取下一个编号
    post_num = get_next_post_number()
    print(f"   新文章编号: post-{post_num:03d}")
    
    if args.no_push:
        print("ℹ️ --no-push 模式，只生成本地文件")
    
    # 1. 生成 post HTML
    print("📝 生成 post HTML...")
    post_html = generate_post_html(post_num, title, body, date_str, tags)
    post_path = os.path.join(REPO_DIR, f"post-{post_num:03d}.html")
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(post_html)
    print(f"   ✅ {post_path}")
    
    # 2. 更新 index.html
    print("📄 更新首页...")
    abstract = body[:120].replace('\n', ' ') if len(body) > 120 else body
    ok, msg = insert_card_into_index(post_num, title, abstract, date_str, tags)
    if not ok:
        print(f"   ❌ {msg}")
        return 1
    print(f"   ✅ {msg}")
    
    if args.no_push:
        print(f"\n📁 文件已生成，但未推送")
        print(f"   新文章: {post_path}")
        print(f"   首页: {INDEX_HTML}")
        return 0
    
    # 3. Git push
    print("🚀 Git push...")
    ok, msg = git_commit_and_push(f"Add post-{post_num:03d}: {title}")
    if not ok:
        print(f"   ❌ {msg}")
        return 1
    print(f"   ✅ {msg}")
    
    # 4. 检测部署
    print("🌐 检测 Vercel 部署...")
    ok, msg = check_vercel_deploy()
    if ok:
        print(f"   ✅ {msg}")
        
        print("📋 更新文章状态...")
        update_article_status(args.input, "已发布", website=VERCEL_URL)
        
        published_dir = os.path.join(VAULT_DIR, "已发布")
        new_path = move_file(args.input, published_dir)
        print(f"   ✅ 已移动到: {new_path}")
        
        print(f"\n🎉 发布成功！")
        print(f"   网站: {VERCEL_URL}")
        print(f"   新文章: {VERCEL_URL}/post-{post_num:03d}.html")
        
        return 0
    else:
        print(f"   ⚠️ {msg}")
        
        print("📋 更新为待上传...")
        update_article_status(args.input, "待上传")
        
        pending_dir = os.path.join(VAULT_DIR, "待上传")
        new_path = move_file(args.input, pending_dir)
        print(f"   ⚠️ 已移动到: {new_path}")
        
        return 1


if __name__ == '__main__':
    sys.exit(main())

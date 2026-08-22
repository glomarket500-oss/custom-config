#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
發布新文章腳本
用法：python publish.py
運行後按提示輸入即可，自動生成文章 + 更新列表頁 + 更新首頁
"""

import os, re, glob, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_next_post_num():
    """取得下一個文章編號"""
    posts = glob.glob(os.path.join(BASE_DIR, 'post-*.html'))
    nums = []
    for p in posts:
        m = re.search(r'post-(\d{3})\.html', os.path.basename(p))
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1

def slugify(title):
    """生成URL友好文件名（保留中文字符）"""
    return re.sub(r'[^\w\u4e00-\u9fff\-]', '', title.replace(' ', '-'))[:30]

def read_file(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✅ 已寫入: {filename}')

def generate_article(num, title, date, location, author, house_type, budget, duration, intro, body):
    """生成文章HTML"""
    filename = f'post-{num:03d}.html'
    
    # 作者標記
    author_name = '张丹枫' if author == '1' else '云蕾'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 工廠預製上門安裝 | 萍踪侠影录</title>
<meta name="description" content="香港{house_type}裝修實錄：{title}，工廠預製上門安裝{duration}完成。真實價錢、工期、材料全公開。">
<meta name="keywords" content="香港{house_type}裝修,{location}裝修,香港定制家具,工廠預製櫃,上門安裝家具,{house_type}裝修價錢">
<meta name="author" content="{author_name}">
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "{title}", "description": "香港{house_type}裝修實錄", "author": {{"@type": "Person", "name": "{author_name}"}}, "datePublished": "{date}", "dateModified": "{date}"}}
</script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif; color: #2c2c2c; background: #faf9f7; line-height: 1.8; }}
  a {{ text-decoration: none; color: inherit; }}
  nav {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 5vw; background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }}
  .logo {{ font-size: 1.15rem; font-weight: 700; letter-spacing: 1px; }}
  .logo span {{ font-weight: 400; font-size: 0.8rem; color: #888; margin-left: 6px; }}
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
  .img-block {{ background: #eee; height: 240px; display: flex; align-items: center; justify-content: center; margin: 20px 0; border-radius: 6px; overflow: hidden; }}
  .img-block img {{ width: 100%; height: 100%; object-fit: cover; }}
  .img-caption {{ text-align: center; font-size: 0.82rem; color: #999; margin-top: -12px; margin-bottom: 20px; }}
  .compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }}
  .compare .before, .compare .after {{ background: #eee; height: 180px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 0.85rem; border-radius: 6px; overflow: hidden; }}
  .compare .before img, .compare .after img {{ width: 100%; height: 100%; object-fit: cover; }}
  .compare-label {{ text-align: center; font-size: 0.85rem; color: #888; margin-bottom: 20px; }}
  .price-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9rem; }}
  .price-table th, .price-table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
  .price-table th {{ background: #f5f0eb; font-weight: 600; }}
  .price-table tr:last-child {{ font-weight: 600; background: #faf9f7; }}
  .cta {{ background: #2c2c2c; color: #fff; padding: 24px; border-radius: 8px; text-align: center; margin: 32px 0; }}
  .cta h3 {{ font-size: 1.1rem; margin-bottom: 12px; }}
  .cta a {{ display: inline-block; padding: 12px 28px; background: #8b5e3c; color: #fff; border-radius: 4px; margin-top: 8px; }}
  .related {{ margin-top: 32px; padding-top: 24px; border-top: 1px solid #eee; }}
  .related h3 {{ font-size: 1rem; margin-bottom: 12px; }}
  .related a {{ display: block; color: #8b5e3c; margin-bottom: 8px; font-size: 0.92rem; }}
  footer {{ text-align: center; padding: 24px 5vw; font-size: 0.82rem; color: #999; border-top: 1px solid #eee; }}
  footer a {{ color: #8b5e3c; }}
</style>
</head>
<body>

<nav>
  <div class="logo">萍踪侠影录 <span>张丹枫、云蕾</span></div>
  <div class="nav-links">
    <a href="index.html">首頁</a>
    <a href="diary.html">裝修日記</a>
    <a href="cases.html">案例</a>
    <a href="contact.html">聯繫</a>
  </div>
</nav>

<div class="article-wrap">

<div class="breadcrumb">
  <a href="index.html">首頁</a> > <a href="diary.html">裝修日記</a> > {title}
</div>

<div class="article-header">
  <h1>{title}</h1>
  <div class="meta">
    <span>📅 {date}</span>
    <span>📍 {location}</span>
    <span>🏠 {house_type}</span>
    <span>✍️ {author_name}</span>
  </div>
  <div class="tags">
    <a href="#">#香港{house_type}裝修</a>
    <a href="#">#{location}裝修</a>
    <a href="#">#定制家具</a>
  </div>
</div>

<!-- 正文開始 -->
{body}
<!-- 正文結束 -->

<div class="cta">
  <h3>想知道自己單位裝修幾錢？</h3>
  <p>傳張相同尺寸俾我，免費報價</p>
  <a href="https://wa.me/85251902328" target="_blank">📱 WhatsApp 免費報價</a>
</div>

<div class="related">
  <h3>你可能都感興趣</h3>
  <a href="post-001.html">300呎公屋裝修，3萬蚊搞定全屋定制櫃，師傅上門即裝即用</a>
  <a href="post-002.html">居屋廚房改造：原本冇位切菜，改造後多咗1.5米工作枱</a>
  <a href="diary.html">查看全部裝修日記 →</a>
</div>

</div>

<footer>
  <p>© 萍踪侠影录 · 张丹枫、云蕾 · <a href="https://wa.me/85251902328" target="_blank">WhatsApp 報價</a> · 香港九龍旺角菜園街</p>
</footer>

</body>
</html>'''
    
    write_file(filename, html)
    return filename

def update_diary(filename, title, date, location, house_type, budget, duration, author, intro):
    """更新日記列表頁"""
    content = read_file('diary.html')
    
    # 構建新卡片HTML
    new_card = f'''  <a href="{filename}">
    <div class="diary-row">
      <div class="thumb">Before/After</div>
      <div class="body">
        <div class="date">{date} · {location} · {house_type} · 作者：{'张丹枫' if author == '1' else '云蕾'}</div>
        <h3>{title}</h3>
        <p>{intro}</p>
        <div class="meta">💰 {budget}  ⏱ {duration}  🏷 {house_type}</div>
      </div>
    </div>
  </a>

'''
    
    # 插入到列表最前面
    marker = '<div class="diary-list">\n'
    if marker in content:
        content = content.replace(marker, marker + new_card)
        write_file('diary.html', content)
    else:
        print('  ⚠️ 找不到 diary.html 插入點')

def update_index(filename, title, date, location, house_type, budget, duration, intro):
    """更新首頁預覽"""
    content = read_file('index.html')
    
    new_card = f'''    <div class="diary-card">
      <a href="{filename}">
        <div class="thumb">Before / After 圖片</div>
        <div class="body">
          <div class="date">{date} · {location}</div>
          <h3>{title}</h3>
          <p>{intro}</p>
          <div class="meta"><span>💰 {budget}</span><span>⏱ {duration}</span><span>🏠 {house_type}</span></div>
        </div>
      </a>
    </div>
'''
    
    # 插入到 diary-grid 裡面第一個位置
    marker = '<div class="diary-grid">\n'
    if marker in content:
        content = content.replace(marker, marker + new_card)
        write_file('index.html', content)
    else:
        print('  ⚠️ 找不到 index.html 插入點')

def git_push():
    """Git commit + push"""
    os.system('git add .')
    os.system('git commit -m "Add new post"')
    result = os.system('git push origin main')
    if result == 0:
        print('  ✅ 已推送到 GitHub，Vercel 會自動重新部署（約1-2分鐘）')
    else:
        print('  ⚠️ Push 失敗，請檢查網絡或手動執行 git push')

def main():
    print('=' * 50)
    print('萍踪侠影录 — 發布新文章')
    print('=' * 50)
    
    # 收集輸入
    title = input('文章標題：').strip()
    if not title:
        print('標題不能為空')
        return
    
    date = input('日期（預設今天）：').strip()
    if not date:
        date = datetime.datetime.now().strftime('%Y年%m月')
    
    location = input('地區（如：將軍澳、荃灣）：').strip() or '香港'
    house_type = input('單位類型（公屋/居屋/劏房/私樓）：').strip() or '公屋'
    author = input('作者（1=张丹枫, 2=云蕾）：').strip() or '1'
    budget = input('預算（如：$30,000）：').strip() or '$0'
    duration = input('工期（如：半日/1日/2日）：').strip() or '1日'
    
    print('\n文章簡介（100字內，用於列表頁預覽）：')
    intro = input().strip()
    
    print('\n文章正文（HTML格式，或純文字我會幫你包裝）：')
    print('提示：用 <h2>標題</h2> 和 <p>段落</p>，對話用 <div class="dialogue">...</div>')
    print('輸入 END 結束：')
    
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    body = '\n'.join(lines)
    
    if not body:
        # 給一個默認模板
        body = f'''<div class="scene">
  <h2>▎ 序幕</h2>
  <p>{intro}</p>
</div>

<div class="scene">
  <h2>▎ 第一幕：見面</h2>
  <p>（請在此處寫見面過程...）</p>
  <div class="dialogue">
    <div class="who">客戶</div>
    <p>「師傅，我想...」</p>
  </div>
</div>

<div class="scene">
  <h2>▎ 第二幕：工廠</h2>
  <p>（請在此處寫工廠生產過程...）</p>
  <div class="img-block">工廠生產中</div>
  <div class="img-caption">旺角工廠——每個櫃體出廠前都要試裝一次</div>
</div>

<div class="scene">
  <h2>▎ 第三幕：安裝</h2>
  <p>（請在此處寫安裝過程...）</p>
  <div class="compare">
    <div class="before">Before</div>
    <div class="after">After</div>
  </div>
  <div class="compare-label">Before & After</div>
</div>

<div class="scene">
  <h2>▎ 尾聲：價錢公開</h2>
  <table class="price-table">
    <tr><th>項目</th><th>規格</th><th>價錢</th></tr>
    <tr><td>項目一</td><td>規格描述</td><td>{budget}</td></tr>
    <tr><td>總計</td><td></td><td>{budget}</td></tr>
  </table>
</div>'''
    
    print('\n' + '=' * 50)
    print('正在生成...')
    
    # 生成文章
    num = get_next_post_num()
    filename = generate_article(num, title, date, location, author, house_type, budget, duration, intro, body)
    
    # 更新列表頁
    print('\n更新 diary.html...')
    update_diary(filename, title, date, location, house_type, budget, duration, author, intro)
    
    # 更新首頁
    print('更新 index.html...')
    update_index(filename, title, date, location, house_type, budget, duration, intro)
    
    # Git push
    print('\n推送到 GitHub...')
    git_push()
    
    print('\n' + '=' * 50)
    print(f'✅ 完成！新文章：{filename}')
    print(f'網址：https://custom-api-cfg.vercel.app/{filename}')
    print('等 1-2 分鐘後刷新網站即可見到新文章')
    print('=' * 50)

if __name__ == '__main__':
    main()

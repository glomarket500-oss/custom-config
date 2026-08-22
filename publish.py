# publish.py - 鐧煎竷鏂拌淇棩瑷樻枃绔?# 鐢ㄦ硶锛歱ython publish.py
# 閬嬭寰屾寜鎻愮ず杓稿叆鍗冲彲

import os, re, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def slugify(title):
    """鐢熸垚URL鍙嬪ソ鐨勬枃浠跺悕"""
    return re.sub(r'[^\w\-]', '', title.replace(' ', '-'))[:30]

def generate_post_html(title, date, location, unit_type, cost, duration, tags, body):
    """鐢熸垚鍠瘒瑁濅慨鏃ヨHTML"""
    tags_html = '\n  '.join(f'<span>#{t}</span>' for t in tags.split(','))
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 宸ュ粻闋愯＝涓婇杸瀹夎 | 钀嶈釜渚犲奖褰?/title>
<meta name="description" content="{title}锛屽伐寤犻爯瑁戒笂闁€瀹夎锛岀湡瀵﹀児閷㈠叕闁?>
<meta name="author" content="钀嶅">
<meta property="og:title" content="{title}">
<meta property="og:description" content="棣欐腐瑁濅慨瀵﹂寗锛氬伐寤犻爯瑁姐€佷笂闁€瀹夎">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_HK">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "author": {{"@type": "Person", "name": "钀嶅"}},
  "datePublished": "{date}",
  "publisher": {{"@type": "Organization", "name": "钀嶈釜渚犲奖褰?}}
}}
</script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif;
    color: #2c2c2c; background: #faf9f7; line-height: 1.8;
  }}
  a {{ text-decoration: none; color: inherit; }}
  nav {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 5vw; background: #fff; border-bottom: 1px solid #eee;
    position: sticky; top: 0; z-index: 100;
  }}
  .logo {{ font-size: 1.15rem; font-weight: 700; letter-spacing: 1px; }}
  .logo span {{ font-weight: 400; font-size: 0.8rem; color: #888; margin-left: 6px; }}
  .nav-links a {{ margin-left: 20px; font-size: 0.88rem; color: #555; }}
  .nav-links a:hover {{ color: #8b5e3c; }}
  .article-wrap {{ max-width: 720px; margin: 0 auto; padding: 32px 5vw 60px; }}
  .breadcrumb {{ font-size: 0.8rem; color: #999; margin-bottom: 20px; }}
  .breadcrumb a {{ color: #8b5e3c; }}
  .article-header {{ margin-bottom: 32px; }}
  .article-header h1 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 12px; line-height: 1.4; }}
  .article-header .meta {{
    display: flex; gap: 16px; font-size: 0.82rem; color: #999; flex-wrap: wrap;
  }}
  .article-header .meta span {{ background: #f5f0eb; padding: 2px 10px; border-radius: 12px; }}
  .scene {{ margin-bottom: 32px; }}
  .scene h2 {{
    font-size: 1.15rem; font-weight: 600; margin-bottom: 14px;
    color: #8b5e3c; display: flex; align-items: center; gap: 8px;
  }}
  .scene h2::before {{ content: "鈻?; }}
  .scene p {{ font-size: 0.97rem; margin-bottom: 14px; color: #3a3a3a; }}
  .dialogue {{
    background: #fff; border-left: 3px solid #8b5e3c;
    padding: 16px 18px; margin: 16px 0; border-radius: 0 6px 6px 0;
  }}
  .dialogue .who {{ font-weight: 600; color: #8b5e3c; font-size: 0.85rem; margin-bottom: 6px; }}
  .dialogue .who::before {{ content: "馃挰 "; }}
  .dialogue p {{ font-size: 0.93rem; margin: 0; color: #444; }}
  .img-block {{
    margin: 20px 0; background: #e8e4df; border-radius: 6px;
    height: 260px; display: flex; align-items: center; justify-content: center;
    color: #999; font-size: 0.9rem;
  }}
  .img-caption {{ text-align: center; font-size: 0.78rem; color: #999; margin-top: 6px; }}
  .compare {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 20px 0;
  }}
  .compare .before, .compare .after {{
    background: #bbb; border-radius: 6px; height: 180px;
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 0.9rem;
  }}
  .compare .after {{ background: #ddd; color: #777; }}
  .cost-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9rem; }}
  .cost-table th, .cost-table td {{
    padding: 10px 12px; border: 1px solid #e0dcd7; text-align: left;
  }}
  .cost-table th {{ background: #f5f0eb; font-weight: 600; }}
  .cost-table tr:nth-child(even) {{ background: #faf9f7; }}
  .cost-table .total {{ font-weight: 700; color: #8b5e3c; }}
  .tags {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 32px 0; }}
  .tags span {{ background: #f5f0eb; padding: 4px 14px; border-radius: 16px; font-size: 0.82rem; color: #666; }}
  .cta-box {{
    background: #2c2c2c; color: #fff; border-radius: 8px; padding: 28px;
    text-align: center; margin: 40px 0;
  }}
  .cta-box h3 {{ font-size: 1.1rem; margin-bottom: 8px; font-weight: 500; }}
  .cta-box p {{ font-size: 0.9rem; color: #bbb; margin-bottom: 16px; }}
  .btn {{
    display: inline-block; padding: 12px 28px; background: #8b5e3c;
    color: #fff; border-radius: 4px; font-size: 0.9rem;
  }}
  .related {{ margin-top: 40px; padding-top: 24px; border-top: 1px solid #eee; }}
  .related h3 {{ font-size: 1rem; margin-bottom: 14px; }}
  .related a {{ display: block; padding: 10px 0; border-bottom: 1px solid #f0f0f0; font-size: 0.9rem; color: #555; }}
  .related a:hover {{ color: #8b5e3c; }}
  footer {{ text-align: center; padding: 24px 5vw; font-size: 0.82rem; color: #999; border-top: 1px solid #eee; }}
  footer a {{ color: #8b5e3c; }}
  @media (max-width: 480px) {{
    .article-header h1 {{ font-size: 1.25rem; }}
    .compare {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<nav>
  <div class="logo">钀嶈釜渚犲奖褰?<span>鍗氫富钀嶅</span></div>
  <div class="nav-links">
    <a href="index.html">棣栭爜</a>
    <a href="diary.html">瑁濅慨鏃ヨ</a>
    <a href="cases.html">妗堜緥</a>
    <a href="contact.html">鑱公</a>
  </div>
</nav>

<div class="article-wrap">

<div class="breadcrumb">
  <a href="index.html">棣栭爜</a> > <a href="diary.html">瑁濅慨鏃ヨ</a> > {title}
</div>

<div class="article-header">
  <h1>{title}</h1>
  <div class="meta">
    <span>馃搮 {date}</span>
    <span>馃搷 {location}</span>
    <span>馃彔 {unit_type}</span>
  </div>
</div>

<div class="scene">
  <h2>姝ｆ枃</h2>
  <p>{body.replace(chr(10), '</p>\\n  <p>')}</p>
</div>

<div class="tags">
  {tags_html}
</div>

<div class="cta-box">
  <h3>鎯崇煡閬撹嚜宸卞柈浣嶈淇咕閷紵</h3>
  <p>WhatsApp 鍌冲嫉鐩稿悓灏哄淇炬垜锛屽厤璨诲牨鍍癸紝鍞斾娇鍗冲埢姹哄畾</p>
  <a href="https://wa.me/85251902328" class="btn" target="_blank">馃摫 WhatsApp 鍏嶈不鍫卞児</a>
</div>

</div>

<footer>
  <p>漏 钀嶈釜渚犲奖褰?路 鍗氫富钀嶅 路 <a href="https://wa.me/85251902328" target="_blank">WhatsApp 鍫卞児</a> 路 棣欐腐涔濋緧鏃鸿</p>
</footer>

</body>
</html>
'''

def update_diary_index(title, date, location, cost, duration, unit_type, filename):
    """鎶婃柊鏂囩珷鍔犲埌 diary.html 鍒楄〃闋傞儴"""
    diary_path = os.path.join(BASE_DIR, 'diary.html')
    with open(diary_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_entry = f'''  <a href="{filename}">
    <div class="diary-row">
      <div class="thumb">Before/After</div>
      <div class="body">
        <div class="date">{date} 路 {location} 路 {unit_type}</div>
        <h3>{title}</h3>
        <p>锛堟柊鏂囩珷鎽樿寰呰鍏?..锛?/p>
        <div class="meta">
          <span>馃挵 {cost}</span>
          <span>鈴?{duration}</span>
          <span>馃彿 {unit_type}</span>
        </div>
      </div>
    </div>
  </a>

'''
    # 鎻掑叆鍒?<div class="diary-list"> 涔嬪緦
    insert_marker = '<div class="diary-list">'
    if insert_marker in content:
        content = content.replace(insert_marker, insert_marker + '\n' + new_entry, 1)
    
    with open(diary_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"鉁?宸叉洿鏂?diary.html")

def update_index_preview(title, date, location, cost, duration, unit_type, filename):
    """鏇存柊棣栭爜鏈€鏂版棩瑷橀爯瑕藉崁"""
    idx_path = os.path.join(BASE_DIR, 'index.html')
    with open(idx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_card = f'''    <div class="diary-card">
      <a href="{filename}">
        <div class="thumb">Before / After 鍦栫墖</div>
        <div class="body">
          <div class="date">{date} 路 {location}</div>
          <h3>{title}</h3>
          <p>锛堟柊鏂囩珷鎽樿寰呰鍏?..锛?/p>
          <div class="meta">
            <span>馃挵 {cost}</span>
            <span>鈴?{duration}</span>
            <span>馃彔 {unit_type}</span>
          </div>
        </div>
      </a>
    </div>
'''
    # 鏇挎彌绗竴鍊?diary-card锛堟渶鏂扮殑涓€绡囷級
    marker = '<div class="diary-card">'
    if marker in content:
        # 鎵惧埌绗竴鍊?diary-card 鍒扮祼鏉熶綅缃紝鏇挎彌
        start = content.find(marker)
        end_marker = '</div>\n  </div>\n\n</section>'
        end = content.find(end_marker, start)
        if end != -1:
            # 鎵惧埌瑭插崱鐗囩祼鏉?            card_end = content.find('</div>', content.find('</div>', start) + 6) + 6
            # 鏇寸啊鍠殑鍋氭硶锛氭妸绗竴鍊嬪崱鐗囨浛鎻?            first_card_end = content.find('</div>\n\n</section>', start)
            if first_card_end != -1:
                content = content[:start] + new_card + content[first_card_end:]
    
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"鉁?宸叉洿鏂?index.html 闋愯")

def main():
    print("=" * 50)
    print("  钀嶈釜渚犲奖褰?路 鐧煎竷鏂拌淇棩瑷?)
    print("=" * 50)
    print()
    
    title = input("馃搶 鏂囩珷妯欓锛?).strip()
    if not title:
        print("鉂?妯欓涓嶈兘鐐虹┖")
        return
    
    date = input("馃搮 鏃ユ湡锛圷YYY-MM-DD锛岀暀绌?浠婂ぉ锛夛細").strip()
    if not date:
        date = datetime.date.today().isoformat()
    
    location = input("馃搷 鍦板崁锛堝锛氬皣杌嶆境銆佽崈鐏ｏ級锛?).strip() or "棣欐腐"
    unit_type = input("馃彔 鍠綅椤炲瀷锛堝叕灞?灞呭眿/鍔忔埧/绉佹〒锛夛細").strip() or "鍏眿"
    cost = input("馃挵 绺藉児閷紙濡傦細$30,000锛夛細").strip() or "寰呭牨鍍?
    duration = input("鈴?宸ユ湡锛堝锛氬崐鏃ャ€?鏃ワ級锛?).strip() or "寰呭畾"
    tags = input("馃彿 妯欑堡锛堢敤閫楄櫉鍒嗛殧锛屽锛氬叕灞嬭淇?瀹氬埗瀹跺叿锛夛細").strip() or "棣欐腐瑁濅慨"
    
    print()
    print("馃摑 璜嬭几鍏ユ枃绔犳鏂囷紙绱旀枃鏈紝鏀彺鎻涜锛夛細")
    print("   锛堣几鍏ュ畬鎸?Enter 鍏╂绲愭潫锛?)
    print()
    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)
    body = '\n'.join(lines[:-1]) if len(lines) > 1 else '\n'.join(lines)
    
    if not body:
        body = "鏂囩珷姝ｆ枃寰呰鍏?.."
    
    # 鐢熸垚鏂囦欢鍚?    slug = slugify(title) or "post"
    filename = f"post-{date.replace('-','')}-{slug}.html"
    filepath = os.path.join(BASE_DIR, filename)
    
    # 鐢熸垚HTML
    html = generate_post_html(title, date, location, unit_type, cost, duration, tags, body)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n鉁?宸插壍寤猴細{filename}")
    
    # 鏇存柊鍒楄〃闋?    update_diary_index(title, date, location, cost, duration, unit_type, filename)
    update_index_preview(title, date, location, cost, duration, unit_type, filename)
    
    print()
    print("=" * 50)
    print("  鐧煎竷瀹屾垚锛?)
    print(f"  鏂囦欢锛歿filepath}")
    print("  涓嬩竴姝ワ細")
    print("  1. 鎶婂湒鐗囨斁鍒?images/ 鏂囦欢澶?)
    print("  2. 淇敼鏂囩珷涓殑鍗犱綅鍦栫墖璺緫")
    print("  3. 鎺ㄩ€佸埌 GitHub 鈫?Vercel 鑷嫊鏇存柊")
    print("=" * 50)

if __name__ == '__main__':
    main()


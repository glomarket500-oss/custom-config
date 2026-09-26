import os

API_KEY = 'sk-bjdhmdfdtzyjzzkekwcamvdzaidkurakdtenulyavkrvgbco'
API_URL = 'https://api.siliconflow.cn/v1/images/generations'
TIER_PRICE = {'simple': 650, 'medium': 1150, 'luxury': 2200}

html = '''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 免費設計效果圖 + 立即報價｜張丹楓、雲蕾——香港全屋定制</title>
  <meta name="description" content="上傳毛坯房照片，AI 即時生成裝修效果圖並計算報價區間。張丹楓、雲蕾香港全屋定制，免費上門量房。">
  <link rel="canonical" href="https://custom-api-cfg.vercel.app/ai-design.html">
  <meta property="og:title" content="AI 免費設計效果圖 + 立即報價｜香港全屋定制">
  <meta property="og:description" content="上傳毛坯房照片，AI 生成效果圖，並計算裝修報價區間。">
  <meta property="og:type" content="website">
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    body{font-family:"PingFang HK","Heiti TC","Noto Sans TC","Microsoft JhengHei",sans-serif;color:#2c2c2c;background:#faf9f7;line-height:1.7}
    nav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;padding:16px 5vw;background:#fff;border-bottom:1px solid #eee;position:sticky;top:0;z-index:100}
    .logo{font-size:1.1rem;font-weight:700;color:#8b5e3c}
    .logo span{display:block;font-size:.7rem;font-weight:400;color:#999}
    .nav-links{display:flex;flex-wrap:wrap;justify-content:flex-end}
    .nav-links a{margin-left:20px;font-size:.88rem;color:#555;text-decoration:none}
    .nav-links a:hover{color:#8b5e3c}
    .nav-links a.ai-nav{color:#8b5e3c;font-weight:600}
    .promo-banner{background:linear-gradient(90deg,#c0392b 0%,#e74c3c 100%);color:#fff;text-align:center;padding:10px 5vw;font-size:.9rem;font-weight:600}
    .promo-banner span{background:#fff;color:#c0392b;border-radius:3px;padding:1px 6px;font-size:.8rem;margin-right:6px}
    .promo-banner .fire{color:#ff6b35}
    .hero-banner{background:linear-gradient(135deg,#8b5e3c 0%,#c49a6c 100%);color:#fff;padding:48px 5vw 40px;text-align:center}
    .hero-banner h1{font-size:1.8rem;margin-bottom:10px}
    .hero-banner p{font-size:.95rem;opacity:.9;max-width:560px;margin:0 auto 16px}
    .hero-badge{display:inline-block;background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.4);border-radius:20px;padding:6px 18px;font-size:.85rem}
    .container{max-width:900px;margin:0 auto;padding:32px 5vw 48px}
    .card{background:#fff;border:1px solid #eee;border-radius:10px;padding:28px;margin-bottom:20px}
    .section-title{font-size:1rem;font-weight:600;margin-bottom:16px;color:#8b5e3c;display:flex;align-items:center;gap:6px}
    .form-row{margin-bottom:18px}
    .form-row:last-child{margin-bottom:0}
    .form-row label{display:block;font-weight:600;margin-bottom:7px;font-size:.88rem}
    .form-row .hint{font-size:.78rem;color:#999;margin-top:4px}
    input[type=text],input[type=number],select,textarea{width:100%;padding:10px 14px;border:1px solid #ddd;border-radius:6px;font-size:.92rem;font-family:inherit;background:#faf9f7;color:#2c2c2c}
    input:focus,select:focus,textarea:focus{outline:none;border-color:#8b5e3c}
    .two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    .radio-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}
    .radio-opt{display:none}
    .radio-opt+label{display:block;padding:9px 6px;border:1.5px solid #ddd;border-radius:6px;text-align:center;font-size:.82rem;cursor:pointer;transition:all .15s;background:#faf9f7}
    .radio-opt:checked+label{border-color:#8b5e3c;background:#fdf8f4;color:#8b5e3c;font-weight:600}
    .upload-area{border:2px dashed #ccc;border-radius:8px;padding:28px;text-align:center;cursor:pointer;transition:border-color .2s,background .2s}
    .upload-area:hover{border-color:#8b5e3c;background:#fdf8f4}
    .upload-area input[type=file]{display:none}
    .upload-icon{font-size:2.2rem;margin-bottom:6px}
    .upload-area .upload-hint{font-size:.82rem;color:#888}
    #preview-thumb{max-width:240px;max-height:180px;border-radius:6px;margin-top:10px;display:none;border:1px solid #eee}
    .price-display{background:linear-gradient(135deg,#8b5e3c 0%,#c49a6c 100%);border-radius:8px;padding:18px 24px;color:#fff;text-align:center;margin-bottom:16px}
    .price-display .label{font-size:.85rem;opacity:.85;margin-bottom:4px}
    .price-display .amount{font-size:2rem;font-weight:700}
    .price-display .range{font-size:.8rem;opacity:.75;margin-top:2px}
    .price-note{font-size:.75rem;color:#aaa;text-align:center;margin-bottom:16px}
    .btn-gen{display:block;width:100%;padding:15px;background:#8b5e3c;color:#fff;border:none;border-radius:8px;font-size:1.05rem;font-weight:700;cursor:pointer;font-family:inherit;transition:background .2s;margin-bottom:10px}
    .btn-gen:hover{background:#7a5234}
    .btn-gen:disabled{background:#c8a98a;cursor:not-allowed}
    .status-msg{text-align:center;margin-top:12px;font-size:.85rem;color:#666;min-height:20px}
    .status-msg.err{color:#c0392b}
    .result-section{display:none}
    .result-section.show{display:block}
    .result-section .card{border-color:#8b5e3c}
    .result-section img{width:100%;max-height:480px;object-fit:contain;border-radius:6px;display:block;margin-bottom:10px}
    .ai-note{font-size:.75rem;color:#bbb;text-align:center}
    .case-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}
    .case-card{border-radius:8px;overflow:hidden;border:1px solid #eee;background:#fff}
    .case-card .case-img{height:130px;background:#e8e0d8;display:flex;align-items:center;justify-content:center;font-size:2.2rem;color:#c49a6c}
    .case-card .case-body{padding:10px 12px}
    .case-card .case-title{font-size:.8rem;font-weight:600;color:#555}
    .case-card .case-meta{font-size:.72rem;color:#999;margin-top:2px}
    .trust-bar{background:#fff;border-top:1px solid #eee;border-bottom:1px solid #eee;padding:20px 5vw;display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin-bottom:24px}
    .trust-item{text-align:center}
    .trust-item .num{font-size:1.6rem;font-weight:700;color:#8b5e3c}
    .trust-item .txt{font-size:.75rem;color:#888}
    .bottom-cta{background:linear-gradient(135deg,#8b5e3c 0%,#c49a6c 100%);border-radius:12px;padding:36px 24px;text-align:center;color:#fff;margin-bottom:24px}
    .bottom-cta h2{font-size:1.25rem;margin-bottom:8px}
    .bottom-cta p{font-size:.88rem;opacity:.85;margin-bottom:20px}
    .bottom-cta .cta-btn{display:inline-block;padding:13px 32px;background:#fff;color:#8b5e3c;border-radius:6px;font-size:.95rem;font-weight:700;text-decoration:none}
    .bottom-cta .cta-btn:hover{background:#fdf8f4}
    footer{text-align:center;padding:24px 5vw;font-size:.82rem;color:#aaa;border-top:1px solid #eee}
    @media(max-width:480px){
      .hero-banner h1{font-size:1.3rem}
      .two-col{grid-template-columns:1fr}
      .radio-grid{grid-template-columns:repeat(3,1fr)}
      .case-grid{grid-template-columns:repeat(2,1fr)}
      nav{flex-direction:column;align-items:flex-start}
      .nav-links{justify-content:flex-start}
      .nav-links a{margin:0 10px 0 0}
      .trust-bar{gap:20px}
    }
  </style>
</head>
<body>

<nav>
  <div class="logo">萍踪侠影录 <span>張丹楓、雲蕾</span></div>
  <div class="nav-links">
    <a href="index.html">首頁</a>
    <a href="diary.html">博主講古</a>
    <a href="live.html">直播間</a>
    <a href="social.html">社媒</a>
    <a href="about.html">認識博主</a>
    <a href="cases.html">案例</a>
    <a href="contact.html">聯繫</a>
    <a href="ai-design.html" class="ai-nav">AI 免費設計</a>
  </div>
</nav>

<div class="promo-banner">
  <span>🔥 本月名額</span>前 20 名報名免費上門量房，額滿即止｜張丹楓、雲蕾香港全屋定制
</div>

<section class="hero-banner">
  <h1>🤖 AI 免費設計效果圖 + 立即報價</h1>
  <p>上傳毛坯房照片，選擇風格，AI 即時生成效果圖，並計算裝修報價區間——完全免費，張丹楓、雲蕾幫你發堀新家的可能性。</p>
  <div class="hero-badge">⚡ 30 秒內生成效果圖 · 📐 同步計算報價</div>
</section>

<div class="container">

  <div class="card">
    <div class="section-title">📋 填寫基本資料</div>
    <div class="two-col">
      <div class="form-row">
        <label>房間類型</label>
        <select id="room-type">
          <option value="living">客廳</option>
          <option value="bedroom">臥室</option>
          <option value="whole">全屋</option>
        </select>
      </div>
      <div class="form-row">
        <label>面積（平方米）</label>
        <input type="number" id="area" placeholder="例如：45" min="5" max="2000">
      </div>
    </div>
  </div>

  <div class="card">
    <div class="section-title">🎨 選擇裝修風格</div>
    <div class="radio-grid">
      <input type="radio" class="radio-opt" name="style" id="s1" value="現代簡約" checked>
      <label for="s1">現代簡約</label>
      <input type="radio" class="radio-opt" name="style" id="s2" value="北歐">
      <label for="s2">北歐</label>
      <input type="radio" class="radio-opt" name="style" id="s3" value="新中式">
      <label for="s3">新中式</label>
      <input type="radio" class="radio-opt" name="style" id="s4" value="輕奢">
      <label for="s4">輕奢</label>
      <input type="radio" class="radio-opt" name="style" id="s5" value="日式">
      <label for="s5">日式</label>
      <input type="radio" class="radio-opt" name="style" id="s6" value="美式">
      <label for="s6">美式</label>
    </div>
  </div>

  <div class="card">
    <div class="section-title">💰 選擇裝修檔次</div>
    <div class="radio-grid">
      <input type="radio" class="radio-opt" name="tier" id="t1" value="simple">
      <label for="t1">簡單｜$650/㎡</label>
      <input type="radio" class="radio-opt" name="tier" id="t2" value="medium" checked>
      <label for="t2">中等｜$1,150/㎡</label>
      <input type="radio" class="radio-opt" name="tier" id="t3" value="luxury">
      <label for="t3">豪華｜$2,200/㎡</label>
    </div>
  </div>

  <div class="card">
    <div class="section-title">📸 上傳毛坯房照片（選填）</div>
    <div class="upload-area" id="upload-area">
      <div class="upload-icon">📁</div>
      <div style="font-size:.88rem;font-weight:600;margin-bottom:4px;">點擊上傳或拖曳圖片</div>
      <div class="upload-hint">支援 JPG / PNG / WEBP，建議解析度 1024×768 或以上</div>
      <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp">
      <img id="preview-thumb" alt="毛坯房預覽">
    </div>
    <div class="hint" style="margin-top:8px;">上傳照片有助 AI 生成更精準效果圖；不上傳也可生成標準風格效果圖。</div>
  </div>

  <div class="card">
    <div class="section-title">✏️ 補充描述（選填）</div>
    <div class="form-row">
      <textarea id="extra-prompt" placeholder="例如：想要白色沙發、木地板、圓形茶几、陽光要充足……越詳細效果越好"></textarea>
    </div>
  </div>

  <div class="price-display" id="price-box" style="display:none;">
    <div class="label">參考裝修報價區間</div>
    <div class="amount" id="price-amount">—</div>
    <div class="range" id="price-range"></div>
  </div>
  <div class="price-note">實際報價以師傅上門量房後最終報價為準</div>

  <button class="btn-gen" id="gen-btn" onclick="generate()">⚡ 生成效果圖 + 獲取報價</button>
  <div class="status-msg" id="status-msg"></div>

  <div class="result-section" id="result-section">
    <div class="card">
      <div class="section-title">✨ 效果圖已完成</div>
      <img id="result-img" alt="AI 裝修效果圖">
      <p class="ai-note">⚠️ 效果圖由 AI 生成，僅供參考。實際裝修效果請與師傅溝通確認。</p>
    </div>
  </div>

</div>

<div class="trust-bar">
  <div class="trust-item"><div class="num">10年+</div><div class="txt">裝修經驗</div></div>
  <div class="trust-item"><div class="num">1000+</div><div class="txt">服務業主</div></div>
  <div class="trust-item"><div class="num">100%</div><div class="txt">香港師傅</div></div>
  <div class="trust-item"><div class="num">0</div><div class="txt">隱藏收費</div></div>
</div>

<div class="container" style="padding-top:0;">
  <div class="card">
    <div class="section-title">🏠 真實裝修案例</div>
    <div class="case-grid">
      <div class="case-card">
        <div class="case-img">🪑</div>
        <div class="case-body">
          <div class="case-title">土瓜灣 L 形廚房</div>
          <div class="case-meta">現代簡約 · 8.5㎡</div>
        </div>
      </div>
      <div class="case-card">
        <div class="case-img">🛋️</div>
        <div class="case-body">
          <div class="case-title">觀塘公屋全屋定制</div>
          <div class="case-meta">北歐風 · 32㎡</div>
        </div>
      </div>
      <div class="case-card">
        <div class="case-img">🛏️</div>
        <div class="case-body">
          <div class="case-title">屯門簡屋臥室</div>
          <div class="case-meta">日式原木 · 12㎡</div>
        </div>
      </div>
      <div class="case-card">
        <div class="case-img">🪟</div>
        <div class="case-body">
          <div class="case-title">深水埗唐樓客廳</div>
          <div class="case-meta">輕奢風 · 18㎡</div>
        </div>
      </div>
    </div>
  </div>

  <div class="bottom-cta">
    <h2>💬 想要完整設計方案 + 詳細報價？</h2>
    <p>效果圖满意就想落實裝修？張丹楓、雲蕾幫你由設計到完工一站式服務，歡迎立即聯絡。</p>
    <a href="https://wa.me/85251902328?text=%E5%B8%AB%E5%82%85%EF%BC%8C%E6%88%91%E7%9C%8B%E5%AE%8C%E4%BD%A0%E7%9A%84AI%E6%95%88%E6%9E%9C%E5%9C%96%E4%BB%A5%E5%8F%8A%E5%85%88%E5%8F%8A%E5%A0%B1%E5%83%B9%EF%BC%8C%E6%88%91%E6%83%B3%E5%95%8F%E4%B8%8B%E8%A3%9D%E5%83%8A%E5%B9%B4%E5%89%AF%E6%88%BF%E4%BB%A5%E5%8F%8A%E5%AE%9A%E5%88%B6%E5%84%AA%E6%83%95%E5%83%8A%E5%B9%B4%E6%9C%8D%E5%8B%9E%EF%BC%9A" class="cta-btn" target="_blank">📱 WhatsApp 免費獲取完整設計方案 + 詳細報價</a>
  </div>
</div>

<footer>
  <p>© 2026 張丹楓、雲蕾｜香港全屋定制｜hkdecor.online｜服務全港｜WhatsApp：5190 2328</p>
</footer>

<script>
var API_KEY = "''' + API_KEY + '''";
var API_URL = "''' + API_URL + '''";
var uploadedImageBase64 = null;
var TIER_PRICE = ''' + str(TIER_PRICE) + ''';

function updatePrice() {
  var area = parseFloat(document.getElementById("area").value) || 0;
  var tierEl = document.querySelector("input[name=tier]:checked");
  var tier = tierEl ? tierEl.value : "medium";
  var priceBox = document.getElementById("price-box");
  if (area >= 5) {
    var total = TIER_PRICE[tier] * area;
    var low = Math.round(total * 0.85);
    var high = Math.round(total * 1.15);
    var tierLabel = tier === "simple" ? "簡單" : tier === "medium" ? "中等" : "豪華";
    document.getElementById("price-amount").textContent = "HK$ " + low.toLocaleString() + " \u2013 " + high.toLocaleString();
    document.getElementById("price-range").textContent = "\u300C" + area + "㎡\u300D\u00D7\u300C" + tierLabel + " HK$" + TIER_PRICE[tier].toLocaleString() + "/㎡\u300D\u2248 HK$" + total.toLocaleString();
    priceBox.style.display = "block";
  } else {
    priceBox.style.display = "none";
  }
}
document.getElementById("area").addEventListener("input", updatePrice);
var tierRadios = document.querySelectorAll("input[name=tier]");
for (var i = 0; i < tierRadios.length; i++) tierRadios[i].addEventListener("change", updatePrice);

var uploadArea = document.getElementById("upload-area");
var fileInput = document.getElementById("file-input");
uploadArea.addEventListener("click", function(){ fileInput.click(); });
uploadArea.addEventListener("dragover", function(e){ e.preventDefault(); uploadArea.style.borderColor="#8b5e3c"; });
uploadArea.addEventListener("dragleave", function(){ uploadArea.style.borderColor="#ccc"; });
uploadArea.addEventListener("drop", function(e){
  e.preventDefault(); uploadArea.style.borderColor="#ccc";
  if (e.dataTransfer.files[0]) processFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener("change", function(){ if(fileInput.files[0]) processFile(fileInput.files[0]); });

function processFile(file) {
  if (!file.type.match(/^image\/(jpeg|png|webp)$/)) { setStatus("[ERROR] 請上傳 JPG、PNG 或 WEBP 格式圖片", true); return; }
  var reader = new FileReader();
  reader.onload = function(e) {
    uploadedImageBase64 = e.target.result.split(",")[1];
    document.getElementById("preview-thumb").src = e.target.result;
    document.getElementById("preview-thumb").style.display = "block";
    setStatus("[OK] 圖片已上傳，可以生成效果圖了");
  };
  reader.readAsDataURL(file);
}

async function generate() {
  var btn = document.getElementById("gen-btn");
  var resultSection = document.getElementById("result-section");
  var area = parseFloat(document.getElementById("area").value) || 0;
  if (area < 5) { setStatus("\u274C \u8ACB\u8F38\u5165\u6709\u6548\u7684\u9762\u7A4D\uFF08\u5E73\u65B9\u7C73\uFF09", true); return; }

  var styleEl = document.querySelector("input[name=style]:checked");
  var tierEl = document.querySelector("input[name=tier]:checked");
  var style = styleEl ? styleEl.value : "\u73FE\u4EE3\u7C21\u7D04";
  var tier = tierEl ? tierEl.value : "medium";
  var extra = document.getElementById("extra-prompt").value.trim();

  btn.disabled = true;
  btn.textContent = "[ 生成中，請稍候… ]";
  setStatus(">> 正在請求 AI 生成效果圖，大約 30-60 秒…");
  resultSection.classList.remove("show");

  var styleMap = {
    "\u73FE\u4EE3\u7C21\u7D04": "modern minimalist interior design, clean white walls, sleek built-in cabinets, neutral tones, contemporary Hong Kong apartment renovation photorealistic render",
    "\u5317\u6B50": "Scandinavian style interior, light oak flooring, pastel accent wall, minimalist furniture, cozy and bright, Nordic home renovation photorealistic render",
    "\u65B0\u4E2D\u5F0F": "new Chinese modern interior, elegant dark wood furniture, subtle traditional motifs, contemporary Chinese style apartment renovation photorealistic render",
    "\u8F15\u5965": "luxury modern interior, gold accent details, marble surfaces, sophisticated lighting, upscale Hong Kong apartment renovation photorealistic render",
    "\u65E5\u5F0F": "Japanese minimalist interior, natural wood textures, tatami inspired corner, warm wood flooring, serene and functional Japanese style renovation photorealistic render",
    "\u7F8E\u5F0F": "American country style interior, warm wood tones, farmhouse kitchen cabinets, cozy countryside home renovation photorealistic render"
  };

  var stylePrompt = styleMap[style] || styleMap["\u73FE\u4EE3\u7C21\u7D04"];
  var extraClause = extra ? ", additional details: " + extra : "";
  var tierClause = tier === "luxury" ? ", luxury high-end finishes" : tier === "simple" ? ", simple clean finishes" : ", standard quality finishes";

  try {
    var imageUrl = null;
    if (uploadedImageBase64) {
      try {
        var imgPayload = {
          model: "FLUX.1-dev",
          image: uploadedImageBase64,
          prompt: "Interior design rendering based on uploaded room photo. " + stylePrompt + tierClause + extraClause + ". High quality architectural visualization, photorealistic, no text, no watermark.",
          image_size: "1024x1024",
          num_inference_steps: 30,
          guidance_scale: 7.5
        };
        var imgResp = await fetch(API_URL, {
          method: "POST",
          headers: { "Authorization": "Bearer " + API_KEY, "Content-Type": "application/json" },
          body: JSON.stringify(imgPayload)
        });
        if (imgResp.ok) {
          var imgData = await imgResp.json();
          if (imgData.images && imgData.images[0] && imgData.images[0].url) imageUrl = imgData.images[0].url;
        }
      } catch(_e) {}
    }
    if (!imageUrl) {
      var textPayload = {
        model: "FLUX.1-dev",
        prompt: "Interior design rendering. " + stylePrompt + tierClause + extraClause + ". High quality architectural visualization, photorealistic, no text, no watermark, Hong Kong apartment renovation.",
        image_size: "1024x1024",
        num_inference_steps: 30,
        guidance_scale: 7.5
      };
      var textResp = await fetch(API_URL, {
        method: "POST",
        headers: { "Authorization": "Bearer " + API_KEY, "Content-Type": "application/json" },
        body: JSON.stringify(textPayload)
      });
      if (!textResp.ok) throw new Error("API " + textResp.status);
      var textData = await textResp.json();
      if (!textData.images || !textData.images[0] || !textData.images[0].url) throw new Error(JSON.stringify(textData));
      imageUrl = textData.images[0].url;
    }
    document.getElementById("result-img").src = imageUrl;
    resultSection.classList.add("show");
    updatePrice();
    window.scrollTo({ top: resultSection.offsetTop - 80, behavior: "smooth" });
    setStatus("[OK] 效果圖已生成！請查看效果圖及上方報價區間。");
    btn.disabled = false;
    btn.textContent = ">> 再次生成效果圖";
  } catch(err) {
    setStatus("[ERROR] 生成失敗：" + err.message, true);
    btn.disabled = false;
    btn.textContent = ">> 生成效果圖 + 獲取報價";
  }
}

function setStatus(msg, isErr) {
  var el = document.getElementById("status-msg");
  el.textContent = msg;
  el.className = "status-msg" + (isErr ? " err" : "");
}
</script>

</body>
</html>'''

path = 'C:/Users/a/Desktop/custom-config/ai-design.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Written', len(html), 'bytes to', path)

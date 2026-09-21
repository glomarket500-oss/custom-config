#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-031
export SILICONFLOW_API_KEY="$SILICONFLOW_API_KEY"
URL="https://api.siliconflow.cn/v1/images/generations"

# 5 张图
gen() {
  local fn="$1"
  local prompt="$2"
  echo ">>> 生成 $fn"
  local body
  body=$(printf '{"model":"Tongyi-MAI/Z-Image-Turbo","prompt":"%s","image_size":"1024x1024","batch_size":1,"num_inference_steps":30,"guidance_scale":7.5}' "$prompt")
  for i in 1 2 3; do
    local resp
    resp=$(curl -s -X POST "$URL" \
      -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$body" \
      --max-time 120)
    local img_url
    img_url=$(echo "$resp" | python -c "import sys,json; d=json.load(sys.stdin); print(d['images'][0]['url'])" 2>/dev/null || echo "")
    if [ -n "$img_url" ]; then
      curl -s -o "$fn" "$img_url" --max-time 90
      local sz
      sz=$(stat -c%s "$fn" 2>/dev/null || echo 0)
      echo "    OK ${fn} ${sz} bytes"
      return 0
    fi
    echo "    attempt $i failed: ${resp:0:200}"
    sleep 3
  done
  return 1
}

# 1. hero - 油塘長者屋邨大堂
gen "post-031-hero.png" "Hong Kong Yau Tong elderly public housing estate corridor early morning, 1970s public lobby, weathered green painted wall, tiled floor, fluorescent ceiling lights, cinematic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

# 2. scene-01 - 板件驗收
gen "post-031-scene-01-board.png" "Hong Kong small apartment workshop interior, daylight through window, master carpenter hand pointing at plywood panel laid on wooden table, hand tools nearby, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

# 3. scene-02 - 到頂大櫃安裝
gen "post-031-scene-02-cabinet.png" "Hong Kong tiny living room custom floor-to-ceiling wardrobe installation, plywood cabinet frame, master carpenter installing hanging rail, daylight, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

# 4. scene-03 - 水性漆/油漆對比
gen "post-031-scene-03-paint.png" "Hong Kong furniture workshop close-up, two paint cans on wooden table near window, daylight, shallow depth of field, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

# 5. scene-04 - 港鐵老友記拍八達通
gen "post-031-scene-04-octopus.png" "Hong Kong MTR train interior, elderly passenger tapping Octopus card at fare gate, platform visible through window, fluorescent lighting, candid documentary photography, no text, no logo, no watermark, no identifiable person"

echo ""
echo "=== 完成 ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-031/*.png

#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-033
mkdir -p /c/Users/a/Desktop/custom-config/images/post-033
export SILICONFLOW_API_KEY="$SILICONFLOW_API_KEY"
URL="https://api.siliconflow.cn/v1/images/generations"

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
      if [ "$sz" -ge 500000 ]; then
        return 0
      fi
    fi
    echo "    attempt $i failed: ${resp:0:200}"
    sleep 3
  done
  return 1
}

# 1. hero - 大坑街道舞火龍前夕掛燈籠
gen "post-033-hero.png" "Hong Kong Tai Hang street evening Mid-Autumn festival lanterns hanging above old tong lau street, red paper lanterns glowing at dusk, traditional atmosphere, narrow lane with shutters, cinematic editorial street photography, no text, no logo, no watermark, no identifiable person"

# 2. scene-01 - 唐樓廚房牆身微微傾斜 + 雷射水平儀
gen "post-033-scene-01-kitchen.png" "Hong Kong old tong lau small kitchen interior, slightly tilted wall visible, carpenter holding laser level on tripod near plywood cabinet base, fluorescent ceiling light, window with grille, realistic editorial interior photography, no text, no logo, no watermark, no identifiable person"

# 3. scene-02 - 鋅盤底板斜放 / L形角鐵承托
gen "post-033-scene-02-zinc.png" "Hong Kong old apartment kitchen under-sink cabinet base detail, slightly sloped zinc sink base panel, L-shaped steel bracket reinforcement, water supply pipe visible, workshop daylight, realistic editorial close-up photography, no text, no logo, no watermark, no identifiable person"

# 4. scene-03 - 飄窗櫈訂造（一戶一尺）
gen "post-033-scene-03-window.png" "Hong Kong tong lau living room bay window seat custom built-in, light wood plywood bench fitted under window, sunlight streaming in, aged wall paint, realistic editorial interior photography, no text, no logo, no watermark, no identifiable person"

# 5. scene-04 - 大坑舞火龍竹棚紮作
gen "post-033-scene-04-dragon.png" "Hong Kong Tai Hang night Fire Dragon Dance preparation, bamboo scaffolding structure, incense sticks inserted, glowing joss sticks red light, street lanterns above, nighttime atmospheric documentary photography, no text, no logo, no watermark, no identifiable person"

echo ""
echo "=== 完成 ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-033/*.png
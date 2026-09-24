#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-035
mkdir -p /c/Users/a/Desktop/custom-config/images/post-035
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

gen "post-035-hero.png" "Hong Kong To Kwa Wan old tong lau flat kitchen corner early morning, elderly master craftsman measuring wall corner with tape measure, worn tiled wall and old window grille, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

gen "post-035-scene-01-kitchen.png" "Hong Kong old apartment small kitchen L-shaped cabinet corner detail, water pipes along wall, plywood cabinet base frame fitted around pipes, fluorescent ceiling light, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

gen "post-035-scene-02-hands.png" "Close-up of elderly craftsman weathered hands holding steel tape measure against wooden workbench, scars and wrinkles visible, chisels and hand tools blurred background, warm workshop light, realistic documentary photography, no text, no logo, no watermark, no identifiable person"

gen "post-035-scene-03-shop.png" "Hong Kong To Kwa Wan old street afternoon, shuttered shopfronts and small family renovation workshop sign-free facade, quiet street with few pedestrians, overcast daylight, documentary street photography, no text, no logo, no watermark, no identifiable person"

gen "post-035-scene-04-tea.png" "Hong Kong old cha chaan teng interior afternoon, hot milk tea cup on formica table in booth seat, sunlight through venetian blinds, empty seat opposite, nostalgic documentary photography, no text, no logo, no watermark, no identifiable person"

echo ""
echo "=== 完成 ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-035/*.png
#!/bin/bash
set -e
OUTDIR="C:/Users/a/Desktop/custom-config/images/post-036"
mkdir -p "$OUTDIR"
cd "$OUTDIR"
ENVF="C:/Users/a/AppData/Local/hermes/profiles/auto-publish/.env"
KEY=$(grep '^SILICONFLOW_API_KEY=' "$ENVF" | cut -d= -f2- | tr -d '\r ')
if [ -z "$KEY" ]; then echo "NO KEY"; exit 1; fi
URL="https://api.siliconflow.cn/v1/images/generations"

gen() {
  local fn="$1"
  local prompt="$2"
  echo ">>> gen $fn"
  local body
  body=$(printf '{"model":"Tongyi-MAI/Z-Image-Turbo","prompt":"%s","image_size":"1024x1024","batch_size":1,"num_inference_steps":30,"guidance_scale":7.5}' "$prompt")
  for i in 1 2 3; do
    local resp
    resp=$(curl -s -X POST "$URL" \
      -H "Authorization: Bearer $KEY" \
      -H "Content-Type: application/json" \
      -d "$body" \
      --max-time 150)
    local img_url
    img_url=$(echo "$resp" | grep -o '"url":"[^"]*"' | head -n1 | cut -d'"' -f4)
    if [ -n "$img_url" ]; then
      curl -s -o "$fn" "$img_url" --max-time 120
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

gen "post-036-hero.png" "Hong Kong Kwun Tong public housing flat living room morning, half-finished custom-built TV cabinet and wardrobe frames in pale wood, toolbox and tape measure on floor, soft daylight through window, realistic editorial interior photography, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

gen "post-036-scene-01-edge.png" "Close-up of edge banding machine sealing wardrobe door panel in small Hong Kong renovation workshop, wood-grain edge strip fusing to plywood board, warm work light, sawdust particles, realistic documentary photography, no text, no logo, no watermark, no identifiable person"

gen "post-036-scene-02-balcony.png" "Hong Kong public housing flat balcony before typhoon, washing machine cabinet frame covered with large red nylon sheet, stacked plywood boards moved indoors, dark storm clouds over harbour rooftops outside window, realistic editorial interior photography, no text, no logo, no watermark, no identifiable person"

gen "post-036-scene-03-salt.png" "Empty newly fitted bedroom corner in Hong Kong public estate flat, large industrial salt bag placed on floor for moisture absorption, freshly painted skirting and custom wardrobe side panel, quiet afternoon light, realistic editorial interior photography, no text, no logo, no watermark, no identifiable person"

gen "post-036-scene-04-reunion.png" "Hong Kong family Mid-Autumn reunion dinner table at night with mooncakes and fruit, new custom sideboard cabinet against wall glowing under warm lamp, full moon visible through window, cosy documentary photography, no text, no logo, no watermark, no identifiable person"

echo ""
echo "=== done ==="
ls -lh "$OUTDIR"/*.png
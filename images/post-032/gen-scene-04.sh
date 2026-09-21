#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-032
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

# post-032 scene-04 - 簡屋收工、社區中心飲水/輕鐵
gen "post-032-scene-04-community.png" "Hong Kong simple public housing community center interior evening, two renovation workers sitting on bench drinking water, light rail tram visible through window glass, daylight fluorescent lighting, realistic documentary interior photography, no text, no logo, no watermark, no identifiable person"
echo "=== done ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-032/*.png
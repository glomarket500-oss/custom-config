#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-035
export SILICONFLOW_API_KEY="$SILICONFLOW_API_KEY"
URL="https://api.siliconflow.cn/v1/images/generations"

gen() {
  local fn="$1"
  local size="$2"
  local prompt="$3"
  echo ">>> 生成 $fn ($size)"
  local body
  body=$(printf '{"model":"Tongyi-MAI/Z-Image-Turbo","prompt":"%s","image_size":"%s","batch_size":1,"num_inference_steps":30,"guidance_scale":7.5}' "$prompt" "$size")
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
      if [ "$sz" -ge 100000 ]; then
        return 0
      fi
    fi
    echo "    attempt $i failed: ${resp:0:200}"
    sleep 3
  done
  return 1
}

SUF="realistic editorial photography, no text, no logo, no watermark, no identifiable person"

gen "youtube-post-035-laohangzun-quanshu-cover-zh.png" "1280x720" "Hong Kong old flat kitchen renovation wide scene, elderly master craftsman crouching measuring cabinet corner with tape measure, young apprentice watching and learning, daylight from window, $SUF"
gen "youtube-post-035-laohangzun-quanshu-cover-en.png" "1280x720" "Hong Kong tong lau kitchen interior renovation scene, craftsman hands fitting L-shaped plywood cabinet around water pipes, tools on floor, warm daylight, $SUF"
gen "linkedin-post-035-laohangzun-quanshu-cover-zh.png" "1200x627" "Hong Kong renovation workshop professional scene, master craftsman reviewing hand-drawn kitchen cabinet blueprint on workbench with younger colleague, businesslike daylight office, $SUF"
gen "linkedin-post-035-laohangzun-quanshu-cover-en.png" "1200x627" "Hong Kong interior fit-out site professional photo, custom kitchen cabinets half installed, level tool and plans on countertop, clean corporate daylight, $SUF"
gen "facebook-post-035-laohangzun-quanshu-cover-zh.png" "1200x630" "Hong Kong cosy completed small kitchen with light wood L-shaped cabinets, kettle on stove, warm homely afternoon light through window, $SUF"
gen "facebook-post-035-laohangzun-quanshu-cover-en.png" "1200x630" "Hong Kong small family kitchen finished renovation, neat L-shaped cupboards and tiled wall, sunlight and plant on windowsill, homely documentary photo, $SUF"
gen "instagram-post-035-laohangzun-quanshu-cover-zh.png" "1080x1080" "Square close-up of elderly craftsman weathered hands holding chisel on wooden cabinet door, wood shavings, warm workshop bokeh, $SUF"
gen "instagram-post-035-laohangzun-quanshu-cover-en.png" "1080x1080" "Square photo of traditional woodworking hand tools laid on workbench, plane chisels and tape measure, top view warm light, $SUF"
gen "tiktok-post-035-laohangzun-quanshu-cover-zh.png" "1080x1920" "Vertical Hong Kong old cha chaan teng booth with hot milk tea on table, sunlight stripes through blinds, nostalgic mood, $SUF"
gen "tiktok-post-035-laohangzun-quanshu-cover-en.png" "1080x1920" "Vertical Hong Kong old street with family renovation workshop storefront, afternoon long shadows, urban documentary mood, $SUF"
gen "twitter-post-035-laohangzun-quanshu-cover-zh.png" "1600x900" "Wide Hong Kong To Kwa Wan streetscape morning, old tong lau buildings with shops below, laundry hanging, everyday city life, $SUF"
gen "twitter-post-035-laohangzun-quanshu-cover-en.png" "1600x900" "Wide Hong Kong old district rooftops and kitchen extractor vents at dusk, residential blocks layered, city documentary wide shot, $SUF"

echo ""
echo "=== 完成 ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-035/*cover*.png
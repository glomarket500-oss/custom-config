#!/bin/bash
set -e
cd /c/Users/a/Desktop/custom-config/images/post-034
mkdir -p /c/Users/a/Desktop/custom-config/images/post-034
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

# 1. hero - 大埔舊樓44年外牆吊船清晨
gen "post-034-hero.png" "Hong Kong Tai Po old residential building exterior early morning, 1970s public housing high-rise tower facade, scaffolding platform suspended on side, urban documentary photography, golden hour soft light, no text, no logo, no watermark, no identifiable person"

# 2. scene-01 - 地鐵車廂內望手機新聞
gen "post-034-scene-01-radio.png" "Hong Kong MTR train carriage interior morning rush hour, elderly passenger sitting and reading news on smartphone, train doors closed, fluorescent lighting, candid documentary photography, no text, no logo, no watermark, no identifiable person"

# 3. scene-02 - 舊樓大維修合約文件砂漿厚度6mm
gen "post-034-scene-02-contract.png" "Hong Kong small workshop table top view, renovation contract documents spread out, handwritten notes next to printed agreement, magnifying glass and pen on table, daylight through window, shallow depth of field documentary photography, no text, no logo, no watermark, no identifiable person"

# 4. scene-03 - 舊樓主人房牆身發霉
gen "post-034-scene-03-mold.png" "Hong Kong old apartment bedroom corner wall, visible mold stains and water damage patches on aged wall paint, peeling paint revealing plaster underneath, dim natural light from window, documentary architecture photography, no text, no logo, no watermark, no identifiable person"

# 5. scene-04 - 黃太記事簿寫三條鐵律
gen "post-034-scene-04-notebook.png" "Hong Kong small flat living room, elderly woman writing notes in small notebook at dining table, three written rules listed on page, soft daylight, cups of tea on table, candid documentary photography, no text, no logo, no watermark, no identifiable person"

# 5. scene-05 - 發展局預審名單文件（实际是 scene 1/5 套路）
gen "post-034-scene-05-list.png" "Hong Kong office desk top view, government policy document printed pages and approved contractor list spread on wooden table, magnifying glass beside, pen and coffee cup, daylight from window, documentary editorial photography, no text, no logo, no watermark, no identifiable person"

echo ""
echo "=== 完成 ==="
ls -lh /c/Users/a/Desktop/custom-config/images/post-034/*.png
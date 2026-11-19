#!/usr/bin/env bash
# Faz qualquer bicho dançar a mesma dança de um vídeo de referência (Kling pela assinatura).
# uso: kit/dancar.sh <video-referencia.mp4> <nome> "<descrição do bicho em inglês>" [imagem-pronta.png]
#   1) vestir.py pinta roupa no dançarino da referência (o Kling recusa corpo que parece nu)
#   2) kling text_to_image cria o bicho em pé (9:16), se não vier imagem pronta
#   3) kling motion_control copia a dança da referência para o bicho
#   4) põe a música da referência e o fecho "construindo no INEMA.CLUB · baixa o kit"
# Saída: saida/<nome>/<nome>-final.mp4
set -euo pipefail
REF="$(realpath "$1")"; NOME="$2"; BICHO="$3"; IMG="${4:+$(realpath "$4")}"
KIT="$(cd "$(dirname "$0")" && pwd)"; K="${KLING:-kling}"
OUT="$(pwd)/saida/$NOME"; mkdir -p "$OUT"; cd "$OUT"

[ -f referencia-vestida.mp4 ] || {
  python3 "$KIT/vestir.py" "$REF" vestida-raw.mp4
  ffmpeg -v error -y -i vestida-raw.mp4 -c:v libx264 -crf 20 -pix_fmt yuv420p referencia-vestida.mp4; }

if [ -z "$IMG" ]; then
  "$K" text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 --img_resolution 2k --poll 300 \
    "Photorealistic vertical photo, full body. Exactly one $BICHO standing upright on two hind legs like a person, one head, standing in the center of the scene, full body visible, natural light, sharp detail." > img.json
  python3 - <<'E'
import json, re, urllib.request
s = open('img.json').read(); j = json.loads(s[s.index('\n{') + 1:] if s.lstrip()[0] != '{' else s)
w = j['body']['generations'][0]['result']['works'][0]
urllib.request.urlretrieve(w.get('url_without_watermark') or w['url'], 'bicho.png')
E
  IMG="$OUT/bicho.png"
fi

"$K" motion_control --model kling-video-v3_0 --image "$IMG" --video referencia-vestida.mp4 \
  --motionDirection motion_direction --resolution 720p --keepOriginalSound false --poll 2300 \
  "The $BICHO from the image dances, copying the dance moves exactly, happy expressive face, natural fur and skin with no clothes, keep the background from the image" > motion.json
python3 - <<'E'
import json, urllib.request
g = json.load(open('motion.json'))['body']['generations'][0]
w = g['result']['works'][0]
if g['status'] != 'COMPLETED':
    raise SystemExit(f"Kling: {g['status']} {w.get('message')}")
urllib.request.urlretrieve(w.get('url_without_watermark') or w['url'], 'danca-raw.mp4')
E
ffmpeg -v error -y -i danca-raw.mp4 -i "$REF" -map 0:v -map 1:a? -c:v libx264 -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -shortest danca.mp4
python3 "$KIT/fecho.py" danca.mp4 "$NOME-final.mp4"
echo "pronto: $OUT/$NOME-final.mp4"

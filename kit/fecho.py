"""Fecho dos reels: nos últimos segundos o vídeo escurece e o texto se constrói letra a letra
("construindo no / INEMA.CLUB / baixa o kit"). Uso: python3 fecho.py <entrada.mp4> <saida.mp4> [segundos=4.5]"""
import os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
SEG = float(sys.argv[3]) if len(sys.argv) > 3 else 4.5
W, H, FPS = 720, 1280, 30
FONT = os.path.expanduser('~/.local/share/fonts/Montserrat-Black.ttf')
AMARELO, BRANCO = (250, 204, 21, 255), (255, 255, 255, 255)
LINHAS = [('construindo no', 58, BRANCO), ('INEMA.CLUB', 92, AMARELO), ('baixa o kit', 70, BRANCO)]

dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                           capture_output=True, text=True).stdout)
ini = dur - SEG
n = int(SEG * FPS)
total_chars = sum(len(t) for t, _, _ in LINHAS)
tmp = tempfile.mkdtemp(prefix='fecho-')
fonts = {s: ImageFont.truetype(FONT, s) for _, s, _ in LINHAS}
for f in range(n):
    t = f / FPS
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    escuro = min(1, t / 0.6) * 0.62                     # escurece em 0,6 s
    d.rectangle([0, 0, W, H], fill=(12, 12, 16, int(255 * escuro)))
    vis = int(max(0, t - 0.4) / 2.2 * total_chars)      # 2,2 s para escrever tudo
    y = H * 0.36
    resto, cursor_feito = vis, False
    for texto, size, cor in LINHAS:
        k = max(0, min(len(texto), resto))
        parte = texto[:k]
        resto -= len(texto)
        fnt = fonts[size]
        x = (W - d.textlength(texto, font=fnt)) / 2
        if parte:
            d.text((x, y), parte, font=fnt, fill=cor, stroke_width=6, stroke_fill=(0, 0, 0, 255))
        if not cursor_feito and k < len(texto) and escuro > 0.3:
            cursor_feito = True                               # cursor piscando na linha que está sendo escrita
            if (f // 8) % 2 == 0:
                cx = x + d.textlength(parte, font=fnt) + 4
                d.rectangle([cx, y + size * 0.1, cx + 8, y + size * 1.05], fill=AMARELO)
        y += size * 1.35
    im.save(f'{tmp}/{f:04d}.png')

subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-framerate', str(FPS), '-i', f'{tmp}/%04d.png',
                '-filter_complex',
                f'[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b];'
                f'[1:v]setpts=PTS+{ini:.3f}/TB[o];[b][o]overlay=0:0:eof_action=pass[v]',
                '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '160k', out], check=True)
print('ok', out)

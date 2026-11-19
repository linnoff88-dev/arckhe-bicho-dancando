"""Porco dançando 100% Agnes: 1 âncora + 3 poses derivadas (img2img) + 3 clipes
keyframe de 8 s (pose→pose) em 9:16 = 24 s. Idempotente: rode de novo para refazer só o que falta."""
import os, sys, json, threading
sys.path.insert(0, os.path.expanduser('~/projetos/videos-agnes'))
import pipeline as P

D = os.path.dirname(os.path.abspath(__file__))
P.STYLE = ('photorealistic smartphone video still, natural warm afternoon sunlight, '
           'sharp detail, natural colors, vertical 9:16 framing')
SIZE = os.environ.get('AGNES_SIZE', '736x1312')

PIG = ('exactly one chubby pink pig standing upright on two hind legs like a person, one head, '
       'big round belly, short arms, wearing a glossy dark brown bowl-cut mop-top wig')
YARD = ('in a sunny dusty dirt yard of a rural South Asian village, old brick wall and thatched '
        'straw roof shelter behind, a small leafy tree on the right, black garbage bags by the wall, '
        'full body visible, static camera')
ANCORA = ('anc', f'Full body photo of {PIG}, happy smiling face, standing relaxed {YARD}.')
POSES = [
    ('p1', 'The same pig strikes a ballerina pose: one arm curved over its head, body turned three-quarters, '
           f'one leg slightly bent, eyes closed with a proud smile, {YARD}.'),
    ('p2', 'The same pig turns sideways, does a cheeky salute with one hand at its forehead, '
           f'hips pushed to one side, big belly sticking out, laughing, {YARD}.'),
    ('p3', 'The same pig squats low with knees bent and both arms stretched out to the sides, '
           f'mouth open in a big happy laugh, {YARD}.'),
]
MOV = [
    'the pig dances playfully, sways its hips and wiggles its round belly, then rises into a ballerina pose with one arm over its head',
    'the pig spins slowly, rolls its hips and shakes its shoulders to the music, then turns sideways and gives a cheeky salute',
    'the pig bounces to the beat, steps forward with arms out, wiggles its belly, laughs and drops into a low proud squat',
]
estado_p = os.path.join(D, 'estado.json')
E = json.load(open(estado_p)) if os.path.exists(estado_p) else {}
salva = lambda: json.dump(E, open(estado_p, 'w'), indent=1)


def img(i, prompt, refs=None):
    dest = os.path.join(D, f'{i}.png')
    if os.path.exists(dest) and E.get(i):
        return E[i]
    texto = f'{prompt} {P.MESMO} {P.SO_UM} {P.STYLE}' if refs else f'{prompt} {P.SO_UM} {P.STYLE}'
    body = {'model': 'agnes-image-2.1-flash', 'prompt': texto, 'size': SIZE,
            'extra_body': {'response_format': 'url'}}
    if refs:
        body['extra_body']['image'] = refs
    import urllib.request, time
    for t in range(1, 6):
        try:
            u = P._post(P.IMG_API, body)['data'][0]['url']
            open(dest, 'wb').write(urllib.request.urlopen(u, timeout=180).read())
            print(f'  [{i}] ok', flush=True)
            E[i] = u; salva(); return u
        except Exception as e:
            print(f'    {i} falha {t}: {str(e)[:100]}', flush=True); time.sleep(5 * t)
    sys.exit(f'imagem {i} falhou')


a = img(*ANCORA)
urls = [a] + [img(i, p, [a]) for i, p in POSES]
if '--so-imagens' in sys.argv:
    sys.exit(0)

P.ASPECT = '9:16'
ths = []
for n in range(3):
    dest = os.path.join(D, f'clipe{n+1}.mp4')
    if os.path.exists(dest):
        continue
    t = threading.Thread(target=P.gerar_video, args=(dest, urls[n], urls[n + 1], MOV[n], 8 * 24))
    t.start(); ths.append(t)
    import time; time.sleep(15)   # rate limit 6/min
for t in ths:
    t.join()
print('clipes:', [os.path.exists(os.path.join(D, f'clipe{n+1}.mp4')) for n in range(3)])

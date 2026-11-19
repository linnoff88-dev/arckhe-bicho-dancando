"""Tira a pose do vídeo original (MediaPipe) e desenha um boneco de manequim
fazendo a mesma dança, em fundo liso. Uso: python3 boneco.py <video> <saida.mp4>"""
import sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
import os, urllib.request

MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pose_landmarker_heavy.task')
if not os.path.exists(MODELO):  # modelo de pose do Google (30 MB), baixado uma vez
    urllib.request.urlretrieve('https://storage.googleapis.com/mediapipe-models/pose_landmarker/'
                               'pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task', MODELO)

src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

opts = vision.PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODELO),
    running_mode=vision.RunningMode.VIDEO, num_poses=1,
    min_pose_detection_confidence=0.3, min_tracking_confidence=0.3)
det = vision.PoseLandmarker.create_from_options(opts)

poses, i = [], 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
    r = det.detect_for_video(img, int(i * 1000 / fps))
    poses.append(np.array([[l.x * W, l.y * H] for l in r.pose_landmarks[0]]) if r.pose_landmarks else None)
    i += 1
n_ok = sum(p is not None for p in poses)
print(f'quadros {len(poses)}  com pose {n_ok} ({100*n_ok/len(poses):.0f}%)')

# preenche buracos com a última pose válida e suaviza (média móvel de 5 quadros)
last = next(p for p in poses if p is not None)
filled = []
for p in poses:
    last = p if p is not None else last
    filled.append(last)
arr = np.stack(filled)
k = 5
pad = np.pad(arr, ((k // 2, k // 2), (0, 0), (0, 0)), mode='edge')
arr = np.stack([pad[j:j + k].mean(0) for j in range(len(arr))])

BONES = [(11, 12), (11, 23), (12, 24), (23, 24),        # tronco
         (11, 13), (13, 15), (12, 14), (14, 16),        # braços
         (23, 25), (25, 27), (24, 26), (26, 28),        # pernas
         (27, 31), (28, 32)]                            # pés
vw = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
for p in arr:
    c = np.full((H, W, 3), (235, 235, 235), np.uint8)
    cv2.line(c, (0, int(H * 0.86)), (W, int(H * 0.86)), (200, 200, 200), 2)
    pt = lambda j: tuple(int(v) for v in p[j])
    sh = np.linalg.norm(p[11] - p[12])
    th = max(10, int(sh * 0.22))
    # tronco preenchido
    torso = np.array([pt(11), pt(12), pt(24), pt(23)], np.int32)
    cv2.fillConvexPoly(c, torso, (90, 90, 90), cv2.LINE_AA)
    for a, b in BONES:
        cv2.line(c, pt(a), pt(b), (60, 60, 60), th, cv2.LINE_AA)
    for j in (11, 12, 13, 14, 23, 24, 25, 26):
        cv2.circle(c, pt(j), th // 2 + 3, (30, 30, 30), -1, cv2.LINE_AA)
    # cabeça: centro entre orelhas/nariz, raio pela largura dos ombros
    head = ((p[7] + p[8]) / 2 * 0.5 + p[0] * 0.5).astype(int)
    cv2.circle(c, tuple(head), max(18, int(sh * 0.32)), (60, 60, 60), -1, cv2.LINE_AA)
    cv2.line(c, tuple(((p[11] + p[12]) / 2).astype(int)), tuple(head), (60, 60, 60), th, cv2.LINE_AA)
    vw.write(c)
vw.release()
print('ok', out)

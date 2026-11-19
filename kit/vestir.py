"""Pinta camiseta + short no dançarino do vídeo de referência usando a pose (MediaPipe).
Uso: python3 vestir.py <video> <saida.mp4>"""
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
det = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODELO),
    running_mode=vision.RunningMode.VIDEO, num_poses=1,
    min_pose_detection_confidence=0.3, min_tracking_confidence=0.3,
    output_segmentation_masks=True))

frames, poses, masks, i = [], [], [], 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    r = det.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,
                                      data=cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)), int(i * 1000 / fps))
    frames.append(fr)
    if r.pose_landmarks:
        poses.append(np.array([[l.x * W, l.y * H] for l in r.pose_landmarks[0]]))
        masks.append(r.segmentation_masks[0].numpy_view().copy())
    else:
        poses.append(None); masks.append(None)
    i += 1

last_p, last_m = next(p for p in poses if p is not None), next(m for m in masks if m is not None)
P, M = [], []
for p, m in zip(poses, masks):
    last_p = p if p is not None else last_p
    last_m = m if m is not None else last_m
    P.append(last_p); M.append(last_m)
arr = np.stack(P)
k = 5
pad = np.pad(arr, ((k // 2, k // 2), (0, 0), (0, 0)), mode='edge')
arr = np.stack([pad[j:j + k].mean(0) for j in range(len(arr))])

SHIRT, SHORTS = (190, 110, 30), (40, 40, 170)   # BGR: azul, vermelho escuro
vw = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
for fr, p, m in zip(frames, arr, M):
    body = (cv2.resize(m, (W, H)) > 0.4).astype(np.uint8)
    sh_y = (p[11][1] + p[12][1]) / 2
    hip_y = (p[23][1] + p[24][1]) / 2
    knee_y = (p[25][1] + p[26][1]) / 2
    ys = np.arange(H)[:, None]
    shirt_zone = ((ys >= sh_y - 0.05 * (hip_y - sh_y)) & (ys < hip_y + 0.08 * (hip_y - sh_y)))
    shorts_zone = ((ys >= hip_y + 0.08 * (hip_y - sh_y)) & (ys < hip_y + 0.6 * (knee_y - hip_y)))
    # tira os braços da camiseta: só o miolo horizontal do corpo naquela altura
    x_lo = min(p[11][0], p[12][0], p[23][0], p[24][0]) - 0.6 * abs(p[11][0] - p[12][0])
    x_hi = max(p[11][0], p[12][0], p[23][0], p[24][0]) + 0.6 * abs(p[11][0] - p[12][0])
    xs = np.arange(W)[None, :]
    core = (xs >= x_lo) & (xs <= x_hi)
    o = fr.copy()
    for zone, col in ((shirt_zone, SHIRT), (shorts_zone, SHORTS)):
        z = (zone & core & (body > 0))
        sh = fr[z].astype(np.float32).mean(axis=1, keepdims=True) / 200.0  # mantém sombreado
        o[z] = np.clip(np.array(col, np.float32) * (0.55 + 0.6 * sh), 0, 255).astype(np.uint8)
    vw.write(o)
vw.release()
print('ok', out, len(frames))

# bicho-dancando

[![bicho-dancando](guia/assets/banner-en.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## What it is

bicho-dancando is a script kit for anyone who makes short videos and wants a kitten dancing just like in a reference video. You provide a video of someone dancing and a phrase describing the kitten; the kit paints an outfit on the dancer, creates an image of the kitten standing up, and tells Kling (an AI video generator) to copy the moves. At the end, it adds the music and a closing card with ARCKHÉ AI text. You need a Kling subscription with its command-line tool installed, Python, and ffmpeg.

## ðŸ“– User guide

Complete guide (landing page + walkthrough): **https://linnoff88-dev.github.io/

A kit for taking the dance from a video and making **any animal** dance the same way: pig, capybara, kitten.
It uses Kling through your subscription (CLI `kling`) and Agnes as a free alternative. The local scripts
(pose, painted outfit, closing card) run on your machine at no cost.

| Version | How it works | Step accuracy | Measured cost (24 s, 720p) |
|---|---|---|---|
| **Copied dance** (recommended) | "Dressed" reference + Kling Motion Control 3.0 | nearly frame by frame | 216 credits |
| Kling 4.0 from text | Animal image + choreography described in the prompt | flexible moves | 240 credits |
| Agnes | 4 poses + 3 8-second keyframe clips | flexible moves, may drift from the scene | free (Agnes API) |

![Result](exemplos/resultado-porco.jpg)

## Video examples

Three animals dancing the same dance (216 credits each):

- ðŸ· Bowl-cut pig â€” https://www.youtube.com/watch?v=3jfNlJ4DduI
- ðŸ¦« Diva capybara â€” https://www.youtube.com/watch?v=opnakJZBDro
- ðŸ± Cute kitten â€” https://www.youtube.com/watch?v=aivt5jwgGX4

## The process, from start to finish

Key: ðŸ§  session with Nei Â· âš™ï¸ script Â· ðŸ¤– AI service

1. ðŸ§  **Choose the reference video** (a full-body dancer, stationary camera). Download it with ARCKHÉvox:
   `python3 baixar_v1.py --url "<URL>" --outdir ref/`
2. âš™ï¸ **Dress the dancer** â€” `python3 kit/vestir.py ref/video.mp4 vestida.mp4`. MediaPipe finds the pose and
   silhouette in each frame and paints on a T-shirt and shorts. Why: Kling **rejects** videos of bodies that look nude
   (`AGENT.FileCensorshipUnsafe`), and a **stick figure** (`kit/boneco.py`) passes the check but fails with
   "No valid characters detected". Painted clothes pass both checks.
3. ðŸ¤– **Create the animal** standing up, 9:16 â€” `kling text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 ...`
   (4 credits for 2 images). Choose the one showing the full body with some space around it.
4. ðŸ¤– **Copy the dance** â€” `kling motion_control --model kling-video-v3_0 --image bicho.png --video vestida.mp4
   --motionDirection motion_direction --resolution 720p`. In the prompt, ask for "natural fur, no clothes" so the
   outfit from the reference doesn't transfer to the animal.
5. âš™ï¸ **Music + closing card** â€” add the reference audio and run `python3 kit/fecho.py danca.mp4 final.mp4`:
   in the last 4.5 seconds, the video darkens and the text is written letter by letter
   ("construindo no / **ARCKHÉ AI** / baixa o kit" (building on / **ARCKHÉ AI** / download the kit), Montserrat Black, yellow `#FACC15`).
6. ðŸ§  **Check the frame sheet** before publishing (face, background, hands).
7. âš™ï¸ **Publish** â€” YouTube with `yt-pubx --agendar` (one per hour) and Instagram/TikTok with Metricool.

Run it all at once (steps 2â€“5):

```bash
kit/dancar.sh ref/video.mp4 capivara "chubby capybara diva with a pink feather boa and red lipstick"
```

## Free version with Agnes

`kit/agnes_poses.py` (pig example): 1 anchor image + 3 poses derived from it (img2img, to keep it the same
animal) + 3 8-second keyframe clips moving from pose to pose in 9:16. Requires the `videos-agnes` project and
`AGNES_API_KEY`. Measured limitation: in one of the 3 clips, the scene drifted (background changed, animal turned away) â€” check the
sheet and redo only the faulty clip.

![Agnes poses](exemplos/agnes-poses.jpg)

## Files

| File | What it does |
|---|---|
| `kit/dancar.sh` | steps 2â€“5 in one call |
| `kit/vestir.py` | paints clothes on the reference dancer (MediaPipe pose + mask) |
| `kit/boneco.py` | draws a stick figure doing the same dance (useful for studying the choreography) |
| `kit/fecho.py` | darkens the ending and writes ARCKHÉ AI text letter by letter |
| `kit/agnes_poses.py` | Agnes version: poses + keyframe clips |

Requirements: `ffmpeg`, Python 3 with `mediapipe`, `opencv-python`, `pillow`; logged-in `kling` CLI
(`npm i -g @klingai/cli-global` + `kling login`). The pose model (30 MB) downloads automatically the first time. The closing card uses `~/.local/share/fonts/Montserrat-Black.ttf` (Google Fonts, `static/` folder in the zip).

## Limitations

- Kling decides what counts as a "character": pure line drawings don't count; a photorealistic animal standing up does.
- The animal's pose matters: with the capybara "standing still" (paws close to its body), Motion Control returned "No valid characters detected in the image" (no charge); the same capybara in a dance pose (leg raised, arms apart) worked. Choose an image with the arms and legs clearly separated from the body.
- Motion Control inherits the framing from the reference; if the dancer leaves the frame, the animal will too.
- CLI login expires: `kling login` opens the browser and waits only 5 minutes for the return.
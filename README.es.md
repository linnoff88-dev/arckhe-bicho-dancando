# bicho-dancando

[![bicho-dancando](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## QuÃ© es

bicho-dancando es un kit de scripts para quienes hacen videos cortos y quieren que un animal baile igual que en un video de referencia. TÃº proporcionas un video de alguien bailando y una frase que describe al animal; el kit pinta ropa sobre el bailarÃ­n, crea la imagen del animal de pie y le pide a Kling (generador de video con IA) que copie los pasos. Al final, une la mÃºsica y un cierre con el texto de ARCKHÉ AI. Necesitas una suscripciÃ³n de Kling, la herramienta de lÃ­nea de comandos instalada, Python y ffmpeg.

## ðŸ“– GuÃ­a de uso

GuÃ­a completa (landing + paso a paso): **https://linnoff88-dev.github.io/

Kit para tomar el baile de un video y hacer que **cualquier animal** baile igual: cerdo, capibara, gatita.
Usa Kling con la suscripciÃ³n (CLI `kling`) y, como alternativa gratis, Agnes. Los scripts locales
(pose, ropa pintada, cierre) se ejecutan en tu mÃ¡quina, sin costo.

| VersiÃ³n | CÃ³mo | Fidelidad a los pasos | Costo medido (24 s, 720p) |
|---|---|---|---|
| **Baile copiado** (recomendado) | referencia "vestida" + Kling Motion Control 3.0 | casi cuadro a cuadro | 216 crÃ©ditos |
| Kling 4.0 por texto | imagen del animal + coreografÃ­a descrita en el prompt | pasos libres | 240 crÃ©ditos |
| Agnes | 4 poses + 3 clips keyframe de 8 s | pasos libres, puede desviarse de la escena | gratis (API Agnes) |

![Resultado](exemplos/resultado-porco.jpg)

## Ejemplos en video

Los tres animales bailando el mismo baile (216 crÃ©ditos cada uno):

- ðŸ· Cerdo con corte de pelo de tazÃ³n â€” https://www.youtube.com/watch?v=3jfNlJ4DduI
- ðŸ¦« Capibara diva â€” https://www.youtube.com/watch?v=opnakJZBDro
- ðŸ± Gatita tierna â€” https://www.youtube.com/watch?v=aivt5jwgGX4

## El proceso, de principio a fin

Leyenda: ðŸ§  sesiÃ³n con Nei Â· âš™ï¸ script Â· ðŸ¤– servicio de IA

1. ðŸ§  **Elegir el video de referencia** (un bailarÃ­n de cuerpo entero, cÃ¡mara fija). Descargarlo con ARCKHÉvox:
   `python3 baixar_v1.py --url "<URL>" --outdir ref/`
2. âš™ï¸ **Vestir al bailarÃ­n** â€” `python3 kit/vestir.py ref/video.mp4 vestida.mp4`. MediaPipe detecta la pose y la
   silueta de cada cuadro, y pinta una camiseta y un pantalÃ³n corto. Por quÃ©: Kling **rechaza** videos de cuerpos que parecen desnudos
   (`AGENT.FileCensorshipUnsafe`), y un **muÃ±eco de lÃ­neas** (`kit/boneco.py`) pasa la verificaciÃ³n, pero falla con
   "No valid characters detected". La ropa pintada pasa ambas.
3. ðŸ¤– **Crear el animal** de pie, en 9:16 â€” `kling text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 ...`
   (4 crÃ©ditos por 2 imÃ¡genes). Elige la que muestre el cuerpo entero con espacio alrededor.
4. ðŸ¤– **Copiar el baile** â€” `kling motion_control --model kling-video-v3_0 --image bicho.png --video vestida.mp4
   --motionDirection motion_direction --resolution 720p`. En el prompt, pide "natural fur, no clothes" para que la ropa
   de la referencia no se transfiera al animal.
5. âš™ï¸ **MÃºsica + cierre** â€” unir el audio de referencia y ejecutar `python3 kit/fecho.py danca.mp4 final.mp4`:
   durante los Ãºltimos 4,5 s, el video se oscurece y el texto se escribe letra por letra
   ("construindo no / **ARCKHÉ AI** / baixa o kit" (construyendo en / **ARCKHÉ AI** / descarga el kit), Montserrat Black, amarillo `#FACC15`).
6. ðŸ§  **Revisar la hoja de cuadros** antes de publicar (rostro, fondo, manos).
7. âš™ï¸ **Publicar** â€” YouTube con `yt-pubx --agendar` (uno por hora) e Instagram/TikTok con Metricool.

Todo de una vez (pasos 2â€“5):

```bash
kit/dancar.sh ref/video.mp4 capivara "chubby capybara diva with a pink feather boa and red lipstick"
```

## VersiÃ³n gratis con Agnes

`kit/agnes_poses.py` (ejemplo del cerdo): 1 imagen ancla + 3 poses derivadas de ella (img2img, para que sea el mismo
animal) + 3 clips keyframe de 8 s que van de una pose a otra en 9:16. Necesita el proyecto `videos-agnes` y
`AGNES_API_KEY`. LÃ­mite medido: en uno de los 3 clips la escena se desviÃ³ (cambiÃ³ el fondo, el animal quedÃ³ de espaldas); revisa la
hoja y vuelve a generar solo el clip defectuoso.

![Poses Agnes](exemplos/agnes-poses.jpg)

## Archivos

| Archivo | QuÃ© hace |
|---|---|
| `kit/dancar.sh` | pasos 2â€“5 en una llamada |
| `kit/vestir.py` | pinta ropa sobre el bailarÃ­n de referencia (pose + mÃ¡scara de MediaPipe) |
| `kit/boneco.py` | dibuja un maniquÃ­ de lÃ­neas con el mismo baile (Ãºtil para estudiar la coreografÃ­a) |
| `kit/fecho.py` | oscurece el final y escribe el texto de ARCKHÉ AI letra por letra |
| `kit/agnes_poses.py` | versiÃ³n Agnes: poses + clips keyframe |

Requisitos: `ffmpeg`, Python 3 con `mediapipe`, `opencv-python`, `pillow`; CLI `kling` con sesiÃ³n iniciada
(`npm i -g @klingai/cli-global` + `kling login`). El modelo de pose (30 MB) se descarga automÃ¡ticamente la primera vez. El cierre usa `~/.local/share/fonts/Montserrat-Black.ttf` (Google Fonts, carpeta `static/` del zip).

## LÃ­mites

- Kling decide quÃ© cuenta como "personaje": un dibujo de lÃ­neas no cuenta; un animal fotorrealista de pie sÃ­.
- La pose del animal importa: con la capibara "quieta" (patas junto al cuerpo), Motion Control devolviÃ³ "No valid characters detected in the image" (sin cobrar); la misma capibara en pose de baile (una pierna levantada, brazos separados) funcionÃ³. Elige una imagen con los brazos y las piernas bien separados del cuerpo.
- Motion Control hereda el encuadre de la referencia; si el bailarÃ­n sale del cuadro, el animal tambiÃ©n.
- La sesiÃ³n de la CLI caduca: `kling login` abre el navegador y espera solo 5 minutos a que regreses.
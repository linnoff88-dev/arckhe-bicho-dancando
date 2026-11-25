# bicho-dancando

[![bicho-dancando](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## QuêÂ© es

bicho-dancando es un kit de scripts para quienes hacen videos cortos y quieren que un animal baile igual que en un video de referencia. TêÂº proporcionas un video de alguien bailando y una frase que describe al animal; el kit pinta ropa sobre el bailarêÂ­n, crea la imagen del animal de pie y le pide a Kling (generador de video con IA) que copie los pasos. Al final, une la mêÂºsica y un cierre con el texto de ARCKHê AI. Necesitas una suscripciêÂ³n de Kling, la herramienta de lêÂ­nea de comandos instalada, Python y ffmpeg.

## ê°Å¸ââ GuêÂ­a de uso

GuêÂ­a completa (landing + paso a paso): **https://linnoff88-dev.github.io/

Kit para tomar el baile de un video y hacer que **cualquier animal** baile igual: cerdo, capibara, gatita.
Usa Kling con la suscripciêÂ³n (CLI `kling`) y, como alternativa gratis, Agnes. Los scripts locales
(pose, ropa pintada, cierre) se ejecutan en tu mêÂ¡quina, sin costo.

| VersiêÂ³n | CêÂ³mo | Fidelidad a los pasos | Costo medido (24 s, 720p) |
|---|---|---|---|
| **Baile copiado** (recomendado) | referencia "vestida" + Kling Motion Control 3.0 | casi cuadro a cuadro | 216 crêÂ©ditos |
| Kling 4.0 por texto | imagen del animal + coreografêÂ­a descrita en el prompt | pasos libres | 240 crêÂ©ditos |
| Agnes | 4 poses + 3 clips keyframe de 8 s | pasos libres, puede desviarse de la escena | gratis (API Agnes) |

![Resultado](exemplos/resultado-porco.jpg)

## Ejemplos en video

Los tres animales bailando el mismo baile (216 crêÂ©ditos cada uno):

- ê°Å¸ÂÂ· Cerdo con corte de pelo de tazêÂ³n ê¢â¬â https://www.youtube.com/watch?v=3jfNlJ4DduI
- ê°Å¸Â¦Â« Capibara diva ê¢â¬â https://www.youtube.com/watch?v=opnakJZBDro
- ê°Å¸ÂÂ± Gatita tierna ê¢â¬â https://www.youtube.com/watch?v=aivt5jwgGX4

## El proceso, de principio a fin

Leyenda: ê°Å¸Â§Â  sesiêÂ³n con Nei êÂ· ê¢Å¡â¢ê¯Â¸Â script êÂ· ê°Å¸Â¤â servicio de IA

1. ê°Å¸Â§Â  **Elegir el video de referencia** (un bailarêÂ­n de cuerpo entero, cêÂ¡mara fija). Descargarlo con ARCKHêvox:
   `python3 baixar_v1.py --url "<URL>" --outdir ref/`
2. ê¢Å¡â¢ê¯Â¸Â **Vestir al bailarêÂ­n** ê¢â¬â `python3 kit/vestir.py ref/video.mp4 vestida.mp4`. MediaPipe detecta la pose y la
   silueta de cada cuadro, y pinta una camiseta y un pantalêÂ³n corto. Por quêÂ©: Kling **rechaza** videos de cuerpos que parecen desnudos
   (`AGENT.FileCensorshipUnsafe`), y un **muêÂ±eco de lêÂ­neas** (`kit/boneco.py`) pasa la verificaciêÂ³n, pero falla con
   "No valid characters detected". La ropa pintada pasa ambas.
3. ê°Å¸Â¤â **Crear el animal** de pie, en 9:16 ê¢â¬â `kling text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 ...`
   (4 crêÂ©ditos por 2 imêÂ¡genes). Elige la que muestre el cuerpo entero con espacio alrededor.
4. ê°Å¸Â¤â **Copiar el baile** ê¢â¬â `kling motion_control --model kling-video-v3_0 --image bicho.png --video vestida.mp4
   --motionDirection motion_direction --resolution 720p`. En el prompt, pide "natural fur, no clothes" para que la ropa
   de la referencia no se transfiera al animal.
5. ê¢Å¡â¢ê¯Â¸Â **MêÂºsica + cierre** ê¢â¬â unir el audio de referencia y ejecutar `python3 kit/fecho.py danca.mp4 final.mp4`:
   durante los êÂºltimos 4,5 s, el video se oscurece y el texto se escribe letra por letra
   ("construindo no / **ARCKHê AI** / baixa o kit" (construyendo en / **ARCKHê AI** / descarga el kit), Montserrat Black, amarillo `#FACC15`).
6. ê°Å¸Â§Â  **Revisar la hoja de cuadros** antes de publicar (rostro, fondo, manos).
7. ê¢Å¡â¢ê¯Â¸Â **Publicar** ê¢â¬â YouTube con `yt-pubx --agendar` (uno por hora) e Instagram/TikTok con Metricool.

Todo de una vez (pasos 2ê¢â¬â5):

```bash
kit/dancar.sh ref/video.mp4 capivara "chubby capybara diva with a pink feather boa and red lipstick"
```

## VersiêÂ³n gratis con Agnes

`kit/agnes_poses.py` (ejemplo del cerdo): 1 imagen ancla + 3 poses derivadas de ella (img2img, para que sea el mismo
animal) + 3 clips keyframe de 8 s que van de una pose a otra en 9:16. Necesita el proyecto `videos-agnes` y
`AGNES_API_KEY`. LêÂ­mite medido: en uno de los 3 clips la escena se desviêÂ³ (cambiêÂ³ el fondo, el animal quedêÂ³ de espaldas); revisa la
hoja y vuelve a generar solo el clip defectuoso.

![Poses Agnes](exemplos/agnes-poses.jpg)

## Archivos

| Archivo | QuêÂ© hace |
|---|---|
| `kit/dancar.sh` | pasos 2ê¢â¬â5 en una llamada |
| `kit/vestir.py` | pinta ropa sobre el bailarêÂ­n de referencia (pose + mêÂ¡scara de MediaPipe) |
| `kit/boneco.py` | dibuja un maniquêÂ­ de lêÂ­neas con el mismo baile (êÂºtil para estudiar la coreografêÂ­a) |
| `kit/fecho.py` | oscurece el final y escribe el texto de ARCKHê AI letra por letra |
| `kit/agnes_poses.py` | versiêÂ³n Agnes: poses + clips keyframe |

Requisitos: `ffmpeg`, Python 3 con `mediapipe`, `opencv-python`, `pillow`; CLI `kling` con sesiêÂ³n iniciada
(`npm i -g @klingai/cli-global` + `kling login`). El modelo de pose (30 MB) se descarga automêÂ¡ticamente la primera vez. El cierre usa `~/.local/share/fonts/Montserrat-Black.ttf` (Google Fonts, carpeta `static/` del zip).

## LêÂ­mites

- Kling decide quêÂ© cuenta como "personaje": un dibujo de lêÂ­neas no cuenta; un animal fotorrealista de pie sêÂ­.
- La pose del animal importa: con la capibara "quieta" (patas junto al cuerpo), Motion Control devolviêÂ³ "No valid characters detected in the image" (sin cobrar); la misma capibara en pose de baile (una pierna levantada, brazos separados) funcionêÂ³. Elige una imagen con los brazos y las piernas bien separados del cuerpo.
- Motion Control hereda el encuadre de la referencia; si el bailarêÂ­n sale del cuadro, el animal tambiêÂ©n.
- La sesiêÂ³n de la CLI caduca: `kling login` abre el navegador y espera solo 5 minutos a que regreses.
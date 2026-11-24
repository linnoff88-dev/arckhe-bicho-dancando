# bicho-dancando

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![bicho-dancando](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

O bicho-dancando Ã© um kit de scripts para quem faz vÃ­deos curtos e quer um bicho danÃ§ando igualzinho a um vÃ­deo de referÃªncia. VocÃª dÃ¡ um vÃ­deo de alguÃ©m danÃ§ando e uma frase descrevendo o bicho; o kit pinta uma roupa no danÃ§arino, cria a imagem do bicho em pÃ© e manda o Kling (gerador de vÃ­deo por IA) copiar os passos. No fim junta a mÃºsica e um fecho com o texto do ARCKHÉ AI. Precisa de uma assinatura do Kling com a ferramenta de linha de comando instalada, Python e ffmpeg.

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo): **https://linnoff88-dev.github.io/

Kit para pegar a danÃ§a de um vÃ­deo e fazer **qualquer bicho** danÃ§ar igual: porco, capivara, gatinha.
Usa o Kling pela assinatura (CLI `kling`) e, como alternativa grÃ¡tis, o Agnes. Os scripts locais
(pose, roupa pintada, fecho) rodam na sua mÃ¡quina, sem custo.

| VersÃ£o | Como | Fidelidade aos passos | Custo medido (24 s, 720p) |
|---|---|---|---|
| **DanÃ§a copiada** (recomendada) | referÃªncia "vestida" + Kling Motion Control 3.0 | quase quadro a quadro | 216 crÃ©ditos |
| Kling 4.0 por texto | imagem do bicho + coreografia descrita no prompt | passos livres | 240 crÃ©ditos |
| Agnes | 4 poses + 3 clipes keyframe de 8 s | passos livres, pode desviar de cena | grÃ¡tis (API Agnes) |

![Resultado](exemplos/resultado-porco.jpg)

## Exemplos em vÃ­deo

Os trÃªs bichos danÃ§ando a mesma danÃ§a (216 crÃ©ditos cada):

- ðŸ· Porco de cabelo de cuia â€” https://www.youtube.com/watch?v=3jfNlJ4DduI
- ðŸ¦« Capivara diva â€” https://www.youtube.com/watch?v=opnakJZBDro
- ðŸ± Gatinha fofa â€” https://www.youtube.com/watch?v=aivt5jwgGX4

## O processo, do inÃ­cio ao fim

Legenda: ðŸ§  sessÃ£o com o Nei Â· âš™ï¸ script Â· ðŸ¤– serviÃ§o de IA

1. ðŸ§  **Escolher o vÃ­deo de referÃªncia** (um danÃ§arino de corpo inteiro, cÃ¢mera parada). Baixar com o ARCKHÉvox:
   `python3 baixar_v1.py --url "<URL>" --outdir ref/`
2. âš™ï¸ **Vestir o danÃ§arino** â€” `python3 kit/vestir.py ref/video.mp4 vestida.mp4`. O MediaPipe acha a pose e a
   silhueta de cada quadro e pinta camiseta e short. Por quÃª: o Kling **recusa** vÃ­deo de corpo que parece nu
   (`AGENT.FileCensorshipUnsafe`), e um **boneco de traÃ§os** (`kit/boneco.py`) passa na checagem mas falha com
   "No valid characters detected". Roupa pintada passa nas duas.
3. ðŸ¤– **Criar o bicho** em pÃ©, 9:16 â€” `kling text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 ...`
   (4 crÃ©ditos por 2 imagens). Escolher a que mostra o corpo inteiro com espaÃ§o em volta.
4. ðŸ¤– **Copiar a danÃ§a** â€” `kling motion_control --model kling-video-v3_0 --image bicho.png --video vestida.mp4
   --motionDirection motion_direction --resolution 720p`. No prompt, pedir "natural fur, no clothes" para a roupa
   da referÃªncia nÃ£o passar para o bicho.
5. âš™ï¸ **MÃºsica + fecho** â€” juntar o Ã¡udio da referÃªncia e rodar `python3 kit/fecho.py danca.mp4 final.mp4`:
   nos Ãºltimos 4,5 s o vÃ­deo escurece e o texto se escreve letra a letra
   ("construindo no / **ARCKHÉ AI** / baixa o kit", Montserrat Black, amarelo `#FACC15`).
6. ðŸ§  **Conferir a folha de quadros** antes de publicar (rosto, fundo, mÃ£os).
7. âš™ï¸ **Publicar** â€” YouTube pelo `yt-pubx --agendar` (um por hora) e Instagram/TikTok pelo Metricool.

Tudo de uma vez (passos 2â€“5):

```bash
kit/dancar.sh ref/video.mp4 capivara "chubby capybara diva with a pink feather boa and red lipstick"
```

## VersÃ£o grÃ¡tis com o Agnes

`kit/agnes_poses.py` (exemplo do porco): 1 imagem-Ã¢ncora + 3 poses derivadas dela (img2img, para ser o mesmo
bicho) + 3 clipes keyframe de 8 s indo de pose a pose em 9:16. Precisa do projeto `videos-agnes` e de
`AGNES_API_KEY`. Limite medido: num dos 3 clipes a cena desviou (fundo trocado, bicho de costas) â€” conferir a
folha e refazer sÃ³ o clipe torto.

![Poses Agnes](exemplos/agnes-poses.jpg)

## Arquivos

| Arquivo | O que faz |
|---|---|
| `kit/dancar.sh` | passos 2â€“5 numa chamada |
| `kit/vestir.py` | pinta roupa no danÃ§arino da referÃªncia (pose + mÃ¡scara MediaPipe) |
| `kit/boneco.py` | desenha um manequim de traÃ§os com a mesma danÃ§a (bom para estudar a coreografia) |
| `kit/fecho.py` | escurece o fim e escreve o texto do ARCKHÉ AI letra a letra |
| `kit/agnes_poses.py` | versÃ£o Agnes: poses + clipes keyframe |

Requisitos: `ffmpeg`, Python 3 com `mediapipe`, `opencv-python`, `pillow`; CLI `kling` logada
(`npm i -g @klingai/cli-global` + `kling login`). O modelo de pose (30 MB) baixa sozinho na 1Âª vez. O fecho usa `~/.local/share/fonts/Montserrat-Black.ttf` (Google Fonts, pasta `static/` do zip).

## Limites

- O Kling decide o que Ã© "personagem": traÃ§o puro nÃ£o conta; bicho fotorrealista em pÃ© conta.
- Pose do bicho importa: com a capivara "parada" (patas junto ao corpo) o Motion Control devolveu "No valid characters detected in the image" (sem cobranÃ§a); a mesma capivara em pose de danÃ§a (perna levantada, braÃ§os afastados) funcionou. Escolha a imagem com braÃ§os e pernas bem separados do corpo.
- Motion Control herda o enquadramento da referÃªncia; se o danÃ§arino sai do quadro, o bicho tambÃ©m sai.
- Login da CLI vence: `kling login` abre o navegador e espera sÃ³ 5 minutos pelo retorno.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
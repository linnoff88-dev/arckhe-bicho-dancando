# bicho-dancando

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![bicho-dancando](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## O que êÂ©

O bicho-dancando êÂ© um kit de scripts para quem faz vêÂ­deos curtos e quer um bicho danêÂ§ando igualzinho a um vêÂ­deo de referêÂªncia. VocêÂª dêÂ¡ um vêÂ­deo de alguêÂ©m danêÂ§ando e uma frase descrevendo o bicho; o kit pinta uma roupa no danêÂ§arino, cria a imagem do bicho em pêÂ© e manda o Kling (gerador de vêÂ­deo por IA) copiar os passos. No fim junta a mêÂºsica e um fecho com o texto do ARCKHê AI. Precisa de uma assinatura do Kling com a ferramenta de linha de comando instalada, Python e ffmpeg.

## ê°Å¸ââ Guia de uso

Guia completo (landing + passo a passo): **https://linnoff88-dev.github.io/

Kit para pegar a danêÂ§a de um vêÂ­deo e fazer **qualquer bicho** danêÂ§ar igual: porco, capivara, gatinha.
Usa o Kling pela assinatura (CLI `kling`) e, como alternativa grêÂ¡tis, o Agnes. Os scripts locais
(pose, roupa pintada, fecho) rodam na sua mêÂ¡quina, sem custo.

| VersêÂ£o | Como | Fidelidade aos passos | Custo medido (24 s, 720p) |
|---|---|---|---|
| **DanêÂ§a copiada** (recomendada) | referêÂªncia "vestida" + Kling Motion Control 3.0 | quase quadro a quadro | 216 crêÂ©ditos |
| Kling 4.0 por texto | imagem do bicho + coreografia descrita no prompt | passos livres | 240 crêÂ©ditos |
| Agnes | 4 poses + 3 clipes keyframe de 8 s | passos livres, pode desviar de cena | grêÂ¡tis (API Agnes) |

![Resultado](exemplos/resultado-porco.jpg)

## Exemplos em vêÂ­deo

Os trêÂªs bichos danêÂ§ando a mesma danêÂ§a (216 crêÂ©ditos cada):

- ê°Å¸ÂÂ· Porco de cabelo de cuia ê¢â¬â https://www.youtube.com/watch?v=3jfNlJ4DduI
- ê°Å¸Â¦Â« Capivara diva ê¢â¬â https://www.youtube.com/watch?v=opnakJZBDro
- ê°Å¸ÂÂ± Gatinha fofa ê¢â¬â https://www.youtube.com/watch?v=aivt5jwgGX4

## O processo, do inêÂ­cio ao fim

Legenda: ê°Å¸Â§Â  sessêÂ£o com o Nei êÂ· ê¢Å¡â¢ê¯Â¸Â script êÂ· ê°Å¸Â¤â serviêÂ§o de IA

1. ê°Å¸Â§Â  **Escolher o vêÂ­deo de referêÂªncia** (um danêÂ§arino de corpo inteiro, cêÂ¢mera parada). Baixar com o ARCKHêvox:
   `python3 baixar_v1.py --url "<URL>" --outdir ref/`
2. ê¢Å¡â¢ê¯Â¸Â **Vestir o danêÂ§arino** ê¢â¬â `python3 kit/vestir.py ref/video.mp4 vestida.mp4`. O MediaPipe acha a pose e a
   silhueta de cada quadro e pinta camiseta e short. Por quêÂª: o Kling **recusa** vêÂ­deo de corpo que parece nu
   (`AGENT.FileCensorshipUnsafe`), e um **boneco de traêÂ§os** (`kit/boneco.py`) passa na checagem mas falha com
   "No valid characters detected". Roupa pintada passa nas duas.
3. ê°Å¸Â¤â **Criar o bicho** em pêÂ©, 9:16 ê¢â¬â `kling text_to_image --model kling-image-v3_0_omni --aspect_ratio 9:16 ...`
   (4 crêÂ©ditos por 2 imagens). Escolher a que mostra o corpo inteiro com espaêÂ§o em volta.
4. ê°Å¸Â¤â **Copiar a danêÂ§a** ê¢â¬â `kling motion_control --model kling-video-v3_0 --image bicho.png --video vestida.mp4
   --motionDirection motion_direction --resolution 720p`. No prompt, pedir "natural fur, no clothes" para a roupa
   da referêÂªncia nêÂ£o passar para o bicho.
5. ê¢Å¡â¢ê¯Â¸Â **MêÂºsica + fecho** ê¢â¬â juntar o êÂ¡udio da referêÂªncia e rodar `python3 kit/fecho.py danca.mp4 final.mp4`:
   nos êÂºltimos 4,5 s o vêÂ­deo escurece e o texto se escreve letra a letra
   ("construindo no / **ARCKHê AI** / baixa o kit", Montserrat Black, amarelo `#FACC15`).
6. ê°Å¸Â§Â  **Conferir a folha de quadros** antes de publicar (rosto, fundo, mêÂ£os).
7. ê¢Å¡â¢ê¯Â¸Â **Publicar** ê¢â¬â YouTube pelo `yt-pubx --agendar` (um por hora) e Instagram/TikTok pelo Metricool.

Tudo de uma vez (passos 2ê¢â¬â5):

```bash
kit/dancar.sh ref/video.mp4 capivara "chubby capybara diva with a pink feather boa and red lipstick"
```

## VersêÂ£o grêÂ¡tis com o Agnes

`kit/agnes_poses.py` (exemplo do porco): 1 imagem-êÂ¢ncora + 3 poses derivadas dela (img2img, para ser o mesmo
bicho) + 3 clipes keyframe de 8 s indo de pose a pose em 9:16. Precisa do projeto `videos-agnes` e de
`AGNES_API_KEY`. Limite medido: num dos 3 clipes a cena desviou (fundo trocado, bicho de costas) ê¢â¬â conferir a
folha e refazer sêÂ³ o clipe torto.

![Poses Agnes](exemplos/agnes-poses.jpg)

## Arquivos

| Arquivo | O que faz |
|---|---|
| `kit/dancar.sh` | passos 2ê¢â¬â5 numa chamada |
| `kit/vestir.py` | pinta roupa no danêÂ§arino da referêÂªncia (pose + mêÂ¡scara MediaPipe) |
| `kit/boneco.py` | desenha um manequim de traêÂ§os com a mesma danêÂ§a (bom para estudar a coreografia) |
| `kit/fecho.py` | escurece o fim e escreve o texto do ARCKHê AI letra a letra |
| `kit/agnes_poses.py` | versêÂ£o Agnes: poses + clipes keyframe |

Requisitos: `ffmpeg`, Python 3 com `mediapipe`, `opencv-python`, `pillow`; CLI `kling` logada
(`npm i -g @klingai/cli-global` + `kling login`). O modelo de pose (30 MB) baixa sozinho na 1êÂª vez. O fecho usa `~/.local/share/fonts/Montserrat-Black.ttf` (Google Fonts, pasta `static/` do zip).

## Limites

- O Kling decide o que êÂ© "personagem": traêÂ§o puro nêÂ£o conta; bicho fotorrealista em pêÂ© conta.
- Pose do bicho importa: com a capivara "parada" (patas junto ao corpo) o Motion Control devolveu "No valid characters detected in the image" (sem cobranêÂ§a); a mesma capivara em pose de danêÂ§a (perna levantada, braêÂ§os afastados) funcionou. Escolha a imagem com braêÂ§os e pernas bem separados do corpo.
- Motion Control herda o enquadramento da referêÂªncia; se o danêÂ§arino sai do quadro, o bicho tambêÂ©m sai.
- Login da CLI vence: `kling login` abre o navegador e espera sêÂ³ 5 minutos pelo retorno.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>
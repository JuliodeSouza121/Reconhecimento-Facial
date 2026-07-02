# Como preparar as demos ao vivo

Este pacote tem as duas demonstrações do seminário: detecção de rostos
(Haar Cascade) e reconhecimento facial (face_recognition).

## Arquivos

```
demo1_deteccao_haar.py          -> Demo 1: detecção com Haar Cascade
demo2_reconhecimento_facial.py  -> Demo 2: reconhecimento facial personalizado
haarcascade_frontalface_default.xml -> classificador usado pela Demo 1 (já incluso)
known_faces/                    -> fotos usadas pela Demo 2 (já vem com obama.jpg e biden.jpg de exemplo)
requirements.txt                -> lista de dependências
```

## 1. Instalar as dependências

Abra o terminal na pasta deste projeto e rode:

```bash
pip install -r requirements.txt
```

### Se der erro ao instalar `face_recognition` (comum no Windows)

O `face_recognition` depende da biblioteca `dlib`, que precisa compilar
código em C++. Se o `pip install` travar ou der erro:

- **Windows**: instale o "Build Tools for Visual Studio" (C++ build tools)
  antes de tentar de novo, ou instale via conda:
  `conda install -c conda-forge dlib` e depois `pip install face_recognition`
- **Mac**: `brew install cmake` antes do pip install
- **Linux**: `sudo apt install cmake build-essential` antes do pip install

Faça esse teste com **alguns dias de antecedência**, não na véspera da
apresentação — a instalação do dlib é a parte mais instável do processo.

## 2. Testar a Demo 1 (detecção)

```bash
python demo1_deteccao_haar.py
```

Uma janela deve abrir mostrando sua câmera com um retângulo azul sobre
qualquer rosto detectado. Pressione `q` para fechar.

## 3. Personalizar a Demo 2 (reconhecimento) com sua própria foto

1. Tire uma foto de rosto (boa iluminação, olhando pra câmera, um único
   rosto na imagem funciona melhor).
2. Salve o arquivo dentro da pasta `known_faces/` com o seu nome, por
   exemplo `known_faces/joao.jpg` (o nome do arquivo vira o nome exibido
   na tela).
3. Se quiser, pode manter `obama.jpg` e `biden.jpg` na pasta também —
   assim, se alguém segurar uma foto do Obama na frente da câmera, o
   sistema também reconhece.
4. Rode:

```bash
python demo2_reconhecimento_facial.py
```

O script imprime no terminal quais rostos carregou. Ao abrir a câmera,
seu rosto deve aparecer com um retângulo **verde** e seu nome. Rostos
fora da base aparecem com retângulo **vermelho** e "Desconhecido".
Pressione `q` para fechar.

## 4. Dicas para o dia da apresentação

- Teste tudo (instalação + as duas demos) pelo menos um dia antes, no
  mesmo notebook que vai usar na sala.
- Feche outros programas que usem a câmera (Zoom, Teams, Meet) antes de
  rodar os scripts — só um programa pode usar a webcam por vez.
- Deixe o terminal com os dois comandos já digitados (ou em um script),
  pra não perder tempo buscando os arquivos ao vivo.
- Se a luz da sala for ruim, teste posicionar-se de frente para uma
  janela ou fonte de luz — isso melhora bastante a detecção.
- Tenha um plano B: grave um vídeo curto de cada demo funcionando, caso
  a câmera do projetor/sala falhe no dia.

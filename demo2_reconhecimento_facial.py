"""
DEMO 2 - Reconhecimento facial personalizado
Baseado em video2.py (Aula 06), com uma melhoria: em vez de fixar
Obama e Biden no código, este script carrega AUTOMATICAMENTE todas as
fotos que estiverem na pasta "known_faces/". O nome do arquivo vira o
nome exibido na tela.

Exemplo:
    known_faces/
        joao.jpg        -> vai aparecer "Joao"
        obama.jpg       -> vai aparecer "Obama"
        maria_silva.jpg -> vai aparecer "Maria Silva"

Requisitos:
    pip install opencv-python face_recognition numpy
    (face_recognition depende do dlib - veja README_DEMO.md se der erro
    na instalação)

Como rodar:
    1. Tire uma foto sua (rosto bem visível, boa iluminação, um único rosto)
    2. Salve como known_faces/seu_nome.jpg
    3. python demo2_reconhecimento_facial.py

Como sair:
    pressione a tecla "q" com a janela da câmera em foco
"""
import os
import cv2
import numpy as np
import face_recognition

KNOWN_FACES_DIR = "known_faces"


def carregar_base_conhecida(pasta):
    """Lê todas as imagens da pasta e gera o encoding (vetor de 128
    dimensões) de cada rosto encontrado. O nome do arquivo (sem extensão)
    vira o nome exibido."""
    encodings = []
    nomes = []

    if not os.path.isdir(pasta):
        print(f"Pasta '{pasta}' não encontrada. Crie-a e coloque fotos dentro.")
        return encodings, nomes

    extensoes_validas = (".jpg", ".jpeg", ".png")

    for arquivo in sorted(os.listdir(pasta)):
        if not arquivo.lower().endswith(extensoes_validas):
            continue

        caminho = os.path.join(pasta, arquivo)
        imagem = face_recognition.load_image_file(caminho)
        rostos = face_recognition.face_encodings(imagem)

        if len(rostos) == 0:
            print(f"Aviso: nenhum rosto encontrado em '{arquivo}', pulando.")
            continue

        nome = os.path.splitext(arquivo)[0].replace("_", " ").title()
        encodings.append(rostos[0])
        nomes.append(nome)
        print(f"Carregado: {nome}")

    return encodings, nomes


# Carrega a base de rostos conhecidos a partir da pasta known_faces/
known_face_encodings, known_face_names = carregar_base_conhecida(KNOWN_FACES_DIR)

if len(known_face_encodings) == 0:
    print("Nenhum rosto conhecido carregado. Adicione fotos em known_faces/ antes de continuar.")
    exit()

video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Não foi possível acessar a câmera. Verifique se ela está livre e conectada.")
    exit()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

falhas_seguidas = 0
MAX_FALHAS_SEGUIDAS = 30  # ~1 segundo de falhas antes de desistir de vez

while True:
    ret, frame = video_capture.read()
    if not ret:
        falhas_seguidas += 1
        print("Aviso: falha ao capturar frame da câmera, tentando novamente...")
        if falhas_seguidas >= MAX_FALHAS_SEGUIDAS:
            print("Falha persistente ao capturar frame da câmera. Encerrando.")
            break
        continue
    falhas_seguidas = 0

    # Processa 1 a cada 2 frames para manter a fluidez em tempo real
    if process_this_frame:
        # Reduz o frame para 1/4 do tamanho, acelera o processamento
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Converte de BGR (OpenCV) para RGB (face_recognition)
        # IMPORTANTE: usamos cv2.cvtColor (e não small_frame[:, :, ::-1]) porque
        # o slicing invertido gera um array "não contíguo" na memória, o que
        # faz o dlib falhar com "compute_face_descriptor(): incompatible
        # function arguments". cv2.cvtColor sempre retorna um array contíguo.
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

        # Detecta as posições dos rostos no frame
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Gera o encoding de cada rosto detectado
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compara o rosto do frame com toda a base conhecida
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconhecido"

            # Distância entre o rosto do frame e cada rosto da base
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Desenha o retângulo e o nome sobre cada rosto detectado
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Escala de volta ao tamanho original (o frame usado na detecção era 1/4)
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cor = (0, 200, 0) if name != "Desconhecido" else (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Reconhecimento Facial', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
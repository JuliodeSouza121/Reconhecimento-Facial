"""
DEMO 1 - Detecção de rostos com Haar Cascade
Baseado em video-2.py (Aula 05)

Requisitos:
    pip install opencv-python

Antes de rodar:
    - Coloque o arquivo 'haarcascade_frontalface_default.xml' na mesma pasta
      deste script (ele já vem com o OpenCV, veja instruções no README_DEMO.md)
    - Garanta que sua webcam está livre (feche Zoom, Teams, Meet, etc.)

Como rodar:
    python demo1_deteccao_haar.py

Como sair:
    pressione a tecla "q" com a janela da câmera em foco
"""
import cv2

# Carrega o classificador Haar Cascade para detecção de rostos
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Inicializa a captura de vídeo da câmera (0 para a câmera padrão)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Não foi possível acessar a câmera. Verifique se ela está livre e conectada.")
    exit()

while True:
    # Captura o frame da câmera
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da câmera.")
        break

    # Converte o frame para escala de cinza (recomendado para detecção com Haar Cascades)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta os rostos no frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Desenha retângulos ao redor dos rostos detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Mostra o frame original com os rostos detectados
    cv2.imshow('Deteccao de Rostos (Haar Cascade)', frame)

    # Aguarda por uma tecla de saída (tecla 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()

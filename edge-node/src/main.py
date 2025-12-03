import cv2
import threading
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask, Response

# --- CONFIGURACIÓN ---
BROKER_IP = "192.168.100.8"
TOPIC_ALERTAS = "camaras/rpi4/alertas"
UMBRAL_MOVIMIENTO = 1000

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

client = mqtt.Client()
try:
    client.connect(BROKER_IP, 1883, 60)
    client.loop_start()  # Inicia un hilo de fondo para la red
except:
    print("⚠️ No se pudo conectar")


def enviar_alerta(area):
    payload = {
        "nodo": "raspberry-pi-01",
        "evento": "MOVIMIENTO",
        "magnitud": area,
        "ts": time.time(),
    }
    client.publish(TOPIC_ALERTAS, json.dumps(payload))


# --- 2. Lógica de Video y Detección ---
def procesar_camara():
    global outputFrame, lock

    # Usamos índice 10 o -1 según tus pruebas
    cap = cv2.VideoCapture(0)
    time.sleep(2.0)  # Esperar a que la cámara caliente

    # Usamos un sustractor de fondo (Mejor que frame1 vs frame2)
    # Esto elimina el efecto "ghosting" y se adapta a cambios de luz
    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=500, varThreshold=50, detectShadows=False
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Reducir tamaño para velocidad (opcional)
        frame = cv2.resize(frame, (640, 480))

        # --- Detección de Movimiento ---
        mask = fgbg.apply(frame)
        # Limpiar ruido
        _, mask = cv2.threshold(mask, 244, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        hay_movimiento = False
        max_area = 0

        for c in contours:
            area = cv2.contourArea(c)
            if area > UMBRAL_MOVIMIENTO:
                hay_movimiento = True
                max_area = max(max_area, area)
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Enviar alerta (con control de flujo para no saturar)
        if hay_movimiento:
            # Aquí podrías poner un timer para no mandar 60 alertas por segundo
            enviar_alerta(max_area)

        # --- Actualizar frame para el Streaming ---
        with lock:
            outputFrame = frame.copy()

    cap.release()


# --- 3. Servidor Web para Streaming ---
def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            # Codificar a JPG
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue

        # Generar el flujo de bytes
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + bytearray(encodedImage) + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# --- MAIN ---
if __name__ == "__main__":
    # Arrancar el hilo de la cámara
    t = threading.Thread(target=procesar_camara)
    t.daemon = True
    t.start()

    # Arrancar el servidor web (Flask bloquea el main thread)
    print("🚀 Servidor de Video iniciado en puerto 5000")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

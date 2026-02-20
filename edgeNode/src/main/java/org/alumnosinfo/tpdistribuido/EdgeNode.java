package org.alumnosinfo.tpdistribuido;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;
import org.opencv.videoio.Videoio;

public class EdgeNode {
    static { nu.pattern.OpenCV.loadLocally(); }

    private static final String DEFAULT_HOST = "localhost";
    private static final int DEFAULT_PORT = 5555;
    private static final String CAM_ID = "CAM_01";

    // Configuración de Detección de Movimiento
    private static final double MIN_CONTOUR_AREA = 500.0; // Sensibilidad al tamaño del movimiento
    private static final int MOVEMENT_THRESHOLD = 25; // Sensibilidad al cambio de luz (0-255)

    // Estados
    private static volatile boolean isStreamingMode = false; // "false" = Modo Análisis, "true" = Modo Streaming

    public static void main(String[] args) {
        String host = (args.length > 0) ? args[0] : DEFAULT_HOST;
        
        System.out.println("🚀 Iniciando Edge Node - Modo Detección de Movimiento");

        VideoCapture camera = new VideoCapture(0);
        camera.set(Videoio.CAP_PROP_FRAME_WIDTH, 640);
        camera.set(Videoio.CAP_PROP_FRAME_HEIGHT, 480);

        if (!camera.isOpened()) {
            System.err.println("❌ Error: Cámara no detectada.");
            System.exit(1);
        }

        Mat frame = new Mat();
        Mat gray = new Mat();
        Mat prevGray = new Mat();
        Mat diff = new Mat();
        MatOfByte buffer = new MatOfByte();

        while (true) {
            try (Socket socket = new Socket(host, DEFAULT_PORT);
                 DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                 DataInputStream in = new DataInputStream(socket.getInputStream())) {

                System.out.println("✅ Conectado al Servidor Central.");
                out.writeUTF(CAM_ID); // Handshake

                // --- HILO DE ESCUCHA (SERVIDOR -> EDGE) ---
                // Escucha órdenes del servidor para volver a "Modo Análisis"
                Thread serverListener = new Thread(() -> {
                    try {
                        while (socket.isConnected()) {
                            // El servidor envía un booleano: true (ignorar) o false (DETENER STREAM)
                            // O un comando específico. Aquí asumiremos que si el servidor manda algo
                            // es para cambiar de estado.
                            String command = in.readUTF(); 
                            if ("STOP_STREAM".equals(command)) {
                                System.out.println("🛑 Orden recibida: Volviendo a Modo Análisis.");
                                isStreamingMode = false;
                            }
                        }
                    } catch (IOException e) {
                        System.out.println("⚠️ Hilo de escucha finalizado.");
                    }
                });
                serverListener.start();

                // --- BUCLE PRINCIPAL (EDGE PROCESSING) ---
                while (camera.read(frame)) {
                    if (frame.empty()) continue;

                    // 1. Convertir a Escala de Grises y Blur (para reducir ruido)
                    Imgproc.cvtColor(frame, gray, Imgproc.COLOR_BGR2GRAY);
                    Imgproc.GaussianBlur(gray, gray, new Size(21, 21), 0);

                    // Si es el primer frame, inicializamos y continuamos
                    if (prevGray.empty()) {
                        gray.copyTo(prevGray);
                        continue;
                    }

                    // 2. DETECCIÓN DE MOVIMIENTO (Modo Análisis)
                    // Calculamos la diferencia absoluta entre el frame actual y el anterior
                    Core.absdiff(prevGray, gray, diff);
                    Imgproc.threshold(diff, diff, MOVEMENT_THRESHOLD, 255, Imgproc.THRESH_BINARY);
                    Imgproc.dilate(diff, diff, new Mat(), new Point(-1, -1), 2);

                    List<MatOfPoint> contours = new ArrayList<>();
                    Mat hierarchy = new Mat();
                    Imgproc.findContours(diff, contours, hierarchy, Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

                    boolean motionDetected = false;
                    for (MatOfPoint contour : contours) {
                        if (Imgproc.contourArea(contour) > MIN_CONTOUR_AREA) {
                            motionDetected = true;
                            // Opcional: Dibujar rectángulo donde hubo movimiento
                            Rect rect = Imgproc.boundingRect(contour);
                            Imgproc.rectangle(frame, rect, new Scalar(0, 255, 0), 2);
                        }
                    }

                    // Actualizamos el frame anterior para la siguiente vuelta
                    gray.copyTo(prevGray);

                    // 3. LÓGICA DE ESTADOS
                    if (motionDetected && !isStreamingMode) {
                        System.out.println("⚠️ Movimiento detectado -> CAMBIO A MODO STREAMING");
                        isStreamingMode = true; 
                        // Nota: Aquí se queda en streaming hasta que el servidor diga "STOP"
                    }

                    // 4. ENVÍO (Solo si estamos en Modo Streaming)
                    if (isStreamingMode) {
                        Imgproc.putText(frame, "REC ●", new Point(20, 30), Imgproc.FONT_HERSHEY_SIMPLEX, 0.7, new Scalar(0, 0, 255), 2);
                        
                        Imgcodecs.imencode(".jpg", frame, buffer);
                        byte[] imageBytes = buffer.toArray();

                        // Sincronizamos para evitar colisión con el hilo de lectura si fuera necesario
                        synchronized (out) {
                            out.writeInt(imageBytes.length);
                            out.write(imageBytes);
                            out.flush();
                        }
                    } else {
                        // En Modo Análisis, ahorramos CPU y Red.
                        // Solo "vigilamos" localmente.
                        Thread.sleep(50); 
                    }
                }

            } catch (Exception e) {
                System.out.println("⚠️ Conexión perdida. Reintentando...");
                try { Thread.sleep(3000); } catch (Exception ex) {}
            }
        }
    }
}
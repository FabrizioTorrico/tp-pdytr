package org.alumnosinfo.tpdistribuido;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

public class CameraHandler implements Runnable {

    private final Socket socket;
    private DataOutputStream out; // Salida para enviar comandos al Edge

    public CameraHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try {
            DataInputStream in = new DataInputStream(socket.getInputStream());
            // Inicializamos el output stream para poder hablarle a la cámara
            this.out = new DataOutputStream(socket.getOutputStream());

            String camId = in.readUTF();
            System.out.println("✅ Cámara conectada: " + camId);

            long streamingStartTime = 0;
            boolean isReceivingStream = false;

            while (true) {
                // Leemos el tamaño de la imagen
                // NOTA: Esta lectura se bloqueará si la cámara está en "Modo Análisis" 
                // y no envía nada. Eso es correcto. El hilo del servidor espera pacientemente.
                int length = in.readInt();

                if (length > 0) {
                    byte[] imageBytes = new byte[length];
                    in.readFully(imageBytes);
                    FrameManager.setFrame(camId, imageBytes);

                    // Lógica de Ejemplo: Control de tiempo
                    if (!isReceivingStream) {
                        isReceivingStream = true;
                        streamingStartTime = System.currentTimeMillis();
                        System.out.println("🔴 " + camId + " ha comenzado a transmitir video.");
                    }

                    // SIMULACIÓN: Después de 10 segundos de video, el servidor ordena cortar.
                    // En la vida real, esto sería un botón en la Web UI que llama a un método.
                    if (System.currentTimeMillis() - streamingStartTime > 10000 && isReceivingStream) {
                        System.out.println("✋ Enviando orden de STOP a " + camId);
                        sendCommand("STOP_STREAM");
                        isReceivingStream = false; // Reseteamos flag local
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("❌ Cámara desconectada: " + e.getMessage());
        }
    }

    // Método síncrono para enviar comandos al Edge
    public synchronized void sendCommand(String command) {
        try {
            if (out != null) {
                out.writeUTF(command);
                out.flush();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
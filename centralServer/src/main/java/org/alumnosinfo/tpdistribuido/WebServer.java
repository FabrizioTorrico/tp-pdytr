package org.alumnosinfo.tpdistribuido;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;

public class WebServer implements Runnable {

    private final int port;

    public WebServer(int port) {
        this.port = port;
    }

    @Override
    public void run() {
        try {
            // El segundo parámetro (backlog) en 0 deja que el sistema decida
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            
            server.createContext("/stream", new StreamHandler());
            
            // Usar un ThreadPool para manejar múltiples espectadores simultáneos
            server.setExecutor(java.util.concurrent.Executors.newCachedThreadPool());
            server.start();
            
            System.out.println("🌐 Servidor Web iniciado en http://localhost:" + port);
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class StreamHandler implements HttpHandler {
        
        // Boundary estándar para MJPEG
        private static final String BOUNDARY = "--BoundaryString";

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // 1. Parsear Query Params de forma más limpia
            Map<String, String> queryParams = parseQuery(exchange.getRequestURI().getQuery());
            String targetCamId = queryParams.get("id");

            // 2. Validación estricta: Si no hay ID, error 400
            if (targetCamId == null || targetCamId.isEmpty()) {
                sendError(exchange, 400, "Falta el parametro ID (ej: /stream?id=cam1)");
                return;
            }

            // 3. Validación de existencia: Si la cámara no está conectada, error 404
            // NOTA: Es importante verificar esto al inicio, pero también manejar si se desconecta durante el stream
            if (!FrameManager.getCameraIds().contains(targetCamId)) {
                sendError(exchange, 404, "Camara no encontrada o desconectada: " + targetCamId);
                return;
            }

            System.out.println("Nuevo espectador conectado a: " + targetCamId);

            // 4. Configurar Cabeceras para MJPEG
            exchange.getResponseHeaders().set("Content-Type", "multipart/x-mixed-replace; boundary=" + BOUNDARY);
            exchange.getResponseHeaders().set("Cache-Control", "no-cache, private");
            exchange.sendResponseHeaders(200, 0);

            try (OutputStream os = exchange.getResponseBody()) {
                byte[] lastFrame = new byte[0]; 

                while (true) {
                    // Verificar si la cámara sigue viva
                    if (!FrameManager.getCameraIds().contains(targetCamId)) {
                        break; 
                    }

                    byte[] currentFrame = FrameManager.getFrame(targetCamId);

                    // OPTIMIZACIÓN: Solo enviar si el frame es válido y DIFERENTE al anterior
                    // (Arrays.equals es rápido para byte arrays, pero idealmente FrameManager debería dar un timestamp o ID de frame)
                    if (currentFrame != null && currentFrame.length > 0 && !Arrays.equals(currentFrame, lastFrame)) {
                        
                        // Escribir cabeceras del frame individual
                        os.write((BOUNDARY + "\r\n").getBytes());
                        os.write("Content-Type: image/jpeg\r\n".getBytes());
                        os.write(("Content-Length: " + currentFrame.length + "\r\n\r\n").getBytes());
                        
                        // Escribir imagen
                        os.write(currentFrame);
                        os.write("\r\n".getBytes());
                        os.flush();

                        lastFrame = currentFrame; 
                    }

                    // Sleep para controlar FPS y no saturar CPU
                    Thread.sleep(30); 
                }
            } catch (IOException e) {
                // El cliente (navegador) cerró la conexión, es normal.
                // No hace falta imprimir stacktrace
                System.out.println("Cliente desconectado de: " + targetCamId);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        // Helper para parsear queries
        private Map<String, String> parseQuery(String query) {
            if (query == null || query.isEmpty()) return java.util.Collections.emptyMap();
            return Arrays.stream(query.split("&"))
                    .map(param -> param.split("="))
                    .filter(parts -> parts.length == 2)
                    .collect(Collectors.toMap(parts -> parts[0], parts -> parts[1]));
        }

        // Helper para errores
        private void sendError(HttpExchange exchange, int code, String message) throws IOException {
            exchange.sendResponseHeaders(code, message.length());
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(message.getBytes());
            }
        }
    }
}
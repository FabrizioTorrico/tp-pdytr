package org.alumnosinfo.tpdistribuido;

import java.net.ServerSocket;
import java.net.Socket;

public class CentralServer {

    private static final int PORT_CAMERAS = 5555;
    private static final int PORT_WEB = 8081;

    public static void main(String[] args) throws Exception {
        System.out.println("==========================================");
        System.out.println("   CENTRAL SERVER - Cámaras Distribuidas  ");
        System.out.println("==========================================");

        try {
            ServerSocket serverSocket = new ServerSocket(PORT_CAMERAS);
            System.out.println("🎥 Escuchando Cámaras en puerto TCP: " + PORT_CAMERAS);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(new CameraHandler(clientSocket)).start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}

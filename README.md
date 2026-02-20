# TP Programación Distribuida y en Tiempo Real (PDyTR)

Este proyecto consiste en un sistema de videovigilancia distribuido e inteligente, compuesto por un **Servidor Central** y múltiples **Nodos de Borde (Edge Nodes)**.

El sistema implementa **Edge Computing**: los nodos procesan el video localmente para detectar movimiento. Solo cuando se detecta actividad relevante, inician la transmisión del stream al servidor, optimizando así el ancho de banda y el procesamiento.

## Estructura del Proyecto

- **centralServer**: Servidor TCP (recibe alertas/video) y Servidor Web (visualización en tiempo real).
- **edgeNode**: Cliente inteligente que realiza análisis de imagen (Detección de Movimiento) y transmite video bajo demanda.

## Requisitos Generales

- **Java 21** o superior.
- **Maven 3.6+**.
- **EdgeNode**: Requiere Webcam USB o cámara compatible con OpenCV.

---

## 1. Servidor Central (CentralServer)

El servidor tiene dos funciones principales:

1.  **Servidor TCP (Puerto 5555):** Escucha conexiones de los nodos.
2.  **Servidor Web (Puerto 8081):** Expone interfaz para visualizar las cámaras activas.

### Instalación y Compilación

Desde la carpeta raíz del proyecto:

```bash
cd centralServer
mvn clean package
```

### Ejecución

El servidor no requiere argumentos (puertos fijos: 5555 y 8081).

```bash
# Opción 1: Ejecutar con Java
java -cp target/centralServer-1.0-SNAPSHOT.jar org.alumnosinfo.tpdistribuido.CentralServer

# Opción 2: Ejecutar con Maven
mvn exec:java -Dexec.mainClass="org.alumnosinfo.tpdistribuido.CentralServer"
```

---

## 2. Nodo de Borde (EdgeNode)

Este nodo implementa lógica de visión artificial con **OpenCV**.

- **Modo Análisis (Default):** Procesa frames buscando cambios (movimiento) sin transmitir video.
- **Modo Streaming:** Al detectar movimiento, comienza a enviar el video al servidor central.

### Instalación

1.  Instalar dependencias del sistema (OpenCV/V4L):

    ```bash
    sudo apt-get update
    sudo apt-get install openjdk-21-jdk maven libv4l-dev
    ```

2.  Compilar:
    ```bash
    cd edgeNode
    mvn clean package
    ```

### Ejecución

El nodo acepta la IP del servidor como argumento único.

**Sintaxis:**

```bash
java -jar target/edgeNode-1.0-SNAPSHOT.jar [IP_SERVIDOR]
```

- `[IP_SERVIDOR]`: (Opcional) IP del Servidor Central. Defecto: `localhost`.
- _Nota: El Puerto está fijado en 5555 y el ID de cámara en `CAM_01` en esta versión._

**Ejemplos:**

1.  **Local:**

    ```bash
    java -jar target/edgeNode-1.0-SNAPSHOT.jar
    ```

2.  **Remoto:**
    ```bash
    java -jar target/edgeNode-1.0-SNAPSHOT.jar 192.168.1.100
    ```

> **NOTA:** Es obligatorio tener una cámara conectada. El programa terminará si no detecta video.

### Configuración de Autoinicio (Servicio Systemd)

Para que el nodo se ejecute automáticamente al encender la Raspberry Pi:

1.  **Preparar el script de inicio:**
    - Edita `edgeNode/start_node.sh` y configura la variable `SERVER_IP`.
    - Dale permisos de ejecución: `chmod +x edgeNode/start_node.sh`.

2.  **Configurar el servicio:**
    - Edita `edgeNode/edgenode.service`. Verifica las rutas y el usuario.
    - Copia el servicio: `sudo cp edgeNode/edgenode.service /etc/systemd/system/`.

3.  **Habilitar el servicio:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable edgenode.service
    ```

---

## 3. Visualización

1.  Asegúrate que el **CentralServer** esté corriendo.
2.  Asegúrate que al menos un **EdgeNode** esté corriendo y conectado (verás logs en el servidor: "Nuevo cliente conectado...").
3.  Abre un navegador web y ve a:

    http://localhost:8081/stream?id=cam1

    _(Reemplaza `cam1` por el ID que hayas configurado en el EdgeNode)._

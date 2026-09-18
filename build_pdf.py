import subprocess
import os
import sys

def build_pdf():
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Documentación Técnica - Sistema de Visión Computacional Distribuido</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {
    size: A4;
    margin: 14mm 15mm 15mm 15mm;
    @bottom-right {
      content: counter(page);
      font-size: 8pt;
      font-family: 'Inter', -apple-system, sans-serif;
      color: #94a3b8;
    }
    @bottom-left {
      content: "PDyTR — Cátedra de Programación Distribuida y Tiempo Real | UNLP";
      font-size: 8pt;
      font-family: 'Inter', -apple-system, sans-serif;
      color: #94a3b8;
    }
  }

  @page:first {
    margin: 0;
    @bottom-right { content: normal; }
    @bottom-left { content: normal; }
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    line-height: 1.44;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* PORTADA */
  .cover-page {
    page-break-after: always;
    height: 100vh;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }

  .cover-top-bar {
    height: 8px;
    background: linear-gradient(90deg, #1e3a8a 0%, #0284c7 100%);
    width: 100%;
  }

  .cover-content {
    padding: 65px 45px 30px 45px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .cover-institution {
    text-align: center;
    margin-bottom: 35px;
  }

  .cover-institution h2 {
    font-size: 13pt;
    font-weight: 800;
    color: #1e3a8a;
    letter-spacing: 1.5px;
    margin: 0 0 4px 0;
    text-transform: uppercase;
    border: none;
    padding: 0;
  }

  .cover-institution h3 {
    font-size: 9.5pt;
    font-weight: 700;
    color: #475569;
    letter-spacing: 1.2px;
    margin: 0 0 12px 0;
    text-transform: uppercase;
  }

  .cover-subject {
    display: inline-block;
    font-size: 8.5pt;
    font-weight: 600;
    color: #0284c7;
    background-color: #f0f9ff;
    border: 1px solid #bae6fd;
    padding: 4px 14px;
    border-radius: 20px;
  }

  .cover-main-title {
    text-align: center;
    margin: 25px 0;
  }

  .cover-main-title h1 {
    font-size: 19pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.3;
    margin: 0 0 12px 0;
  }

  .cover-subtitle {
    font-size: 9pt;
    color: #475569;
    line-height: 1.45;
    max-width: 520px;
    margin: 0 auto;
  }

  .cover-badge-container {
    text-align: center;
    margin: 12px 0;
  }

  .cover-badge {
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    color: #1e40af;
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 4px 14px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .cover-footer-box {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 15px;
  }

  .authors-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    text-align: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 10px;
    margin-bottom: 8px;
  }

  .author-label {
    font-size: 7pt;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
  }

  .author-name {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
  }

  .cover-meta {
    font-size: 7.2pt;
    color: #64748b;
    text-align: center;
  }

  .cover-meta span {
    color: #334155;
    font-weight: 600;
  }

  /* HEADINGS */
  h1.section-h1 {
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 3px;
    margin-top: 14px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }

  .page-break-section {
    page-break-before: always;
  }

  h2.section-h2 {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    page-break-after: avoid;
  }

  h2.section-h2::before {
    content: "";
    display: inline-block;
    width: 3px;
    height: 11px;
    background-color: #0284c7;
    margin-right: 5px;
    border-radius: 2px;
  }

  p {
    margin-top: 0;
    margin-bottom: 6px;
    text-align: justify;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 6px;
    padding-left: 16px;
  }

  li {
    margin-bottom: 2.5px;
    text-align: justify;
  }

  /* TABLA DE CONTENIDOS */
  .toc-box {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 10px 14px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }

  .toc-title {
    font-size: 9pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3px;
  }

  .toc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
  }

  .toc-table td {
    padding: 2px 0;
    border: none;
    background: transparent !important;
  }

  .toc-table td.toc-name {
    color: #334155;
  }

  .toc-table td.toc-sec {
    text-align: right;
    color: #64748b;
    font-weight: 600;
  }

  .toc-main-row td {
    font-weight: 700;
    color: #0f172a;
    padding-top: 3px;
  }

  /* TABLAS DE DATOS */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 7.8pt;
    page-break-inside: avoid;
  }

  table.data-table th, table.data-table td {
    border: 1px solid #cbd5e1;
    padding: 4px 7px;
    text-align: left;
    vertical-align: top;
  }

  table.data-table th {
    background-color: #1e293b;
    color: #ffffff;
    font-weight: 600;
  }

  table.data-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* CALLOUT BOXES */
  .callout-box {
    background-color: #eff6ff;
    border-left: 3.5px solid #2563eb;
    border-radius: 0 4px 4px 0;
    padding: 7px 10px;
    margin: 8px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }

  .callout-header {
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 3px;
  }

  /* DIAGRAMAS ESTILO FIGURA */
  .figure-container {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 8px;
    margin: 8px 0;
    page-break-inside: avoid;
  }

  .figure-caption {
    text-align: center;
    font-size: 7.2pt;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 6px;
  }

  /* DIAGRAMA 1: ARQUITECTURA */
  .arch-top-row {
    display: grid;
    grid-template-columns: 1.1fr 1.6fr 1.3fr;
    gap: 8px;
  }

  .arch-card {
    background: #ffffff;
    border-radius: 4px;
    padding: 6px;
    font-size: 7.2pt;
  }

  .card-web {
    border: 1.5px solid #38bdf8;
    background: #f0f9ff;
  }

  .card-server {
    border: 1.5px solid #818cf8;
    background: #eef2ff;
  }

  .card-edge {
    border: 1.5px solid #4ade80;
    background: #f0fdf4;
  }

  .card-header-title {
    font-weight: 700;
    text-align: center;
    padding-bottom: 3px;
    margin-bottom: 4px;
    border-bottom: 1px solid rgba(0,0,0,0.08);
    font-size: 7.2pt;
    text-transform: uppercase;
  }
  .card-web .card-header-title { color: #0369a1; }
  .card-server .card-header-title { color: #3730a3; }
  .card-edge .card-header-title { color: #166534; }

  .card-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 2.5px 4.5px;
    margin-bottom: 3px;
    font-size: 6.8pt;
    line-height: 1.22;
  }

  .card-item strong {
    color: #0f172a;
  }

  /* DIAGRAMA 2: MÁQUINA DE ESTADOS */
  .state-diagram-grid {
    display: grid;
    grid-template-columns: 1fr 115px 1fr;
    gap: 7px;
    align-items: center;
  }

  .state-card {
    background: #ffffff;
    border-radius: 4px;
    padding: 6px;
    font-size: 7.2pt;
  }

  .state-1 {
    border: 1.5px solid #0284c7;
    background: #f0f9ff;
  }

  .state-2 {
    border: 1.5px solid #16a34a;
    background: #f0fdf4;
  }

  .state-title {
    font-weight: 800;
    font-size: 7.5pt;
    text-align: center;
    padding: 2.5px;
    border-radius: 3px;
    margin-bottom: 5px;
    color: #ffffff;
  }
  .state-1 .state-title { background-color: #0284c7; }
  .state-2 .state-title { background-color: #16a34a; }

  .state-bullets {
    margin: 0;
    padding-left: 12px;
    font-size: 6.8pt;
    line-height: 1.3;
  }

  .state-badge-alert {
    background: #e0f2fe;
    color: #0369a1;
    font-weight: 700;
    font-size: 6.6pt;
    padding: 2.5px;
    text-align: center;
    border-radius: 3px;
    margin-top: 5px;
  }

  .state-badge-stream {
    background: #dcfce7;
    color: #15803d;
    font-weight: 700;
    font-size: 6.6pt;
    padding: 2.5px;
    text-align: center;
    border-radius: 3px;
    margin-top: 5px;
  }

  .state-arrows {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 6.5pt;
    text-align: center;
  }

  .arrow-box-right {
    background: #f1f5f9;
    border: 1px dashed #0284c7;
    border-radius: 3px;
    padding: 3px 2px;
    color: #0369a1;
    font-weight: 600;
    line-height: 1.15;
  }

  .arrow-box-left {
    background: #f1f5f9;
    border: 1px dashed #dc2626;
    border-radius: 3px;
    padding: 3px 2px;
    color: #b91c1c;
    font-weight: 600;
    line-height: 1.15;
  }

  /* CÓDIGO */
  code {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 7.6pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 2px;
    border: 1px solid #e2e8f0;
  }

  .code-block {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 7.2pt;
    line-height: 1.3;
    padding: 5px 8px;
    border-radius: 3px;
    margin: 4px 0;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
  }

  .code-block-light {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    color: #0f172a;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 7.2pt;
    line-height: 1.3;
    padding: 5px 7px;
    border-radius: 3px;
    margin: 4px 0;
    white-space: pre-wrap;
    page-break-inside: avoid;
  }

  .footer-meta-doc {
    text-align: center;
    font-size: 7.2pt;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    padding-top: 10px;
    margin-top: 25px;
    page-break-inside: avoid;
  }
</style>
</head>
<body>

<!-- PÁGINA 1: PORTADA -->
<div class="cover-page">
  <div class="cover-top-bar"></div>
  <div class="cover-content">
    <div class="cover-institution">
      <h2>Universidad Nacional de La Plata</h2>
      <h3>Facultad de Informática</h3>
      <div class="cover-subject">Programación Distribuida y Tiempo Real (PDyTR)</div>
    </div>

    <div class="cover-main-title">
      <h1>Sistema de Visión Computacional<br>Distribuido y Monitoreo Inteligente<br>en el Borde</h1>
      <div class="cover-subtitle">
        Documentación Técnica de Arquitectura, Virtualización con Vagrant, Aprovisionamiento y Módulos de Procesamiento en el Borde
      </div>
    </div>

    <div class="cover-badge-container">
      <div class="cover-badge">Informe Final de Entrega</div>
    </div>

    <div class="cover-footer-box">
      <div class="authors-grid">
        <div>
          <div class="author-label">Autor / Desarrollador</div>
          <div class="author-name">Nicolas Ricciardi</div>
        </div>
        <div>
          <div class="author-label">Autor / Desarrollador</div>
          <div class="author-name">Fabrizio Torrico</div>
        </div>
      </div>
      <div class="cover-meta">
        Fecha: <span>Agosto de 2026</span> &nbsp;|&nbsp; Versión: <span>1.0 Final</span> &nbsp;|&nbsp; Tecnologías: <span>Java 21, OpenCV, Vagrant, VirtualBox, React + Vite</span>
      </div>
    </div>
  </div>
</div>

<!-- PÁGINAS DE CONTENIDO -->
<div class="content-page">

  <!-- ÍNDICE GENERAL -->
  <div class="toc-box">
    <div class="toc-title">Índice General del Documento</div>
    <table class="toc-table">
      <tr class="toc-main-row">
        <td class="toc-name">1. Funcionamiento General del Sistema</td>
        <td class="toc-sec">Sección 1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;1.1. Propósito y Paradigma de Edge Computing</td>
        <td class="toc-sec">1.1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;1.2. Diagrama de Arquitectura Global</td>
        <td class="toc-sec">1.2</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;1.3. Componentes Principales</td>
        <td class="toc-sec">1.3</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;1.4. Máquina de Estados de los Nodos Edge</td>
        <td class="toc-sec">1.4</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;1.5. Protocolo de Comunicación de Red</td>
        <td class="toc-sec">1.5</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">2. Estrategia de Virtualización y Aprovisionamiento</td>
        <td class="toc-sec">Sección 2</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;2.1. Arquitectura de Red y Virtualización</td>
        <td class="toc-sec">2.1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;2.2. Aprovisionamiento vs. Despliegue en Producción</td>
        <td class="toc-sec">2.2</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">3. Documentación del Vagrantfile y Dependencias</td>
        <td class="toc-sec">Sección 3</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;3.1. Configuración Base Global</td>
        <td class="toc-sec">3.1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;3.2. Sección del Servidor Central (central_server)</td>
        <td class="toc-sec">3.2</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;3.3. Secciones de los Nodos de Borde (edge_node_1 y edge_node_2)</td>
        <td class="toc-sec">3.3</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">4. Virtualización y Módulos del Nodo de Borde (edgeNode)</td>
        <td class="toc-sec">Sección 4</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;4.1. Fuentes que Corren en los Edges</td>
        <td class="toc-sec">4.1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;4.2. Instalación y Modalidades de Ejecución</td>
        <td class="toc-sec">4.2</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">5. Virtualización y Módulos del Servidor Central (centralServer)</td>
        <td class="toc-sec">Sección 5</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;5.1. Fuentes que Corren en el Servidor</td>
        <td class="toc-sec">5.1</td>
      </tr>
      <tr>
        <td class="toc-name">&nbsp;&nbsp;&nbsp;&nbsp;5.2. Instalación y Ejecución del Servidor</td>
        <td class="toc-sec">5.2</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">6. Integración con el Cliente Web Dashboard (webClient)</td>
        <td class="toc-sec">Sección 6</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">7. Resumen Consolidado de Dependencias y Requisitos</td>
        <td class="toc-sec">Sección 7</td>
      </tr>
      <tr class="toc-main-row">
        <td class="toc-name">8. Guía de Verificación y Puesta en Marcha</td>
        <td class="toc-sec">Sección 8</td>
      </tr>
    </table>
  </div>

  <!-- SECCIÓN 1 -->
  <h1 class="section-h1">1. Funcionamiento General del Sistema</h1>

  <h2 class="section-h2">1.1. Propósito y Paradigma de Edge Computing</h2>
  <p>El sistema implementa una arquitectura distribuida de videovigilancia orientada a la <strong>optimización del uso de ancho de banda en la red y del procesamiento central</strong>, dando cumplimiento a los requerimientos del trabajo final de la cátedra de Programación Distribuida y Tiempo Real (PDyTR).</p>

  <p>En concordancia con las definiciones metodológicas fijadas en las reuniones de seguimiento de la bitácora, se mantiene estricta consistencia en la terminología empleada: los términos <em>"Edge"</em> y <em>"Nodo de Borde"</em> representan conceptualmente el cómputo en el extremo de la red (implementado tanto sobre una <strong>Raspberry Pi 4B</strong> física como sobre máquinas virtuales Linux), mientras que <em>"Central Server"</em> y <em>"Back End"</em> corresponden al servidor centralizador.</p>

  <p>En los esquemas convencionales de CCTV, todas las cámaras transmiten de forma ininterrumpida flujos de video completos hacia un servidor central, lo que satura los canales de comunicación y genera cuellos de botella de procesamiento. Para mitigar esta problemática, el presente proyecto aplica el paradigma de <strong>Edge Computing (Computación en el Borde)</strong>:</p>

  <ul>
    <li><strong>Definición de Video "de Interés":</strong> Siguiendo el alcance delimitado por la cátedra, se define video de interés estrictamente como <strong>video con identificación de movimiento</strong>. Los nodos de borde transmiten hacia el servidor central <em>únicamente</em> cuando se discrimina movimiento local en la escena vigilada.</li>
    <li><strong>Procesamiento en el Borde:</strong> Cada nodo de borde analiza localmente las imágenes capturadas utilizando técnicas de visión por computadora livianas implementadas con OpenCV.</li>
    <li><strong>Silencio de Red (Ahorro de Recursos):</strong> Mientras no se registre actividad en la escena, los nodos no transmiten video por la red, permaneciendo en estado de análisis local silencioso.</li>
    <li><strong>Transmisión Conducida por Eventos:</strong> Al detectarse movimiento relevante (o ante la petición explícita de un operador desde el cliente web), el nodo conmuta a modo de transmisión activa y envía los fotogramas comprimidos mediante un socket TCP hacia el Servidor Central.</li>
    <li><strong>Procesamiento Central y Distribución:</strong> El Servidor Central recibe los fotogramas, aplica algoritmos de sustracción y marcado para delimitar visualmente el movimiento con recuadros verdes y leyendas de alerta, gestiona temporizadores de inactividad para ordenar el retorno al modo silencioso cuando cesa la actividad, y expone los flujos de video mediante MJPEG y APIs REST hacia el Dashboard web.</li>
    <li><strong>Topología Distribuida:</strong> El sistema opera con al menos 2 nodos edge concurrentes (un nodo real sobre Raspberry Pi 4 y nodos simulados/virtualizados en PC mediante Vagrant).</li>
  </ul>

  <h2 class="section-h2">1.2. Diagrama de Arquitectura Global</h2>

  <div class="figure-container">
    <div class="arch-top-row">
      <!-- CLIENTE WEB -->
      <div class="arch-card card-web">
        <div class="card-header-title">CLIENTE WEB (DASHBOARD)</div>
        <div class="card-item"><strong>React 18 + Vite UI</strong><br>Panel de Control y Monitoreo</div>
        <div class="card-item"><strong>API Polling (500ms)</strong><br>Consulta de estado y cámaras</div>
        <div class="card-item"><strong>Visor MJPEG Stream</strong><br>Renderizado directo en &lt;img&gt;</div>
      </div>

      <!-- SERVIDOR CENTRAL -->
      <div class="arch-card card-server">
        <div class="card-header-title">SERVIDOR CENTRAL (:5555 / :8081)</div>
        <div class="card-item"><strong>TcpServer &amp; CameraSession (:5555)</strong><br>Sesiones multihilo y buffers acotados</div>
        <div class="card-item"><strong>CameraRegistry (ConcurrentHashMap)</strong><br>Estado de cámaras y canales de comando</div>
        <div class="card-item"><strong>FrameProcessor (OpenCV Anotador)</strong><br>Marcado de movimiento y bounding boxes</div>
        <div class="card-item"><strong>InactivityMonitor (Watchdog 60s)</strong><br>Envío automático de orden TCP STOP</div>
        <div class="card-item"><strong>WebServer REST &amp; MJPEG (:8081)</strong><br>APIs /api/* y streaming de video</div>
      </div>

      <!-- NODOS EDGE -->
      <div class="arch-card card-edge">
        <div class="card-header-title">NODOS EDGE (BORDE)</div>
        <div class="card-item"><strong>Edge Node 1 (CAM_01)</strong><br>IP: 192.168.56.20 (RPi 4 / VM)<br>MotionDetector + StreamClient TCP</div>
        <div class="card-item"><strong>Edge Node 2 (CAM_02)</strong><br>IP: 192.168.56.21 (VM Linux)<br>MotionDetector + StreamClient TCP</div>
      </div>
    </div>
    <div class="figure-caption">Figura 1: Arquitectura Distribuida y Flujos de Comunicación del Sistema</div>
  </div>

  <h2 class="section-h2">1.3. Componentes Principales</h2>
  <ul>
    <li><strong>Nodos de Borde (<code>edgeNode</code>):</strong> Capturan video desde dispositivos de captura física (webcam USB vía V4L2) o archivos de video de prueba, ejecutan el algoritmo de detección de movimiento local en memoria y transmiten fotogramas únicamente bajo demanda o detección confirmada.</li>
    <li><strong>Servidor Central (<code>centralServer</code>):</strong> Orquestador multihilo que administra las conexiones TCP de las cámaras, desacopla la recepción mediante colas acotadas anti-lag (capacidad 5), anota fotogramas resaltando áreas en movimiento, supervisa la inactividad y sirve la API REST y los streams MJPEG.</li>
    <li><strong>Cliente Web (<code>webClient</code>):</strong> Single Page Application construida en React + Vite que proporciona un panel de monitoreo y control en tiempo real.</li>
  </ul>

  <h2 class="section-h2">1.4. Máquina de Estados de los Nodos Edge</h2>
  <p>Cada nodo de borde implementa una máquina de estados finita estrictamente excluyente con dos modos de funcionamiento (establecidos junto a la cátedra el 02/02/26):</p>

  <div class="figure-container">
    <div class="state-diagram-grid">
      <!-- ESTADO 1 -->
      <div class="state-card state-1">
        <div class="state-title">ESTADO 1: MONITOREO LOCAL</div>
        <ul class="state-bullets">
          <li>Captura continua de frames (30 FPS)</li>
          <li>Conversión Grayscale + GaussianBlur(21,21)</li>
          <li>Diferencia absoluta (absdiff) + Threshold</li>
          <li>Dilatación + Búsqueda de contornos</li>
        </ul>
        <div class="state-badge-alert">🔒 CERO EMISIÓN DE RED (Ahorro Ancho de Banda)<br><small>Si no hay movimiento: Sleep preventivo de 50ms</small></div>
      </div>

      <!-- FLECHAS Y TRANSICIONES -->
      <div class="state-arrows">
        <div class="arrow-box-right">
          <strong>Movimiento detectado</strong><br>(Área &gt; 500 px²)<br>o Comando 'START' &rarr;
        </div>
        <div class="arrow-box-left">
          &larr; <strong>Comando 'STOP'</strong><br>(Timeout inactividad 60s<br>o Dashboard Web)
        </div>
      </div>

      <!-- ESTADO 2 -->
      <div class="state-card state-2">
        <div class="state-title">ESTADO 2: TRANSMISIÓN ACTIVA</div>
        <ul class="state-bullets">
          <li>Compresión JPEG en memoria (imencode)</li>
          <li>Envío de longitud (4 Bytes) por Socket TCP</li>
          <li>Transmisión secuencial del byte array JPG</li>
          <li>Servidor Central dibuja bounding boxes</li>
        </ul>
        <div class="state-badge-stream">📡 TRANSMISIÓN TCP CONTINUA ACTIVA<br><small>Al retornar a Estado 1: reset de frame previo</small></div>
      </div>
    </div>
    <div class="figure-caption">Figura 2: Máquina de Estados y Transiciones del Nodo de Borde</div>
  </div>

  <p><strong>Justificación del Algoritmo en el Edge (Visión Clásica vs. YOLO):</strong> Durante la fase de prototipado se evaluaron modelos de redes neuronales (YOLOv5 Nano) sobre la CPU de la Raspberry Pi 4B. Las mediciones mostraron una degradación crítica del rendimiento a ~5 FPS y un consumo excesivo de CPU/temperatura. Siguiendo las directivas docentes, se consolidó el algoritmo clásico determinístico con OpenCV (diferencia de fotogramas sucesivos, desenfoque gaussiano y análisis de contornos), lo cual asegura una tasa fluida y estable de <strong>~30 FPS</strong> con mínimo consumo computacional.</p>

  <h2 class="section-h2">1.5. Protocolo de Comunicación de Red</h2>
  <ol>
    <li><strong>Handshake Inicial:</strong> El nodo Edge abre una conexión TCP hacia el puerto 5555 del Servidor Central y transmite como primer dato una cadena UTF-8 con su identificador único (<code>camId</code>). El servidor registra el socket asociado a dicha identidad e IP.</li>
    <li><strong>Trama de Video Binaria:</strong> En el Estado 2, cada fotograma se transmite estructurado en dos partes:
      <ul>
        <li><strong>Encabezado de Tamaño:</strong> Entero de 4 bytes (formato Big-Endian / <code>writeInt</code>) indicando la longitud en bytes del fotograma JPEG.</li>
        <li><strong>Carga Útil (Payload):</strong> Arreglo de bytes crudos de la imagen JPEG (<code>write(imageBytes)</code>).</li>
      </ul>
    </li>
    <li><strong>Canal de Control Bidireccional sobre TCP:</strong> Conforme a la reunión del 08/04/26, se descartó el uso de servidores HTTP en el edge para simplificar el nodo y ahorrar recursos. A través del mismo socket TCP ya establecido, el Servidor Central envía cadenas de comando UTF-8:
      <ul>
        <li><code>START</code>: Ordena al Edge conmutar inmediatamente al Estado 2 (Streaming).</li>
        <li><code>STOP</code>: Ordena al Edge conmutar inmediatamente al Estado 1 (Monitoreo silencioso).</li>
      </ul>
    </li>
    <li><strong>API REST y Streaming MJPEG Web:</strong>
      <ul>
        <li><code>GET /api/cameras</code>: Retorna un JSON con la lista de cámaras registradas, direcciones IP y estado booleano de streaming.</li>
        <li><code>GET /api/start?id=CAM_ID</code> y <code>GET /api/stop?id=CAM_ID</code>: Control manual remoto desde el dashboard.</li>
        <li><code>GET /stream?id=CAM_ID</code>: Flujo de video continuo con cabecera <code>multipart/x-mixed-replace; boundary=--BoundaryString</code> compatible con elementos estándar HTML.</li>
      </ul>
    </li>
  </ol>

  <!-- SECCIÓN 2 -->
  <h1 class="section-h1">2. Estrategia de Virtualización y Aprovisionamiento</h1>

  <h2 class="section-h2">2.1. Arquitectura de Red y Virtualización</h2>
  <p>Para garantizar el aislamiento de procesos y total reproducibilidad en la evaluación del sistema (según lo conversado en la bitácora respecto a no utilizar Docker sino máquinas virtuales completas), la solución se virtualiza utilizando <strong>Vagrant</strong> sobre el hipervisor <strong>Oracle VirtualBox</strong>. La topología está configurada con una Red Privada (Host-Only Network) bajo el rango <code>192.168.56.0/24</code>:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th>Máquina Virtual</th>
        <th>Hostname</th>
        <th>IP Privada</th>
        <th>Servicios y Puertos</th>
        <th>Recursos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong><code>central_server</code></strong></td>
        <td><code>centralserver</code></td>
        <td><code>192.168.56.10</code></td>
        <td>TCP :5555 (Video/Comandos)<br>HTTP :8081 (Forwarded a Host:8081)</td>
        <td>1 CPU, 1024 MB RAM</td>
      </tr>
      <tr>
        <td><strong><code>edge_node_1</code></strong></td>
        <td><code>edgenode1</code></td>
        <td><code>192.168.56.20</code></td>
        <td>Cliente TCP hacia 192.168.56.10:5555<br>Controlador USB habilitado</td>
        <td>1 CPU, 1024 MB RAM</td>
      </tr>
      <tr>
        <td><strong><code>edge_node_2</code></strong></td>
        <td><code>edgenode2</code></td>
        <td><code>192.168.56.21</code></td>
        <td>Cliente TCP hacia 192.168.56.10:5555<br>Controlador USB habilitado</td>
        <td>1 CPU, 1024 MB RAM</td>
      </tr>
    </tbody>
  </table>

  <h2 class="section-h2">2.2. Aprovisionamiento vs. Despliegue en Producción</h2>

  <div class="callout-box">
    <div class="callout-header">📌 Nota Técnica sobre el Modelo de Entrega y Aprovisionamiento (Reunión del 08/04/26)</div>
    <p>En la configuración de Vagrant de este proyecto, el directorio del repositorio en la máquina anfitriona se monta automáticamente en el punto <code>/vagrant</code> dentro de cada máquina virtual mediante carpetas compartidas.</p>
    <p>Durante la etapa de <strong>aprovisionamiento (<code>provision shell</code>)</strong>, se instalan los paquetes del sistema operativo base (Ubuntu 22.04 LTS), OpenJDK 21, Apache Maven y utilidades de video. Inmediatamente a continuación, el aprovisionamiento ingresa a la carpeta compartida correspondiente (<code>/vagrant/centralServer</code> o <code>/vagrant/edgeNode</code>) y compila el código fuente ejecutando <code>mvn clean compile</code>, generando asimismo los scripts ejecutables de inicio (<code>start_central.sh</code> y <code>start_edge.sh</code>).</p>
    <p style="margin-bottom: 0;"><strong>Aclaración de Diseño:</strong> Se explicita que compilar el código fuente dentro del script de aprovisionamiento de una máquina virtual no representa un proceso de despliegue productivo estándar (donde se generarían artefactos inmutables precompilados, imágenes de contenedor o paquetes Debian versionados). Para los fines de esta entrega académica, este mecanismo garantiza máxima <strong>transparencia, reproducibilidad y verificación directa</strong> de la compilación y ejecución del código fuente sin requerir binarios pesados en el repositorio.</p>
  </div>

  <!-- SECCIÓN 3 -->
  <h1 class="section-h1">3. Documentación del Vagrantfile y Dependencias</h1>
  <p>El archivo de configuración <code>Vagrantfile</code> define de forma declarativa toda la infraestructura virtual y sus dependencias explícitas:</p>

  <h2 class="section-h2">3.1. Configuración Base Global</h2>
  <p>Se utiliza la imagen oficial <code>ubuntu/jammy64</code> (Ubuntu Server 22.04 LTS de 64 bits), proveyendo un entorno Linux homogéneo y estable para la ejecución de Java 21 y la manipulación de dispositivos de video.</p>

  <h2 class="section-h2">3.2. Sección del Servidor Central (<code>central_server</code>)</h2>
  <ul>
    <li><strong>Red y Puertos:</strong> IP estática privada <code>192.168.56.10</code> y redirección del puerto <code>8081</code> del huésped hacia el puerto <code>8081</code> del anfitrión para permitir el acceso del dashboard web en React.</li>
    <li><strong>Hardware Virtual:</strong> 1 núcleo vCPU y 1024 MB de memoria RAM.</li>
    <li><strong>Dependencias Explícitas de Aprovisionamiento:</strong> <code>openjdk-21-jdk</code> y <code>maven</code>.</li>
    <li><strong>Compilación y Script de Inicio:</strong> Ejecuta <code>mvn clean compile</code> en <code>/vagrant/centralServer</code> y crea el script ejecutable <code>/home/vagrant/start_central.sh</code>.</li>
  </ul>

  <h2 class="section-h2">3.3. Secciones de los Nodos de Borde (<code>edge_node_1</code> y <code>edge_node_2</code>)</h2>
  <ul>
    <li><strong>Red:</strong> IPs estáticas privadas <code>192.168.56.20</code> y <code>192.168.56.21</code>.</li>
    <li><strong>Controladores USB en VirtualBox:</strong> Activa los flags <code>--usb on</code>, <code>--usbehci on</code> y <code>--usbxhci on</code> para permitir el passthrough de cámaras físicas USB 2.0 y 3.0 hacia la máquina virtual.</li>
    <li><strong>Hardware Virtual:</strong> 1 núcleo vCPU y 1024 MB de memoria RAM por cada nodo.</li>
    <li><strong>Dependencias Explícitas de Aprovisionamiento:</strong> <code>openjdk-21-jdk</code>, <code>maven</code> y <code>v4l-utils</code> (Video4Linux2).</li>
    <li><strong>Compilación y Script de Inicio Parametrizado:</strong> Ejecuta <code>mvn clean compile</code> en <code>/vagrant/edgeNode</code> y genera <code>/home/vagrant/start_edge.sh</code> admitiendo parámetros para seleccionar el índice de cámara física (<code>0</code>, <code>1</code>) o la ruta a un archivo de video simulado.</li>
  </ul>

  <!-- SECCIÓN 4 -->
  <h1 class="section-h1">4. Virtualización y Módulos del Nodo de Borde (<code>edgeNode</code>)</h1>

  <h2 class="section-h2">4.1. Fuentes que Corren en los Edges</h2>
  <p>Los módulos de software que componen el nodo de borde se ubican en el paquete <code>org.alumnosinfo.tpdistribuido</code> dentro de la carpeta <code>edgeNode/</code>:</p>

  <ul>
    <li><strong><code>EdgeNode.java</code>:</strong> Orquestador principal del nodo. Carga dinámicamente las librerías nativas de OpenCV (<code>nu.pattern.OpenCV.loadLocally()</code>), procesa los argumentos de ejecución (IP del servidor, ID de cámara y fuente de video), gestiona la reconexión automática ante caídas de red, computa y reporta métricas periódicas de FPS, y coordina el bucle de captura y streaming.</li>
    <li><strong><code>EdgeStateManager.java</code>:</strong> Modela el estado operativo del nodo de borde de forma segura para hilos mediante variables marcadas con <code>volatile</code> (<code>streamingMode</code> y <code>resetPrevGray</code>), asegurando sincronización inmediata entre el hilo de comandos TCP y el hilo de captura de video.</li>
    <li><strong><code>MotionDetector.java</code>:</strong> Implementa el algoritmo de visión por computadora para detección de movimiento en el borde. Transforma la imagen a escala de grises, aplica desenfoque gaussiano de 21 x 21, efectúa sustracción de fondo absoluta (<code>absdiff</code>), binariza por umbral y dilata la imagen. Confirma detección si el área de algún contorno excede los 500 píxeles cuadrados.</li>
    <li><strong><code>StreamClient.java</code>:</strong> Administra el socket TCP cliente. Ejecuta el apretón de manos inicial, mantiene un hilo escucha para comandos remotos (<code>START</code> / <code>STOP</code>), y en el modo de transmisión comprime los fotogramas a JPEG y los envía con enmarcado de longitud de 4 bytes en bloques sincronizados.</li>
    <li><strong><code>VideoSource.java</code>:</strong> Capa de abstracción para la captura de video que soporta indistintamente dispositivos físicos (V4L2 en Linux) y archivos de video pregrabados (<code>.mp4</code>). Para archivos de video, implementa rebobinado automático al final de la pista para simulación continua.</li>
    <li><strong><code>pom.xml</code>:</strong> Define las dependencias de Maven del nodo, incluyendo <code>org.openpnp:opencv:4.9.0-0</code> y el plugin <code>maven-shade-plugin</code> para empaquetado autónomo.</li>
    <li><strong><code>edgenode.service</code>:</strong> Archivo de configuración para registrar el nodo como un servicio administrado por <strong>systemd</strong> en dispositivos físicos independientes (como Raspberry Pi OS).</li>
  </ul>

  <h2 class="section-h2">4.2. Instalación y Modalidades de Ejecución</h2>
  <ul>
    <li><strong>Aprovisionamiento en la VM:</strong> Realizado automáticamente al ejecutar <code>vagrant up</code>.</li>
    <li><strong>Ejecución con Cámara Física:</strong> Habiendo capturado el dispositivo USB en VirtualBox, se ejecuta <code>./start_edge.sh 0</code> dentro de la VM.</li>
    <li><strong>Ejecución con Video Simulado:</strong> Se pasa como argumento la ruta al archivo de video: <code>./start_edge.sh /vagrant/videos/prueba.mp4</code>.</li>
  </ul>

  <!-- SECCIÓN 5 -->
  <h1 class="section-h1">5. Virtualización y Módulos del Servidor Central (<code>centralServer</code>)</h1>

  <h2 class="section-h2">5.1. Fuentes que Corren en el Servidor</h2>
  <p>Los módulos de software del Servidor Central se encuentran en la carpeta <code>centralServer/</code>:</p>

  <ul>
    <li><strong><code>CentralServer.java</code>:</strong> Punto de entrada del servidor. Carga librerías nativas de OpenCV, inicializa el <code>CameraRegistry</code>, inicia el <code>InactivityMonitor</code>, y levanta el servidor HTTP (:8081) y el servidor TCP (:5555) en hilos dedicados.</li>
    <li><strong><code>CameraRegistry.java</code>:</strong> Estructura de datos thread-safe (<code>ConcurrentHashMap</code>) que centraliza el estado de las cámaras: últimos fotogramas procesados, IPs, flujos de salida para comandos, y marcas temporales de último frame y último movimiento registrado.</li>
    <li><strong><code>TcpServer.java</code> y <code>CameraSession.java</code>:</strong> Servidor de sockets TCP multihilo. Por cada nodo conectado crea una sesión que encola los fotogramas entrantes en un búfer acotado (<code>LinkedBlockingQueue(5)</code>) descartando frames obsoletos ante saturación para eliminar la latencia acumulada (lag).</li>
    <li><strong><code>FrameProcessor.java</code>:</strong> Hilo de procesamiento de imagen que desencola frames, detecta contornos con movimiento, dibuja cuadros delimitadores verdes, estampa la leyenda <code>MOVIMIENTO DETECTADO</code> en texto rojo y actualiza el registro central con el fotograma anotado.</li>
    <li><strong><code>InactivityMonitor.java</code>:</strong> Tarea periódica programada cada 10 segundos que audita las cámaras activas. Si transcurren más de 60 segundos sin registrarse movimiento en la escena, emite automáticamente la orden TCP <code>STOP</code> para apagar la transmisión del nodo.</li>
    <li><strong>Subpaquete Web (WebServer y Handlers):</strong>
      <ul>
        <li><code>WebServer.java</code>: Servidor HTTP embebido en el puerto 8081 con pool de hilos en caché.</li>
        <li><code>BaseHttpHandler.java</code>: Manejador base con soporte para cabeceras CORS y resolución de solicitudes OPTIONS.</li>
        <li><code>CamerasApiHandler.java</code>: Endpoint <code>GET /api/cameras</code> que lista las cámaras y su estado en JSON.</li>
        <li><code>CommandApiHandler.java</code>: Endpoints <code>GET /api/start</code> y <code>GET /api/stop</code> para control remoto.</li>
        <li><code>StreamHandler.java</code>: Endpoint <code>GET /stream?id=CAM_ID</code> con streaming MJPEG <code>multipart/x-mixed-replace</code>.</li>
        <li><code>CameraDto.java</code>: Objeto de transferencia de datos para serialización JSON.</li>
      </ul>
    </li>
    <li><strong><code>pom.xml</code>:</strong> Define la compilación con Java 21 y la dependencia de OpenCV.</li>
  </ul>

  <h2 class="section-h2">5.2. Instalación y Ejecución del Servidor</h2>
  <p>El aprovisionamiento de Vagrant instala Java 21 y Maven, compila el proyecto y deja listo el script <code>/home/vagrant/start_central.sh</code>. Para iniciar el servidor dentro de la máquina virtual:</p>

  <div class="code-block-light"><strong>Comandos de Inicio del Servidor Central:</strong>
vagrant ssh central_server
./start_central.sh</div>

  <!-- SECCIÓN 6 -->
  <h1 class="section-h1">6. Integración con el Cliente Web Dashboard (<code>webClient</code>)</h1>
  <p>El cliente web es una aplicación desarrollada en <strong>React + Vite</strong> ubicada en <code>webClient/</code>:</p>

  <ul>
    <li><strong>Monitoreo en Tiempo Real:</strong> Consulta periódicamente <code>GET /api/cameras</code> para listar nodos conectados y su estado.</li>
    <li><strong>Reproducción MJPEG:</strong> Incrusta el stream de video directamente en etiquetas <code>&lt;img src="http://localhost:8081/stream?id=CAM_ID" /&gt;</code>.</li>
    <li><strong>Control Remoto:</strong> Permite forzar el inicio o la detención de cualquier cámara mediante peticiones a <code>/api/start</code> y <code>/api/stop</code>.</li>
    <li><strong>Ejecución en Host:</strong> Se instala y ejecuta en la máquina anfitriona con <code>npm install &amp;&amp; npm run dev</code>, accediendo en <code>http://localhost:5173</code>.</li>
  </ul>

  <!-- SECCIÓN 7 -->
  <h1 class="section-h1">7. Resumen Consolidado de Dependencias y Requisitos</h1>

  <table class="data-table">
    <thead>
      <tr>
        <th>Componente</th>
        <th>Software / Herramienta</th>
        <th>Versión</th>
        <th>Función en el Sistema</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Virtualización</strong></td>
        <td>Vagrant</td>
        <td>&ge; 2.3</td>
        <td>Definición y aprovisionamiento automatizado de las VMs</td>
      </tr>
      <tr>
        <td><strong>Hipervisor</strong></td>
        <td>Oracle VirtualBox</td>
        <td>&ge; 6.1 / 7.0</td>
        <td>Ejecución de VMs y emulación de controladores USB</td>
      </tr>
      <tr>
        <td><strong>Sistema Huésped</strong></td>
        <td>Ubuntu Server</td>
        <td>22.04 LTS</td>
        <td>Sistema operativo base en todas las máquinas virtuales</td>
      </tr>
      <tr>
        <td><strong>Lenguaje</strong></td>
        <td>OpenJDK</td>
        <td>21</td>
        <td>Compilación y ejecución de aplicaciones Java</td>
      </tr>
      <tr>
        <td><strong>Construcción</strong></td>
        <td>Apache Maven</td>
        <td>&ge; 3.8</td>
        <td>Gestión de dependencias y ciclo de vida de compilación</td>
      </tr>
      <tr>
        <td><strong>Visión Artificial</strong></td>
        <td>OpenCV (OpenPnP)</td>
        <td>4.9.0-0</td>
        <td>Procesamiento de imágenes y algoritmos de detección</td>
      </tr>
      <tr>
        <td><strong>Captura Linux</strong></td>
        <td>v4l-utils / V4L2</td>
        <td>Nativo</td>
        <td>Control y captura de dispositivos de video en Linux</td>
      </tr>
      <tr>
        <td><strong>Frontend Web</strong></td>
        <td>React + Vite (Node.js)</td>
        <td>Node &ge; 18</td>
        <td>Dashboard interactivo de usuario y visualización</td>
      </tr>
    </tbody>
  </table>

  <!-- SECCIÓN 8: SALTO DE PÁGINA PARA PÁGINA 7 -->
  <h1 class="section-h1 page-break-section">8. Guía de Verificación y Puesta en Marcha</h1>

  <h2 class="section-h2">8.1. Despliegue Automatizado con Vagrant (Recomendado)</h2>
  <ol>
    <li><strong>Levantar la Infraestructura Virtual (en la raíz del proyecto):</strong>
      <div class="code-block">vagrant up</div>
    </li>
    <li><strong>Iniciar el Servidor Central (Terminal 1):</strong>
      <div class="code-block">vagrant ssh central_server &rarr; ./start_central.sh</div>
    </li>
    <li><strong>Iniciar el Edge Node 1 (Terminal 2):</strong>
      <div class="code-block">vagrant ssh edge_node_1 &rarr; ./start_edge.sh 0 (o con ruta a video)</div>
    </li>
    <li><strong>Iniciar el Edge Node 2 (Terminal 3):</strong>
      <div class="code-block">vagrant ssh edge_node_2 &rarr; ./start_edge.sh 0 (o con ruta a video)</div>
    </li>
    <li><strong>Iniciar el Dashboard Web en el Host (Terminal 4):</strong>
      <div class="code-block">cd webClient &rarr; npm run dev &rarr; Abrir http://localhost:5173</div>
    </li>
  </ol>

  <h2 class="section-h2">8.2. Ejecución Nativa en Host (Sin Virtualización)</h2>
  <ol>
    <li><strong>Servidor Central:</strong>
      <div class="code-block">cd centralServer &amp;&amp; mvn exec:java -Dexec.mainClass="org.alumnosinfo.tpdistribuido.CentralServer"</div>
    </li>
    <li><strong>Edge Node 1:</strong>
      <div class="code-block">cd edgeNode &amp;&amp; mvn exec:java -Dexec.mainClass="org.alumnosinfo.tpdistribuido.EdgeNode" -Dexec.args="localhost CAM_01 0"</div>
    </li>
    <li><strong>Edge Node 2:</strong>
      <div class="code-block">cd edgeNode &amp;&amp; mvn exec:java -Dexec.mainClass="org.alumnosinfo.tpdistribuido.EdgeNode" -Dexec.args="localhost CAM_02 1"</div>
    </li>
    <li><strong>Web Client:</strong>
      <div class="code-block">cd webClient &amp;&amp; npm run dev</div>
    </li>
  </ol>

  <div class="footer-meta-doc">
    Documentación Técnica Final — Cátedra de Programación Distribuida y Tiempo Real (PDyTR)<br>
    Autores: Nicolas Ricciardi &amp; Fabrizio Torrico — Facultad de Informática, UNLP — Agosto 2026
  </div>

</div>

</body>
</html>
"""

    html_path = os.path.abspath("temp_doc.html")
    pdf_path = os.path.abspath("Documentacion_Sistema_PDyTR.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and os.path.exists(pdf_path):
        print(f"PDF generado: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    else:
        print("Error:", result.stderr)

    if os.path.exists(html_path):
        os.remove(html_path)

if __name__ == "__main__":
    build_pdf()

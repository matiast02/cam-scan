# IP Scanner - Multi-Port Scanner for IP Cameras, DVR & NVR

Herramienta profesional de escaneo de red para identificar cámaras IP, DVR y NVR con vulnerabilidades de seguridad, especialmente aquellos con credenciales por defecto.

## Características

- **Escaneo Multi-Puerto**: Detecta múltiples servicios (RTSP, HTTP, ONVIF, protocolos propietarios)
- **Identificación Automática**: Reconoce fabricantes (Hikvision, Dahua, Axis, etc.)
- **Prueba de Credenciales**: Verifica credenciales por defecto conocidas
- **Escaneo Paralelo**: Utiliza multi-threading para escaneos rápidos
- **Reportes Detallados**: Genera reportes con URLs listas para usar
- **Modular y Extensible**: Arquitectura modular para fácil mantenimiento

## Protocolos Soportados

- **RTSP** (554, 8554, 555, 7447)
- **HTTP/HTTPS** (80, 443, 8080, 8081, 8000, 9000, 5000)
- **ONVIF** (3702)
- **Dahua Propietario** (37777, 37778)
- **DVR Genéricos** (34567, 6036, 7001)
- **RTMP** (1935)

## Estructura del Proyecto

```
ip_scanner/
├── config/                 # Configuraciones
│   ├── __init__.py
│   ├── ports.py           # Definición de puertos
│   ├── credentials.py     # Base de datos de credenciales
│   └── paths.py           # Rutas RTSP comunes
├── protocols/             # Manejadores de protocolos
│   ├── __init__.py
│   ├── http_handler.py    # HTTP/HTTPS
│   ├── rtsp_handler.py    # RTSP
│   ├── onvif_handler.py   # ONVIF
│   ├── dahua_handler.py   # Dahua propietario
│   └── dvr_handler.py     # DVR genéricos
├── scanner/               # Lógica de escaneo
│   ├── __init__.py
│   ├── device_scanner.py  # Escaneo de dispositivos
│   ├── network_scanner.py # Escaneo de red
│   └── identifier.py      # Identificación de fabricantes
├── utils/                 # Utilidades
│   ├── __init__.py
│   ├── network_utils.py   # Funciones de red
│   └── output_utils.py    # Formateo de salida
├── main.py               # Script principal
└── README.md             # Este archivo
```

## Instalación

### Requisitos

- Python 3.6 o superior
- Módulos estándar de Python (no requiere dependencias externas)

### Instalación desde el código fuente

```bash
# Clonar o descargar el proyecto
cd ip_scanner

# Opcional: Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# No se requieren dependencias adicionales
```

## Uso

### Sintaxis Básica

```bash
python3 main.py [OPTIONS]
```

### Opciones

| Opción | Descripción | Valor por defecto |
|--------|-------------|-------------------|
| `-n, --network` | Red a escanear (ej: 192.168.1.0/24) | Red local auto |
| `-p, --ports` | Puertos específicos separados por comas | Todos |
| `--preset` | Preset predefinido (critical/rtsp/http/proprietary/all) | all |
| `-t, --timeout` | Timeout de escaneo en segundos | 1 |
| `-a, --auth-timeout` | Timeout de autenticación en segundos | 3 |
| `-w, --workers` | Número de hilos concurrentes | 20 |

### Ejemplos de Uso

#### 1. Escaneo Completo de Red Local

```bash
python3 main.py
```

Escanea automáticamente tu red local con todos los puertos configurados.

#### 2. Escaneo Rápido (Solo Puertos Críticos)

```bash
python3 main.py --preset critical
```

Escanea solo los puertos más importantes para mayor velocidad.

#### 3. Solo Puertos RTSP

```bash
python3 main.py --preset rtsp
```

Busca únicamente servicios RTSP.

#### 4. Solo Puertos HTTP/Web

```bash
python3 main.py --preset http
```

Busca únicamente interfaces web.

#### 5. Puertos Específicos

```bash
python3 main.py --ports 554,8554,37777,3702
```

Escanea solo los puertos especificados.

#### 6. Red Específica

```bash
python3 main.py -n 192.168.0.0/24
```

Escanea una red específica en lugar de la red local.

#### 7. Escaneo Rápido con Más Hilos

```bash
python3 main.py -n 192.168.0.0/24 -w 50 --preset critical
```

Utiliza 50 hilos para un escaneo más rápido de puertos críticos.

#### 8. Escaneo Detallado con Timeouts Largos

```bash
python3 main.py -t 2 -a 5
```

Aumenta los timeouts para redes lentas o dispositivos que responden lentamente.

## Presets Disponibles

| Preset | Descripción | Puertos |
|--------|-------------|---------|
| `critical` | Puertos más importantes | 554, 8554, 8000, 37777, 34567, 80, 3702 |
| `rtsp` | Solo RTSP | 554, 8554, 555, 7447 |
| `http` | Solo HTTP/HTTPS | 80, 443, 8080, 8081, 8000, 9000, 5000 |
| `proprietary` | Protocolos propietarios | 37777, 37778, 34567, 6036, 7001 |
| `all` | Todos los puertos | Todos los configurados |

## Ejemplo de Salida

```
================================================================================
  ESCÁNER MULTI-PUERTO PARA CÁMARAS IP Y DVR
================================================================================
[*] Tu IP local: 192.168.1.50
[*] Red a escanear: 192.168.1.0/24
[*] Puertos a escanear: 17

[*] Escaneando red: 192.168.1.0/24
[*] Puertos a escanear: 17
[*] Timeout escaneo: 1s | Auth: 3s
[*] Hilos: 20
[*] Total IPs: 256
[*] Iniciado: 2025-01-15 10:30:00

================================================================================
Puertos:
    80 - HTTP       - Web estándar
   554 - RTSP       - RTSP estándar
  3702 - ONVIF      - ONVIF Discovery
 37777 - DAHUA      - Dahua DVR/NVR
================================================================================

🟢 192.168.1.100    - Hikvision        - 4 puerto(s) - 3 accesible(s)
🟢 192.168.1.101    - Dahua            - 3 puerto(s) - 2 accesible(s)
🔵 192.168.1.102    - ONVIF Compatible - 2 puerto(s) - 0 accesible(s)

[*] Escaneo completado en 45.23s

================================================================================
  RESUMEN DEL ESCANEO
================================================================================
Total dispositivos encontrados: 3
Dispositivos VULNERABLES: 2
Dispositivos PROTEGIDOS: 1

Distribución por fabricante:
  - Hikvision: 1
  - Dahua: 1
  - ONVIF Compatible: 1

================================================================================
  ⚠️  DISPOSITIVOS VULNERABLES ⚠️
================================================================================

┌─ 192.168.1.100 (camera-01.local)
├─ Fabricante: Hikvision
├─ Puertos accesibles:
│
│  ┌─ Puerto 554 (RTSP)
│  ├─ Descripción: RTSP estándar
│  ├─ Servidor: RTSP Server
│  ├─ Usuario: admin
│  ├─ Password: 12345
│  ├─ Fabricante sugerido: Hikvision
│  └─ URL: rtsp://admin:12345@192.168.1.100:554/Streaming/Channels/101
│     Path: /Streaming/Channels/101
└──────────────────────────────────────────────────────────────────────────────
```

## Seguridad y Uso Responsable

⚠️ **ADVERTENCIA IMPORTANTE**:

Esta herramienta está diseñada para:
- Auditorías de seguridad autorizadas
- Pruebas en redes propias
- Identificación de vulnerabilidades en infraestructuras propias
- Fines educativos

**NO USAR** para:
- Acceder a redes sin autorización
- Actividades ilegales o maliciosas
- Comprometer la seguridad de sistemas ajenos

El uso indebido de esta herramienta puede ser ilegal en tu jurisdicción.

## Recomendaciones de Seguridad

Si encuentras dispositivos vulnerables en tu red:

1. **Cambiar contraseñas inmediatamente** - Usar contraseñas fuertes y únicas
2. **Deshabilitar servicios innecesarios** - Cerrar puertos no utilizados
3. **Configurar firewall** - Segmentar red y limitar accesos
4. **Actualizar firmware** - Mantener dispositivos actualizados
5. **Deshabilitar acceso desde Internet** - Nunca exponer cámaras directamente
6. **Usar VPN** - Para acceso remoto seguro
7. **Monitorear accesos** - Revisar logs regularmente

## Extender la Herramienta

### Agregar Nuevas Credenciales

Edita `config/credentials.py`:

```python
DEFAULT_CREDENTIALS = [
    ("nuevo_usuario", "nueva_password", "Fabricante"),
    # ... más credenciales
]
```

### Agregar Nuevos Puertos

Edita `config/ports.py`:

```python
DEFAULT_PORTS = {
    9999: {'protocol': 'NUEVO', 'description': 'Descripción'},
    # ... más puertos
}
```

### Agregar Nuevas Rutas RTSP

Edita `config/paths.py`:

```python
RTSP_PATHS = [
    "/nueva/ruta",
    # ... más rutas
]
```

### Crear Nuevo Manejador de Protocolo

1. Crea un nuevo archivo en `protocols/`
2. Implementa la función de prueba
3. Importa en `protocols/__init__.py`
4. Úsalo en `scanner/device_scanner.py`

## Solución de Problemas

### Error: "No se pudo detectar la red local"

- Verifica tu conexión de red
- Usa `-n` para especificar manualmente: `-n 192.168.1.0/24`

### Escaneo muy lento

- Reduce el número de puertos: `--preset critical`
- Aumenta hilos: `-w 50`
- Reduce timeout: `-t 0.5 -a 2`

### No encuentra dispositivos conocidos

- Aumenta timeout: `-t 2 -a 5`
- Verifica que los dispositivos estén en la red correcta
- Algunos dispositivos pueden no responder a ciertos puertos

### Errores de permisos en Linux

```bash
sudo python3 main.py
```

## Salida de Archivos

Los resultados se guardan automáticamente en:

```
scan_vulnerable_YYYYMMDD_HHMMSS.txt
```

Ejemplo: `scan_vulnerable_20250115_103045.txt`

## Contribuir

Para contribuir al proyecto:

1. Agrega nuevos protocolos en `protocols/`
2. Agrega credenciales conocidas en `config/credentials.py`
3. Mejora la detección de fabricantes en `scanner/identifier.py`
4. Reporta bugs y sugerencias

## Licencia

Este proyecto es solo para fines educativos y de auditoría de seguridad autorizada.

## Disclaimer

El autor no se hace responsable del uso indebido de esta herramienta. Úsala solo en redes y sistemas donde tengas autorización expresa.

---

**Última actualización**: 2025-01-15
**Versión**: 1.0.0

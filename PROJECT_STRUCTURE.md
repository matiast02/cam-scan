# Estructura del Proyecto IP Scanner

## Vista General

```
ip_scanner/
├── config/                    # Módulos de configuración
│   ├── __init__.py           # Exporta configuraciones principales
│   ├── ports.py              # Definición de puertos y presets
│   ├── credentials.py        # Base de datos de credenciales por defecto
│   └── paths.py              # Rutas RTSP comunes por fabricante
│
├── protocols/                 # Manejadores de protocolos
│   ├── __init__.py           # Exporta todos los handlers
│   ├── http_handler.py       # Maneja HTTP/HTTPS
│   ├── rtsp_handler.py       # Maneja RTSP
│   ├── onvif_handler.py      # Maneja ONVIF discovery
│   ├── dahua_handler.py      # Protocolo propietario Dahua
│   └── dvr_handler.py        # Protocolo DVR genérico
│
├── scanner/                   # Lógica de escaneo
│   ├── __init__.py           # Exporta funciones de escaneo
│   ├── device_scanner.py     # Escaneo de dispositivos individuales
│   ├── network_scanner.py    # Escaneo de redes completas
│   └── identifier.py         # Identificación de fabricantes
│
├── utils/                     # Utilidades
│   ├── __init__.py           # Exporta utilidades
│   ├── network_utils.py      # Funciones de red (scan_port, get_hostname, etc.)
│   └── output_utils.py       # Formateo y presentación de resultados
│
├── examples/                  # Ejemplos de uso
│   └── custom_scan.py        # Scripts de ejemplo personalizados
│
├── __init__.py               # Inicialización del paquete
├── main.py                   # Punto de entrada principal
├── setup.py                  # Configuración de instalación
├── requirements.txt          # Dependencias (ninguna externa)
├── .gitignore               # Archivos a ignorar en git
├── LICENSE                   # Licencia MIT
├── README.md                # Documentación principal
├── USAGE.md                 # Guía de uso detallada
└── PROJECT_STRUCTURE.md     # Este archivo
```

## Descripción de Módulos

### 1. Config (config/)

**Propósito**: Centralizar todas las configuraciones del scanner.

- **ports.py**: Define todos los puertos a escanear y sus características
  - `DEFAULT_PORTS`: Diccionario con puertos y metadatos
  - `PORT_PRESETS`: Presets predefinidos (critical, rtsp, http, etc.)

- **credentials.py**: Base de datos de credenciales conocidas
  - `DEFAULT_CREDENTIALS`: Lista de tuplas (user, pass, manufacturer)

- **paths.py**: Rutas RTSP comunes
  - `RTSP_PATHS`: Lista de rutas comunes
  - `RTSP_PATHS_BY_MANUFACTURER`: Rutas específicas por fabricante

### 2. Protocols (protocols/)

**Propósito**: Implementar lógica específica para cada protocolo.

Cada handler sigue el mismo patrón:
```python
def test_PROTOCOL(ip, port, username, password, timeout=3):
    """
    Returns: (success, status, details)
    """
```

- **http_handler.py**: Prueba autenticación HTTP Basic
- **rtsp_handler.py**: Prueba autenticación RTSP
- **onvif_handler.py**: Descubrimiento WS-Discovery
- **dahua_handler.py**: Protocolo binario Dahua
- **dvr_handler.py**: Protocolo DVR genérico chino

### 3. Scanner (scanner/)

**Propósito**: Coordinar el escaneo de dispositivos y redes.

- **device_scanner.py**:
  - `scan_single_port()`: Escanea un puerto específico
  - `scan_device()`: Escanea todos los puertos de un dispositivo
  - Funciones internas `_test_*_port()` para cada tipo de protocolo

- **network_scanner.py**:
  - `scan_network()`: Escanea toda una red usando ThreadPoolExecutor
  - Coordina el escaneo paralelo de múltiples dispositivos

- **identifier.py**:
  - `identify_manufacturer()`: Identifica fabricante basándose en servicios

### 4. Utils (utils/)

**Propósito**: Funciones de utilidad reutilizables.

- **network_utils.py**:
  - `get_local_network()`: Detecta automáticamente la red local
  - `scan_port()`: Verifica si un puerto está abierto
  - `get_hostname()`: Obtiene hostname de una IP

- **output_utils.py**:
  - `display_results()`: Muestra resultados formateados
  - `print_scan_header()`: Imprime cabecera de escaneo
  - `print_device_found()`: Imprime dispositivo encontrado
  - Funciones internas para guardar archivos y advertencias

### 5. Main (main.py)

**Propósito**: Punto de entrada de la aplicación.

- Parseo de argumentos CLI
- Coordinación de alto nivel
- Manejo de errores y excepciones

## Flujo de Datos

```
main.py
  │
  ├─► parse_arguments() → Obtiene opciones CLI
  │
  ├─► determine_network() → Detecta o usa red especificada
  │     └─► utils.get_local_network()
  │
  ├─► determine_ports() → Selecciona puertos a escanear
  │     └─► config.DEFAULT_PORTS / PORT_PRESETS
  │
  └─► scan_network() → Escanea la red
        │
        ├─► ThreadPoolExecutor → Múltiples hilos
        │
        └─► Para cada IP:
              └─► scan_device()
                    │
                    └─► Para cada puerto:
                          └─► scan_single_port()
                                │
                                ├─► network_utils.scan_port() → ¿Está abierto?
                                │
                                └─► protocols.test_*() → Probar autenticación
                                      │
                                      ├─► test_http_auth()
                                      ├─► test_rtsp_auth()
                                      ├─► test_onvif_discovery()
                                      ├─► test_dahua_protocol()
                                      └─► test_generic_dvr()
```

## Patrones de Diseño Utilizados

### 1. Separation of Concerns
- Cada módulo tiene una responsabilidad única y bien definida
- Configuración separada de lógica de negocio
- Protocolos aislados en handlers individuales

### 2. Strategy Pattern
- Diferentes estrategias para probar diferentes protocolos
- Cada protocol handler implementa la misma interfaz conceptual

### 3. Factory Pattern
- `determine_ports()` actúa como factory para crear configuraciones de puertos
- Presets como configuraciones predefinidas

### 4. Thread Pool Pattern
- `ThreadPoolExecutor` para escaneo paralelo eficiente
- Número configurable de workers

## Extensibilidad

### Agregar un Nuevo Protocolo

1. Crear nuevo handler en `protocols/`:
```python
# protocols/nuevo_handler.py
def test_nuevo_protocolo(ip, port, username, password, timeout=3):
    """Implementación del nuevo protocolo"""
    return (success, status, details)
```

2. Exportar en `protocols/__init__.py`:
```python
from .nuevo_handler import test_nuevo_protocolo
__all__ = [..., 'test_nuevo_protocolo']
```

3. Usar en `scanner/device_scanner.py`:
```python
elif protocol == 'NUEVO':
    result = _test_nuevo_port(ip, port, result, timeout_auth)

def _test_nuevo_port(ip, port, result, timeout):
    from ..protocols import test_nuevo_protocolo
    success, status, details = test_nuevo_protocolo(ip, port, timeout=timeout)
    # ... procesar resultado
```

4. Agregar puertos en `config/ports.py`:
```python
DEFAULT_PORTS = {
    9999: {'protocol': 'NUEVO', 'description': 'Nuevo protocolo'},
}
```

### Agregar Nuevo Preset

En `config/ports.py`:
```python
PORT_PRESETS = {
    'mi_preset': [554, 8000, 37777],
}
```

### Agregar Nueva Funcionalidad de Salida

En `utils/output_utils.py`:
```python
def export_to_csv(devices):
    """Nueva función de exportación"""
    pass
```

## Dependencias

### Internas (Python Standard Library)
- `socket`: Comunicación de red
- `ipaddress`: Manejo de direcciones IP
- `concurrent.futures`: Threading
- `argparse`: CLI parsing
- `datetime`: Timestamps
- `base64`: Encoding
- `xml.etree.ElementTree`: Parseo XML (ONVIF)
- `http.client`: Cliente HTTP

### Externas
- Ninguna (100% Python estándar)

## Testing

Para probar el código modular:

```python
# test_example.py
from ip_scanner.protocols import test_http_auth

result = test_http_auth("192.168.1.100", 80, "admin", "admin")
print(result)
```

## Performance

### Optimizaciones Implementadas
- **Threading**: Escaneo paralelo de múltiples IPs
- **Timeouts configurables**: Evitar bloqueos en dispositivos no responsivos
- **Early return**: Detener pruebas al encontrar credenciales válidas
- **Presets**: Reducir puertos a escanear cuando sea apropiado

### Características de Rendimiento
- ~20 IPs/segundo con preset `critical` y 20 workers
- ~5 IPs/segundo con todos los puertos y autenticación completa
- Escalable hasta 100+ workers para redes grandes

## Seguridad del Código

### Medidas Implementadas
- No ejecuta código remoto
- Solo lectura (no modifica dispositivos)
- Timeouts para prevenir DoS accidental
- Manejo de excepciones robusto
- No almacena credenciales permanentemente

### Advertencias
- Los archivos de resultados contienen credenciales en texto plano
- Proteger adecuadamente `scan_vulnerable_*.txt`
- No compartir resultados sin sanitizar

## Mantenimiento

### Actualizar Credenciales
Editar `config/credentials.py`

### Actualizar Puertos
Editar `config/ports.py`

### Actualizar Rutas RTSP
Editar `config/paths.py`

### Mejorar Identificación
Editar `scanner/identifier.py`

## Roadmap Futuro

Posibles mejoras:
- [ ] Soporte para autenticación Digest
- [ ] Base de datos SQLite para resultados
- [ ] Interfaz web (dashboard)
- [ ] Exportación a múltiples formatos (CSV, JSON, XML)
- [ ] Integración con API de vulnerability databases
- [ ] Modo pasivo (solo detección sin autenticación)
- [ ] Soporte para IPv6
- [ ] Plugin system para protocolos custom

---

**Versión**: 1.0.0
**Fecha**: 2025-01-15
**Autor**: Security Research

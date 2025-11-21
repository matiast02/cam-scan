# Guía de Instalación - IP Scanner

## Instalación Rápida

### Linux / macOS

```bash
# 1. Descargar o clonar el proyecto
cd /path/to/ip_scanner

# 2. Dar permisos de ejecución
chmod +x main.py

# 3. Ejecutar
python3 main.py --help
```

### Windows

```cmd
# 1. Navegar al directorio
cd C:\path\to\ip_scanner

# 2. Ejecutar
python main.py --help
```

## Instalación como Paquete

### Instalación en modo desarrollo

```bash
cd ip_scanner
pip install -e .
```

Después de esto, puedes ejecutar desde cualquier lugar:
```bash
ip-scanner --help
```

### Instalación estándar

```bash
cd ip_scanner
pip install .
```

## Verificar Instalación

```bash
# Verificar Python
python3 --version
# Debe ser >= 3.6

# Verificar módulos
python3 -c "import socket, ipaddress, concurrent.futures; print('OK')"
```

## Instalación en Diferentes Sistemas

### Ubuntu / Debian

```bash
# Python ya viene instalado, verificar versión
python3 --version

# Si necesitas instalar Python 3
sudo apt update
sudo apt install python3 python3-pip

# Clonar/descargar proyecto
cd ip_scanner

# Ejecutar
python3 main.py
```

### CentOS / RHEL / Fedora

```bash
# Verificar o instalar Python 3
sudo dnf install python3

# Clonar/descargar proyecto
cd ip_scanner

# Ejecutar
python3 main.py
```

### macOS

```bash
# Python 3 viene con macOS moderno
python3 --version

# Si no está instalado, instalar con Homebrew
brew install python3

# Clonar/descargar proyecto
cd ip_scanner

# Ejecutar
python3 main.py
```

### Windows 10/11

```cmd
# Descargar Python desde python.org
# Durante instalación, marcar "Add Python to PATH"

# Verificar
python --version

# Navegar al proyecto
cd C:\ip_scanner

# Ejecutar
python main.py
```

## Instalación en Entorno Virtual (Recomendado)

### Crear entorno virtual

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Instalar en entorno virtual

```bash
# Una vez activado el entorno
cd ip_scanner
pip install -e .
```

### Desactivar entorno virtual

```bash
deactivate
```

## Instalación en Kali Linux

```bash
# Python ya viene instalado
python3 --version

# Clonar proyecto
cd /opt
sudo git clone <repo-url> ip_scanner
cd ip_scanner

# Ejecutar
python3 main.py

# Opcional: crear alias
echo "alias ip-scan='python3 /opt/ip_scanner/main.py'" >> ~/.bashrc
source ~/.bashrc

# Ahora puedes usar
ip-scan --help
```

## Instalación en Raspberry Pi

```bash
# Actualizar sistema
sudo apt update
sudo apt upgrade

# Python ya viene instalado
python3 --version

# Clonar proyecto
cd ~
git clone <repo-url> ip_scanner
cd ip_scanner

# Ejecutar
python3 main.py
```

## Instalación en Termux (Android)

```bash
# Instalar Python
pkg install python

# Clonar proyecto
cd ~
git clone <repo-url> ip_scanner
cd ip_scanner

# Ejecutar
python main.py
```

## Instalación en Docker

### Crear Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ip_scanner/ /app/ip_scanner/
COPY main.py /app/

RUN chmod +x /app/main.py

ENTRYPOINT ["python3", "main.py"]
CMD ["--help"]
```

### Construir y ejecutar

```bash
# Construir imagen
docker build -t ip-scanner .

# Ejecutar
docker run --rm --network host ip-scanner

# Con opciones
docker run --rm --network host ip-scanner -n 192.168.1.0/24 --preset critical
```

## Solución de Problemas de Instalación

### Error: "python3: command not found"

**Linux**:
```bash
sudo apt install python3  # Ubuntu/Debian
sudo dnf install python3  # Fedora/RHEL
```

**macOS**:
```bash
brew install python3
```

**Windows**: Instalar desde python.org

### Error: "No module named 'ipaddress'"

Este módulo es estándar desde Python 3.3. Actualizar Python:
```bash
python3 --version  # Debe ser >= 3.6
```

### Error: Permisos denegados

**Linux/macOS**:
```bash
chmod +x main.py
```

O ejecutar con:
```bash
python3 main.py
```

### Error: "Permission denied" al escanear

Algunos sistemas requieren permisos elevados:
```bash
sudo python3 main.py
```

### Error: Import errors

Verificar que estás ejecutando desde el directorio correcto:
```bash
cd ip_scanner
python3 main.py  # NO python3 ip_scanner/main.py
```

## Actualización

### Git

```bash
cd ip_scanner
git pull origin main
```

### Manual

1. Descargar nueva versión
2. Reemplazar archivos
3. Mantener archivos de configuración personalizados si los hay

## Desinstalación

### Si instalaste como paquete

```bash
pip uninstall ip_scanner
```

### Si usas directamente

```bash
rm -rf /path/to/ip_scanner
```

## Verificación Post-Instalación

```bash
# Test básico
python3 main.py --help

# Test de escaneo (red ficticia, no hará nada)
python3 main.py -n 127.0.0.1/32 -t 0.1

# Test de importación
python3 -c "from ip_scanner.config import DEFAULT_PORTS; print(len(DEFAULT_PORTS), 'ports configured')"
```

## Performance Tips

### Linux: Aumentar límite de archivos abiertos

```bash
# Temporal
ulimit -n 65535

# Permanente
echo "* soft nofile 65535" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65535" | sudo tee -a /etc/security/limits.conf
```

### Todos los sistemas: Ajustar workers

```bash
# Más hilos para mejor rendimiento (si tienes buenos recursos)
python3 main.py -w 50

# Menos hilos si tienes recursos limitados
python3 main.py -w 10
```

## Instalación para Desarrollo

Si planeas modificar el código:

```bash
# Clonar proyecto
git clone <repo-url> ip_scanner
cd ip_scanner

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar en modo editable
pip install -e .

# Hacer cambios...
# Los cambios se reflejan inmediatamente sin reinstalar
```

## Configuración Inicial Recomendada

Después de instalar, prueba con:

```bash
# 1. Escaneo rápido de prueba
python3 main.py --preset critical -t 0.5 -w 10

# 2. Si funciona, escaneo completo
python3 main.py

# 3. Revisa resultados
ls -lh scan_*.txt
```

---

Para más información, consulta README.md y USAGE.md

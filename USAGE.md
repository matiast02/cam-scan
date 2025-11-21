# Guía de Uso Rápido - IP Scanner

## Casos de Uso Comunes

### 1. Primera Auditoría de Seguridad en Red Corporativa

**Escenario**: Necesitas auditar la seguridad de cámaras en una oficina.

```bash
# Paso 1: Escaneo rápido inicial
python3 main.py --preset critical

# Paso 2: Si encuentras dispositivos, escaneo completo
python3 main.py

# Paso 3: Documentar y reportar
# Los resultados se guardan automáticamente en scan_vulnerable_*.txt
```

### 2. Auditoría Específica de RTSP

**Escenario**: Solo te interesan las cámaras con RTSP expuesto.

```bash
python3 main.py --preset rtsp -w 30
```

### 3. Red Grande (> 1000 dispositivos)

**Escenario**: Escanear una red empresarial grande.

```bash
# Usar más hilos y timeout corto
python3 main.py -n 10.0.0.0/22 -w 100 -t 0.5 -a 2 --preset critical
```

### 4. Red Lenta o Inalámbrica

**Escenario**: Dispositivos con respuesta lenta.

```bash
# Aumentar timeouts
python3 main.py -t 3 -a 10 -w 10
```

### 5. Buscar Solo Interfaces Web

**Escenario**: Identificar todas las interfaces web de cámaras.

```bash
python3 main.py --preset http
```

### 6. Múltiples Redes

**Escenario**: Auditar varias subredes.

```bash
# Escanear cada red por separado
python3 main.py -n 192.168.1.0/24
python3 main.py -n 192.168.2.0/24
python3 main.py -n 192.168.3.0/24
```

### 7. Verificación Post-Hardening

**Escenario**: Verificar que las medidas de seguridad funcionan.

```bash
# Antes de hardening - documentar
python3 main.py > antes.txt

# Después de cambiar contraseñas y cerrar puertos
python3 main.py > despues.txt

# Comparar resultados
diff antes.txt despues.txt
```

## Interpretación de Resultados

### Símbolos

- 🟢 **Verde**: Dispositivo con puertos accesibles (VULNERABLE)
- 🔵 **Azul**: Dispositivo detectado pero protegido

### Información Mostrada

```
🟢 192.168.1.100    - Hikvision        - 4 puerto(s) - 3 accesible(s)
   └─ IP             └─ Fabricante      └─ Total      └─ Vulnerables
```

### Niveles de Severidad

| Puertos Accesibles | Severidad | Acción Requerida |
|-------------------|-----------|------------------|
| 0 | ✅ Seguro | Verificar configuración |
| 1-2 | ⚠️ Media | Cambiar contraseñas |
| 3+ | 🚨 Alta | Acción inmediata |

## Workflow Recomendado

### Auditoría de Seguridad Completa

1. **Escaneo Inicial**
   ```bash
   python3 main.py --preset critical
   ```

2. **Análisis de Resultados**
   - Revisar archivo `scan_vulnerable_*.txt`
   - Identificar dispositivos críticos
   - Priorizar por número de puertos accesibles

3. **Escaneo Detallado**
   ```bash
   python3 main.py
   ```

4. **Verificación Manual**
   - Usar URLs generadas para acceder a dispositivos
   - Confirmar vulnerabilidades
   - Documentar hallazgos

5. **Remediation**
   - Cambiar contraseñas
   - Cerrar puertos innecesarios
   - Actualizar firmware

6. **Verificación Post-Remediation**
   ```bash
   python3 main.py
   ```
   - Confirmar que no hay dispositivos vulnerables

## Tips y Trucos

### Optimización de Velocidad

```bash
# Máxima velocidad (red rápida, dispositivos confiables)
python3 main.py --preset critical -w 100 -t 0.3 -a 1

# Balance velocidad/precisión
python3 main.py -w 30 -t 1 -a 3

# Máxima precisión (puede ser lento)
python3 main.py -w 10 -t 3 -a 10
```

### Reducir Falsos Negativos

```bash
# Aumentar timeouts y reducir hilos
python3 main.py -t 2 -a 5 -w 10
```

### Escaneo Silencioso (Menos Agresivo)

```bash
# Menos hilos, más timeout entre requests
python3 main.py -w 5 -t 2
```

### Buscar Fabricante Específico

```bash
# Buscar solo Hikvision (puerto 8000)
python3 main.py --ports 8000,554,80

# Buscar solo Dahua (puerto 37777)
python3 main.py --ports 37777,554,80
```

## Automatización

### Script Bash para Múltiples Redes

```bash
#!/bin/bash
# scan_multiple.sh

NETWORKS=(
    "192.168.1.0/24"
    "192.168.2.0/24"
    "10.0.0.0/24"
)

for net in "${NETWORKS[@]}"; do
    echo "Escaneando $net..."
    python3 main.py -n "$net" --preset critical
    sleep 5
done
```

### Cron Job para Escaneo Periódico

```bash
# Ejecutar cada día a las 2 AM
0 2 * * * cd /path/to/ip_scanner && python3 main.py --preset critical > /var/log/camera_scan.log 2>&1
```

### Script Python para Análisis

```python
#!/usr/bin/env python3
import glob
import os

# Encontrar últimos resultados
results = sorted(glob.glob("scan_vulnerable_*.txt"))
if results:
    latest = results[-1]
    with open(latest) as f:
        content = f.read()
        # Contar dispositivos vulnerables
        count = content.count("IP:")
        print(f"Dispositivos vulnerables encontrados: {count}")
```

## Troubleshooting

### Problema: No encuentra dispositivos conocidos

**Solución**:
```bash
# Aumentar timeout
python3 main.py -t 3 -a 10

# Verificar red correcta
ip addr  # Linux
ipconfig # Windows

# Escanear red específica
python3 main.py -n 192.168.X.0/24
```

### Problema: Escaneo muy lento

**Solución**:
```bash
# Reducir puertos
python3 main.py --preset critical

# Aumentar hilos
python3 main.py -w 50

# Reducir timeout
python3 main.py -t 0.5 -a 2
```

### Problema: Demasiados falsos positivos

**Solución**:
```bash
# Aumentar timeout de autenticación
python3 main.py -a 5
```

## Integración con Otras Herramientas

### Exportar a CSV

```python
# export_csv.py
import re
import csv

with open('scan_vulnerable_20250115_103045.txt') as f:
    content = f.read()

devices = []
for block in content.split('IP:'):
    if block.strip():
        # Extraer información
        ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', block)
        if ip:
            devices.append({'ip': ip.group(1)})

with open('devices.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['ip'])
    writer.writeheader()
    writer.writerows(devices)
```

### Usar con nmap

```bash
# Generar lista de IPs
grep "IP:" scan_vulnerable_*.txt | awk '{print $2}' > targets.txt

# Escaneo detallado con nmap
nmap -sV -p 554,8554,80,37777 -iL targets.txt
```

### Usar con VLC (Probar streams RTSP)

```bash
# Extraer URLs RTSP
grep "rtsp://" scan_vulnerable_*.txt > rtsp_urls.txt

# Abrir con VLC
vlc $(head -1 rtsp_urls.txt)
```

## Preguntas Frecuentes

**P: ¿Es legal usar esta herramienta?**
R: Solo en redes donde tengas autorización expresa.

**P: ¿Puedo escanear desde Internet?**
R: No recomendado. Diseñado para redes locales/internas.

**P: ¿Funciona en Windows/Mac/Linux?**
R: Sí, es multiplataforma (Python estándar).

**P: ¿Necesita permisos de root/admin?**
R: No para puertos > 1024. Algunos sistemas pueden requerirlo.

**P: ¿Guarda contraseñas encontradas?**
R: Sí, en el archivo scan_vulnerable_*.txt (¡protegerlo adecuadamente!).

**P: ¿Afecta a los dispositivos?**
R: No, solo lectura. No modifica configuraciones.

**P: ¿Detecta todos los dispositivos?**
R: Detecta los que responden a protocolos conocidos. Algunos dispositivos muy antiguos o exóticos pueden no detectarse.

---

Para más información, consulta el README.md principal.

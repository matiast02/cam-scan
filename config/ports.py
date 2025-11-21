"""
Port definitions for different camera and DVR protocols
"""

# Puertos a escanear por defecto
DEFAULT_PORTS = {
    # RTSP
    554: {'protocol': 'RTSP', 'description': 'RTSP estándar'},
    8554: {'protocol': 'RTSP', 'description': 'RTSP alternativo'},
    555: {'protocol': 'RTSP', 'description': 'RTSP alternativo 2'},
    7447: {'protocol': 'RTSP', 'description': 'RTSP DVR chinos'},

    # HTTP/Web
    80: {'protocol': 'HTTP', 'description': 'Web estándar'},
    443: {'protocol': 'HTTPS', 'description': 'Web segura'},
    8080: {'protocol': 'HTTP', 'description': 'Web alternativo'},
    8081: {'protocol': 'HTTP', 'description': 'Web alternativo 2'},
    8000: {'protocol': 'HTTP', 'description': 'Hikvision web'},
    9000: {'protocol': 'HTTP', 'description': 'DVR/NVR web'},

    # Protocolos propietarios
    37777: {'protocol': 'DAHUA', 'description': 'Dahua DVR/NVR'},
    37778: {'protocol': 'DAHUA', 'description': 'Dahua alternativo'},
    34567: {'protocol': 'DVR', 'description': 'DVR genéricos chinos'},
    6036: {'protocol': 'DVR', 'description': 'Sistemas vigilancia'},
    7001: {'protocol': 'DVR', 'description': 'DVR varios'},

    # Otros protocolos
    3702: {'protocol': 'ONVIF', 'description': 'ONVIF Discovery'},
    1935: {'protocol': 'RTMP', 'description': 'RTMP streaming'},
    5000: {'protocol': 'HTTP', 'description': 'Synology/Otros'},
}

# Presets de puertos para escaneos específicos
PORT_PRESETS = {
    'critical': [554, 8554, 8000, 37777, 34567, 80, 3702],
    'rtsp': [554, 8554, 555, 7447],
    'http': [80, 443, 8080, 8081, 8000, 9000, 5000],
    'proprietary': [37777, 37778, 34567, 6036, 7001],
    'all': list(DEFAULT_PORTS.keys())
}

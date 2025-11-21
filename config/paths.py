"""
Common RTSP paths for different camera manufacturers and models
"""

# Rutas RTSP comunes
RTSP_PATHS = [
    "/",
    "/live/ch0",
    "/live/ch1",
    "/live/ch2",
    "/live/ch3",
    "/live/ch00_0",
    "/live/ch01_0",
    "/Streaming/Channels/101",
    "/Streaming/Channels/102",
    "/Streaming/Channels/201",
    "/Streaming/Channels/1",
    "/Streaming/Channels/2",
    "/cam/realmonitor?channel=1&subtype=0",
    "/cam/realmonitor?channel=1&subtype=1",
    "/cam/realmonitor?channel=2&subtype=0",
    "/h264",
    "/h264/ch1/main/av_stream",
    "/h264/ch1/sub/av_stream",
    "/stream1",
    "/stream2",
    "/video.mp4",
    "/live.sdp",
    "/mpeg4",
    "/CH001.sdp",
    "/videoMain",
    "/videoSub",
    "/11",
    "/12",
]

# Rutas RTSP específicas por fabricante
RTSP_PATHS_BY_MANUFACTURER = {
    'hikvision': [
        '/Streaming/Channels/101',
        '/Streaming/Channels/102',
        '/Streaming/Channels/1',
        '/h264/ch1/main/av_stream',
    ],
    'dahua': [
        '/cam/realmonitor?channel=1&subtype=0',
        '/cam/realmonitor?channel=1&subtype=1',
    ],
    'generic': [
        '/live/ch0',
        '/live/ch1',
        '/h264',
        '/stream1',
    ]
}

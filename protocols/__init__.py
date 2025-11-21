"""Protocol handlers for different camera and DVR protocols"""

from protocols.http_handler import test_http_auth
from protocols.rtsp_handler import test_rtsp_auth
from protocols.onvif_handler import test_onvif_discovery
from protocols.dahua_handler import test_dahua_protocol
from protocols.dvr_handler import test_generic_dvr

__all__ = [
    'test_http_auth',
    'test_rtsp_auth',
    'test_onvif_discovery',
    'test_dahua_protocol',
    'test_generic_dvr'
]

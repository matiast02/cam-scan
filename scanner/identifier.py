"""
Device and manufacturer identification
"""


def identify_manufacturer(device_info):
    """
    Identify manufacturer based on ports and services

    Args:
        device_info: Device information dictionary

    Returns:
        str: Identified manufacturer name
    """
    manufacturers = []

    for port_info in device_info['ports']:
        server = port_info.get('server', '').lower()

        if 'hikvision' in server or 'hik' in server:
            manufacturers.append('Hikvision')
        elif 'dahua' in server or port_info['protocol'] == 'DAHUA':
            manufacturers.append('Dahua')
        elif 'axis' in server:
            manufacturers.append('Axis')
        elif 'onvif' in server:
            manufacturers.append('ONVIF Compatible')

        if port_info.get('credentials'):
            mfr = port_info['credentials'].get('manufacturer', '')
            if mfr and mfr != 'Generic':
                manufacturers.append(mfr)

    if manufacturers:
        # Return the most common one
        return max(set(manufacturers), key=manufacturers.count)

    return 'Unknown'

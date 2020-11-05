VALID_KEYS = {
    'apod': [
        'concept_tags',
        'date',
        'hd',
        'count',
        'start_date',
        'end_date',
        'thumbs',
    ],
    'neo': [
        'start_date',
        'end_date',
        'asteroid_id',
    ],
    'cme': [
        'startDate',
        'endDate',
    ],
    'cme-a': [
        'startDate',
        'endDate',
        'mostAccurateOnly',
        'completeEntryOnly',
        'speed',
        'halfAngle',
        'catalog',
        'keyword',
    ],
    'gst': [
        'startDate',
        'endDate',
    ],
    'ips': [
        'startDate',
        'endDate',
        'location',
        'catalog',
    ],
    'flr': [
        'startDate',
        'endDate',
    ],
    'sep': [
        'startDate',
        'endDate',
    ],
    'mpc': [
        'startDate',
        'endDate',
    ],
    'rbe': [
        'startDate',
        'endDate',
    ],
    'hss': [
        'startDate',
        'endDate',
    ],
    'wsa-enlil': [
        'startDate',
        'endDate',
    ],
}

ROUTES = {
    'apod': '/planetary/apod',
    'neo': '/neo/rest/v1',
    'cme': '/DONKI/CME',
    'cme-a': '/DONKI/CMEAnalysis',
    'gst': '/DONKI/GST',
    'ips': '/DONKI/IPS',
    'flr': '/DONKI/FLR',
    'sep': '/DONKI/SEP',
    'mpc': '/DONKI/MPC',
    'rbe': '/DONKI/RBE',
    'hss': '/DONKI/HSS',
    'wsa-enlil': '/DONKI/WASEnlilSimulations',
}


ROVERS = [
    'curiosity',
    'opportunity',
    'spirit',
]


ROVER_CAMERAS = [
    'fhaz',
    'rhaz',
    'mast',
    'chemcam',
    'mahli',
    'mardi',
    'navcam',
    'pancam',
    'minites',
]


BASE_URL = "https://api.nasa.gov"

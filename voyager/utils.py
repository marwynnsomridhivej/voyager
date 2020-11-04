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
}

ROUTES = {
    'apod': '/planetary/apod',
    'neo': '/neo/rest/v1',
}

BASE_URL = "https://api.nasa.gov"
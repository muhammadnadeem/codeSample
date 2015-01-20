import handler

secure_scheme = 'https'

_routes = [
    RedirectRoute('/fill_app_data/', handler.FillAppData, name='fill_app_data', strict_slash=True),
]


def get_routes():
    return _routes


def add_routes(app):
    for r in _routes:
        app.router.add(r)
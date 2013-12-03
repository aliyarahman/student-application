import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if not app.debug:
    import logging
    from logging import FileHandler
    from logging import Formatter

    file_handler = FileHandler('/var/www/html/student-application/app.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

    app.logger.addHandler(file_handler)

application = app

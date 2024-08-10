from flask import Blueprint

reports = Blueprint('reports', __name__, template_folder='templates', url_prefix='/reportes')

from . import routes
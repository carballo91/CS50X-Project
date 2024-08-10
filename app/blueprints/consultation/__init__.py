from flask import Blueprint

consultation = Blueprint('consultation', __name__, template_folder='templates', url_prefix='/consulta')

from . import routes
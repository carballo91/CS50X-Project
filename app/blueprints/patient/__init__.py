from flask import Blueprint

patient = Blueprint('patient', __name__, template_folder='templates', url_prefix='/paciente')

from . import routes
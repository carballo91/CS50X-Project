from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired,Regexp



class FindPatient(FlaskForm):
    class Meta:
        csrf = False
    name = SearchField("Nombre del Paciente: ", validators=[DataRequired(message="No puede estar vacio"),Regexp('[a-zA-Z]+',message="Nombre: Por favor solo utilize letras")])
    last_name = SearchField("Apellido del Paciente",validators=[DataRequired(message="No puede estar vacio"),Regexp('[a-zA-Z]+',message="Apellido: Por favor solo utilize letras")])
    submit = SubmitField("Buscar")
    
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PrescriptionForm(FlaskForm):
    medicine = StringField('Medicina',validators=[DataRequired()])
    dose = IntegerField('Dosis',validators=[DataRequired()])
    instructions = TextAreaField('Instrucciones',validators=[DataRequired()])
    notes = TextAreaField('Notas',validators=[DataRequired()])
    save = SubmitField('Crear Medicamento')
    submit = SubmitField('Ver Receta')
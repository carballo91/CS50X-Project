from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Regexp, Optional


class PatientForm(FlaskForm): 
    name = StringField('Nombre',validators=[DataRequired()])
    last_name = StringField('Apellido',validators=[DataRequired()])
    age = IntegerField('Edad', validators=[DataRequired()])
    address = StringField('Direccion', validators=[DataRequired()])
    submit = SubmitField('Enviar')
        
class MedicineForm(FlaskForm):
    medicine = StringField('Medicamento', validators=[Optional(),Regexp('[a-zA-Z]+', message="Nombre: Por favor solo utilize letras")])
    dose = StringField('Dosis')
    instructions = StringField('Instrucciones')
    
class ConsultationForm(FlaskForm):
    height = FloatField('Estatura', validators=[DataRequired()])
    weight = FloatField('Peso', validators=[DataRequired()])
    imc = FloatField('IMC', validators=[DataRequired()])
    temperature = FloatField('T°',validators=[DataRequired()])
    ta = StringField('TA',validators=[DataRequired()])
    fr = FloatField('FR',validators=[DataRequired()])
    sat = StringField('Sat%')
    fc = StringField('FC')
    clinic_history = TextAreaField('Historia Clinica', validators=[DataRequired()])
    medical_records = TextAreaField('Antecedentes Medicos', validators=[DataRequired()])
    physical_exam = TextAreaField('Examen Fisico', validators=[DataRequired()])
    lab_exams = TextAreaField('Examenes de Laboratorio', validators=[DataRequired()])
    diagnostic = TextAreaField('Diagnostico', validators=[DataRequired()])
    # Plan Table Inputs
    medicines = FieldList(FormField(MedicineForm), min_entries=10, max_entries=10)
    submit = SubmitField('Guardar')
    
        
class PatientNotFoundForm(FlaskForm):
    submit = SubmitField('Crear Nuevo Expediente')
    
class ButtonNewConsultation(FlaskForm):
    submit = SubmitField('Crear')

class EmptyForm(FlaskForm):
    submit = SubmitField("Notificar Consulta")
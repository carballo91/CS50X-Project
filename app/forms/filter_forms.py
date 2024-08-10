from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class DateSearchForm(FlaskForm):
    class Meta:
        csrf = False
    month = IntegerField('Mes',validators=[DataRequired(),NumberRange(min=1,max=12)])
    year = IntegerField('Año',validators=[DataRequired()])
    filter = SubmitField('Filtrar')

class YearSearchForm(FlaskForm):
    class Meta:
        csrf = False
    year1 = IntegerField('Año',validators=[DataRequired()])
    filter = SubmitField('Filtrar')
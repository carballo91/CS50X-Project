from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp, Length

pass_regx = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@$!%*#?&])[A-Za-z0-9@$!%*#?&]{8,18}$'

class Login(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(),
                                                  Regexp('^[a-zA-Z0-9_]+$', message="Nombre de usuario debe contener solamente letras, numeros o guion bajo.")])
    password = PasswordField('Contraseña',validators=[DataRequired(), 
                                                      Length(min=8, message='Password tiene que tener al menos 8 caracteres'),
                                                      Regexp(pass_regx, message='Password es invalido. Debe contener al menos una letra mayuscula, un numero y un caracter especial @$!%*#?&')],
                             render_kw={'autocomplete':'off'})
    submit = SubmitField('Acceder')
    
    
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Regexp('^[a-zA-Z0-9_]+$', message="Nombre de usuario debe contener solamente letras, numeros o guion bajo."),
                                                   Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Regexp(pass_regx, message='Password es invalido. Debe contener al menos una letra mayuscula, un numero y un caracter especial @$!%*#?&'),
                                                     Length(min=8)],
                             render_kw={'autocomplete':'off'})
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
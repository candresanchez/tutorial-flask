from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length

#Formulario registro de usuario. Vista(show_signup_form())-> Plantilla(signup_form.html)
class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

#Formulario crear entradas en el Blog. Vista(post_form)-> Plantilla(post_form.html)
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])   
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')

#Clase para el Formulario Login. Vista(login)-> Plantilla(login_form.html)
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


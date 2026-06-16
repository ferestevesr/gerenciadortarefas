from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from gerenciadortarefas.models import Usuario

class FormLogin(FlaskForm):
    pass
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    pass
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirmar_senha = PasswordField("Confirme Password", validators=[DataRequired(), EqualTo("password")])
    botao_confirmacao = SubmitField("Criar Password")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado, faça login novamente.")
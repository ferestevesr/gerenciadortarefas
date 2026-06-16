from wtforms.validators import email

from gerenciadortarefas import app, database
from flask import render_template, url_for
from flask_login import login_required
from gerenciadortarefas.forms import FormLogin, FormCriarConta
from gerenciadortarefas.models import Usuario

@app.route('/', methods=['GET', 'POST'])
def index():
    formlogin=FormLogin()
    return render_template('index.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        usuario = Usuario(
            email=formcriarconta.email.data,
            username=formcriarconta.username.data,
            password=formcriarconta.password.data
        )

        database.session.add(usuario)
        database.session.commit()

        print("Usuário salvo!")

    return render_template('criarconta.html', form=formcriarconta)

@app.route('/tarefas/<usuario>')
@login_required
def tarefas(usuario):
    return render_template('tarefas.html', usuario=usuario)


@app.route('/gerenciador', methods=['GET', 'POST'])
def gerenciador():
    return render_template('gerenciador.html')
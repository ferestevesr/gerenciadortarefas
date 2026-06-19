from wtforms.validators import email

from gerenciadortarefas import app, database, bcrypt
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from gerenciadortarefas.forms import FormLogin, FormCriarConta
from gerenciadortarefas.models import Usuario

@app.route('/', methods=['GET', 'POST'])
def index():
    formlogin=FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.password, formlogin.password.data):
            login_user(usuario, remember=True)
            return redirect(url_for('tarefas', usuario=usuario.username))

    return render_template('index.html', form=formlogin)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        password = bcrypt.generate_password_hash(formcriarconta.password.data).decode('utf-8')
        usuario = Usuario(
            email=formcriarconta.email.data,
            username=formcriarconta.username.data,
            password=password
        )

        database.session.add(usuario)
        database.session.commit()

        print("Usuário salvo!")
        login_user(usuario, remember=True)
        return redirect(url_for('tarefas', usuario=usuario.username))


    return render_template('criarconta.html', form=formcriarconta)

@app.route('/tarefas/<usuario>')
@login_required
def tarefas(usuario):
    return render_template('tarefa.html', usuario=usuario)


@app.route('/gerenciador', methods=['GET', 'POST'])
def gerenciador():
    return render_template('gerenciador.html')
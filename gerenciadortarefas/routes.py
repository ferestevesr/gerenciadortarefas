from wtforms.validators import email

from gerenciadortarefas import app, database, bcrypt
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user, current_user
from gerenciadortarefas.forms import FormLogin, FormCriarConta, FormFoto
from gerenciadortarefas.models import Usuario
import os
from werkzeug.utils import secure_filename
@app.route('/', methods=['GET', 'POST'])
def index():
    formlogin=FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.password, formlogin.password.data):
            login_user(usuario, remember=True)
            return redirect(url_for('tarefas', id_usuario=usuario.id))

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
        return redirect(url_for('tarefas', id_usuario=usuario.username))


    return render_template('criarconta.html', form=formcriarconta)

@app.route('/tarefas/<id_usuario>', methods=['GET', 'POST'])
@login_required
def tarefas(id_usuario):

    usuario = Usuario.query.get(int(id_usuario))
    form = FormFoto()

    if int(id_usuario) == current_user.id:

        if form.validate_on_submit():
            arquivo = form.foto.data
            nome_seguro = secure_filename(arquivo.filename)

            caminho_projeto = os.path.abspath(os.path.dirname(__file__))
            caminho = os.path.join(
                caminho_projeto,
                app.config['UPLOAD_FOLDER'],
                nome_seguro
            )

            arquivo.save(caminho)

            current_user.foto_perfil = nome_seguro
            database.session.commit()

        return render_template(
            'tarefas.html',
            usuario=current_user,
            form=form
        )

    return render_template(
        'tarefas.html',
        usuario=usuario,
        form=None
    )
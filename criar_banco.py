from gerenciadortarefas import database, app
from gerenciadortarefas.models import Usuario, Tarefa, Projeto

from flask_login import login_required
with app.app_context():
    database.create_all()
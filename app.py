from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

app.app_context().push()
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # Mostrar todas as tarefas
    lista_tarefas = Lista.query.all()
    print(lista_tarefas)
    return render_template('base.html', lista_tarefas=lista_tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    # Adiciona uma nova tarefa
    titulo = request.form.get("title")
    nova_tarefa = Lista(title=titulo, complete=False)
    db.session.add(nova_tarefa)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/atualizar/<int:lista_id>")
def atualizar(lista_id):
    # Atualiza uma tarefa
    tarefa = Lista.query.filter_by(id=lista_id).first()
    tarefa.complete = not tarefa.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/apagar/<int:lista_id>")
def apagar(lista_id):
    # Apaga uma tarefa
    tarefa = Lista.query.filter_by(id=lista_id).first()
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
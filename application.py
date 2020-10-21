#coding:utf-8

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(application)


class Pessoa(db.Model):

    __tablename__ = 'Cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)

    def __init__ (self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email


db.create_all()


@application.route("/index")
def index():
    return render_template("index.html")

@application.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@application.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        if nome and telefone and cpf and email:
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))

@application.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return  render_template("lista.html", pessoas=pessoas)

@application.route("/excluir/<int:id>")
def excluir(id):
        pessoas = Pessoa.query.filter_by(id=id).first()

        db.session.delete(pessoas)
        db.session.commit()


        pessoas = Pessoa.query.all()
        return render_template("lista.html", pessoas = pessoas)

@application.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")

        if nome and telefone and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.email = email

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", pessoa=pessoa)



if __name__ == '__main__':
    application.run(host='0.0.0.0', degub=True)
from flask import Flask, jsonify, request
from flask_login import (
  LoginManager,
  current_user,
  login_required,
  login_user,
  logout_user,
)

from database import db
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # noqa: S105
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id: int):
  return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    # login
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message": "Autenticação realizada com sucesso"})

  return jsonify({"message": "Credenciais inválidas"}), 400


@app.route("/logout", methods=["POST"])
@login_required  # protege a rota e determina que apenas quem estiver logado, conseguirá acessa-la
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})


@app.route("/user", methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

  return jsonify({"message": "Credenciais inválidas"}), 400


@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello world"


if __name__ == "__main__":
  app.run(debug=True, port=3333)  # noqa: S201

# Comando "flask shell" no terminal, para entrar na aplicação que esta rodando, para criar o banco de dados
## dentro da aplicação pelo terminal, digitar "db.create_all()"
## toda vez que um banco de dados é acessado, é criado uma sessão e essa deve ser commitada "db.session.commit()"
## para sair da aplicação pelo terminal, digitar "exit()"

## para criar um registro na DB, dentro da aplicação pelo terminal, instanciar um objeto com os dados da entidade "user = User(username="admin",password="123")"
## adicionar o objeto através do terminal ao DB, "db.session.add(user)"
## salvar o que foi feito, "db.session.commit()"
## para sair da aplicação pelo terminal, digitar "exit()"

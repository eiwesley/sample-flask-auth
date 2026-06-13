from flask import Flask

from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # noqa: S105
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)


@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello world"


if __name__ == "__main__":
  app.run(debug=True, port=3333)  # noqa: S201

# Comando "flask shell" no terminal, para entrar na aplicação que esta rodando, para criar o banco de dados
## dentro da aplicação pelo terminal, digitar "db.create_all()"
## toda vez que um banco de dados é acessado, é criado uma sessão e essa deve ser commitada "db.session.commit()"
## para sair da aplicação pelo terminal, digitar "exit()"

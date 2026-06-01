import click
from dotenv import load_dotenv
from flask.cli import with_appcontext

from app import create_app
from app.extensions import db
from app.models.user import User

load_dotenv()

app = create_app()


@click.command("create-admin")
@click.option("--nome", prompt=True)
@click.option("--email", prompt=True)
@click.option("--senha", prompt=True, hide_input=True, confirmation_prompt=True)
@with_appcontext
def create_admin(nome, email, senha):
    existing = User.query.filter_by(email=email).first()
    if existing:
        click.echo("Usuario ja existe.")
        return
    user = User(nome=nome, email=email, perfil="admin")
    user.set_password(senha)
    db.session.add(user)
    db.session.commit()
    click.echo("Usuario admin criado com sucesso.")


app.cli.add_command(create_admin)

if __name__ == "__main__":
    app.run()

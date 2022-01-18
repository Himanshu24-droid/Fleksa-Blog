import click
from flask.cli import with_appcontext
from .extensions import db
from .models import User, Post

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(create_tables)


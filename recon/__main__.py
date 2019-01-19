import click

from recon import create_app, run_server
from recon.models import db


@click.group()
def cli():
    pass


@cli.command()
def run():
    """Runs the server."""
    app = create_app()
    with app.app_context():
        run_server(app)


@cli.command()
def create_db():
    """Initializes database, insert some sample data."""
    app = create_app()
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    cli()

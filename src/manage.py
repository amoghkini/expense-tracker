from flask import cli

from main.extensions import db
from main.main import AppFactory
app = AppFactory().get_app(__name__)



# def migrate_command():
#     # cli.run_command('db', ['migrate'])
#     cli.main(args=['db', 'migrate'])

# def upgrade_command():
#     cli.run_command('db', ['upgrade'])

@app.cli.command()
def initdb():
    """Creates the database tables."""
    db.create_all()

# @app.cli.command()
# def migrate():
#     migrate_command()

# @app.cli.command()
# def upgrade():
#     upgrade_command()

@app.cli.command()
def run():
    """Runs the Flask application."""
    app.run()  # Adjust debug as needed
    
if __name__ == '__main__':
    app.cli()

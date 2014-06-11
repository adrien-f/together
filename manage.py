from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand
from together.app import create_app
from together.models import db, migrate

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

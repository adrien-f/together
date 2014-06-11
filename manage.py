from flask.ext.assets import ManageAssets
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand
from together.app import create_app
from together.assets import assets_env
from together.models import db, migrate

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets(assets_env))

if __name__ == '__main__':
    manager.run()

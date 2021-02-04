from flask_migrate import Migrate, init, migrate as _migrate, upgrade, downgrade, revision
from config import app, db, logging
from models.user_model import UserModel

migrate = Migrate(app, db)


class MigrateFunctions:
    """
        Class to use Flask-Migrate Api function dor db migrations
    """
    try:
        def initializedb(self):
            with app.app_context():
                init(directory='migrations', multidb=False)
                return "db initialised"

        def revisiondb(self):
            with app.app_context():
                revision(directory='migrations', message=None, autogenerate=False, sql=False, head='head', splice=False, branch_label=None, version_path=None, rev_id=None)
                return "created empty script"

        def migratedb(self):
            with app.app_context():
                _migrate(directory='migrations', message=None, sql=False, head='head', splice=False, branch_label=None, version_path=None, rev_id=None)
                return "created an script"

        def upgradedb(self):
            with app.app_context():
                upgrade(directory='migrations', revision='head', sql=False, tag=None)
                return "db upgraded"

        def downgradedb(self):
            with app.app_context():
                downgrade(directory='migrations', revision='-1', sql=False, tag=None)
                return "db downgraded"

        def custom_migratdb(self):
            with app.app_context():
                _migrate(directory='migrations', message=None, sql=False, head='head', splice=False,
                         branch_label=None, version_path=None, rev_id=None)
                upgrade(directory='migrations', revision='head', sql=True, tag=None)
                return "db upgraded"

    except Exception as ex:
        print(ex)


def alterdata():
    # db.session.execute('insert into history values(3,"awdq@astd.cin","asdasdasdasdasdasdasdsad");')
    # db.session.execute('alter table history drop column nameplus;')
    db.session.commit()
    print("done")


version = []


def version_alembic():
    for version_num in db.session.query('version_num from alembic_version;'):
        print(version_num)
        global version
        version = version_num


def check_version():
    print(version[0])
    if version[0] == 'fb29b6bf3a27':
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    dbm = MigrateFunctions()
    # dbm.initializedb()
    # dbm.revisiondb()
    # dbm.migratedb()
    # dbm.upgradedb()
    # dbm.downgradedb()
    # dbm.custom_migratdb()

    #version_alembic()
    #check_version()

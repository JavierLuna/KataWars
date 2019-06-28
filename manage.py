from getpass import getpass
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models.notifications import Notification
from app.models.participant import Participant
from app.models.skills import Skill

app = create_app(os.getenv('ENV_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    def clear():
        [print() for _ in range(100)]

    def db_add(o):
        db.session.add(o)
        db.session.commit()

    def flush():
        db.session.rollback()

    return dict(app=app, db=db, db_add=db_add, flush=flush, clear=clear, Participant=Participant, Skill=Skill, Notification=Notification)


@manager.command
def create_superuser():
    username = input("Username: ")
    password = getpass("Password: ")

    participant = Participant(username=username, password=password, is_superuser=True)
    db.session.add(participant)
    try:
        db.session.commit()
        print("Done :)")
    except:
        print("Oops, shit happened!")
        db.session.rollback()


@manager.command
def notify_user():
    participants = Participant.query.all()
    targets = {}
    while 1:
        print("Participants:")
        for p in participants:
            print(p.username)
            targets[p.username] = p
        target = input("Who are you gonna notify? ")
        if target in targets:
            break
    content = input("Content: ")
    n = Notification(forwared_to=targets[target], description=content)
    db.session.add(n)
    try:
        db.session.commit()
        print("Done :)")
    except:
        print("Oops! Shit happened!")
        db.session.rollback()


@manager.command
def notify_all():
    participants = Participant.query.all()
    content = input("Content: ")
    for participant in participants:
        n = Notification(forwared_to=participant, description=content)
        db.session.add(n)
    try:
        db.session.commit()
        print("Done :)")
    except:
        print("Oops! Shit happened!")
        db.session.rollback()

@manager.command
def leaderboard():
    participants = Participant.query.order_by(Participant.score.desc())


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

import time

from app import create_app, db
from app.codewars.api import get_profile, get_score, get_completed_challenges
from app.models.notifications import Notification
from app.models.participant import Participant
from app.models.skills import Skill

application = create_app()
while 1:
    with application.app_context():
        participants = Participant.query.filter_by(is_superuser=False).all()
        skills = Skill.query.filter_by(visible=True).all()
        for participant in participants:
            time.sleep(0.5)
            print("Fetching", participant.codewars_username, "...")
            profile = get_profile(participant.codewars_username)
            score = get_score(profile)
            completed_challenges = get_completed_challenges(profile)

            if completed_challenges > participant.completed_challenges:
                print("\t\t\tWow!! Participant", participant.codewars_username, "has completed",
                      completed_challenges - participant.completed_challenges, "additional katas since last time!")
                n = Notification(description="Congrats on the new kata!", forwared_to=participant)
                db.session.add(n)
                for skill in skills:
                    if skill.can_consume(participant):
                        participant.add_skill(skill.id)
                        n = Notification(description="It looks like you have a new skill!", forwared_to=participant)
                        db.session.add(n)
                        print("Participant", participant.codewars_username, "won skill", skill.name)
                        break
                participant.score = int(score)
                participant.completed_challenges = int(score)
                print("Saving participant stats and skills...")
                db.session.add(participant)
                try:
                    db.session.commit()
                except:
                    print("There was an error trying to save participant", participant.codewars_username,
                          f"(id {participant.id})")
                    print("Rolling back!!!")
                    db.session.rollback()

    print("Sleeping for 10 seconds...")
    time.sleep(10)

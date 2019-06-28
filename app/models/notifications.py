from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)

    forwared_to_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('participants.id'))

    description = db.Column(db.String(400))

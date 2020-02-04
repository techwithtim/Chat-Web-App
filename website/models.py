from website import db


class Message(db.Model):
    """Model for messages """

    __tablename__ = 'messages'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(64),
                         index=False,
                         unique=False,
                         nullable=False)
    content = db.Column(db.Text,
                    index=False,
                    unique=False,
                    nullable=True)
    time = db.Column(db.DateTime,
                      index=False,
                      unique=False,
                      nullable=False)

    def __repr__(self):
        return f'<Message: Name: {self.name}, Content:{self.content}, DateTime:{self.time}>'

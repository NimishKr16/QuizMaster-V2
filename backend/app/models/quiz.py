from app.extensions import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.String(20))
    time_duration = db.Column(db.String(5))  # e.g., "00:30"
    remarks = db.Column(db.Text)

    questions = db.relationship('Question', backref='quiz', cascade="all, delete", lazy=True)
    scores = db.relationship('Score', backref='quiz', cascade="all, delete", lazy=True)
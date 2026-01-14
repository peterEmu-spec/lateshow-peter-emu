from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship("Appearance", back_populates="episode", cascade="all, delete-orphan")

    def to_dict(self, include_appearances=False):
        data = {"id": self.id, "date": self.date, "number": self.number}
        if include_appearances:
            data["appearances"] = [a.to_dict() for a in self.appearances]
        return data

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    appearances = db.relationship("Appearance", back_populates="guest", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "occupation": self.occupation}

class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guest.id"), nullable=False)

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    @staticmethod
    def validate_rating(rating):
        return 1 <= rating <= 5

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id,
            "episode": self.episode.to_dict() if self.episode else None,
            "guest": self.guest.to_dict() if self.guest else None
        }

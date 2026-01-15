from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = "episodes"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # One Episode has many Appearances
    appearances = db.relationship(
        "Appearance", 
        back_populates="episode", 
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_appearances=False):
        data = {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }
        if include_appearances:
            # Prevent infinite recursion
            data["appearances"] = [a.to_dict(include_episode=False) for a in self.appearances]
        return data


class Guest(db.Model):
    __tablename__ = "guests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # One Guest has many Appearances
    appearances = db.relationship(
        "Appearance", 
        back_populates="guest", 
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "occupation": self.occupation
        }


class Appearance(db.Model):
    __tablename__ = "appearances"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # --- Validation ---
    @staticmethod
    def validate_rating(rating):
        """Rating must be an integer between 1 and 5"""
        return isinstance(rating, int) and 1 <= rating <= 5

    # --- Serialization ---
    def to_dict(self, include_episode=True, include_guest=True):
        data = {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id
        }
        if include_episode and self.episode:
            data["episode"] = self.episode.to_dict()
        if include_guest and self.guest:
            data["guest"] = self.guest.to_dict()
        return data

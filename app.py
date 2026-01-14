from flask import Flask, jsonify, request
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lateshow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Seed database if empty
with app.app_context():
    db.create_all()
    if not Episode.query.first():
        ep1 = Episode(date="1/11/99", number=1)
        ep2 = Episode(date="1/12/99", number=2)
        g1 = Guest(name="Michael J. Fox", occupation="actor")
        g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
        g3 = Guest(name="Tracey Ullman", occupation="television actress")
        db.session.add_all([ep1, ep2, g1, g2, g3])
        db.session.commit()

# GET /episodes
@app.route("/episodes")
def get_episodes():
    return jsonify([e.to_dict() for e in Episode.query.all()])

# GET /episodes/:id
@app.route("/episodes/<int:id>")
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict(include_appearances=True))

# GET /guests
@app.route("/guests")
def get_guests():
    return jsonify([g.to_dict() for g in Guest.query.all()])

# POST /appearances
@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()
    rating = data.get("rating")
    episode_id = data.get("episode_id")
    guest_id = data.get("guest_id")

    if not Appearance.validate_rating(rating):
        return jsonify({"errors": ["rating must be between 1 and 5"]}), 400

    episode = Episode.query.get(episode_id)
    guest = Guest.query.get(guest_id)
    if not episode or not guest:
        return jsonify({"errors": ["Episode or Guest not found"]}), 404

    appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
    db.session.add(appearance)
    db.session.commit()

    return jsonify(appearance.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)

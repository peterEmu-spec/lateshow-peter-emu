from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lateshow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# --- Routes ---
@app.route("/episodes")
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict() for e in episodes])

@app.route("/episodes/<int:id>")
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict(include_appearances=True))

@app.route("/episodes/<int:id>", methods=["DELETE"])
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    try:
        db.session.delete(episode)
        db.session.commit()
        return jsonify({"message": f"Episode {id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete episode"}), 500

@app.route("/guests")
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests])

@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    # Extract fields from request
    rating = data.get("rating")
    episode_id = data.get("episode_id")
    guest_id = data.get("guest_id")

    errors = []

    # Validate rating
    if rating is None or not Appearance.validate_rating(rating):
        errors.append("Rating must be an integer between 1 and 5.")

    # Validate episode existence
    episode = Episode.query.get(episode_id)
    if not episode:
        errors.append(f"Episode with id {episode_id} does not exist.")

    # Validate guest existence
    guest = Guest.query.get(guest_id)
    if not guest:
        errors.append(f"Guest with id {guest_id} does not exist.")

    # If there are any validation errors, return 400
    if errors:
        return jsonify({"errors": errors}), 400

    # Create the appearance
    appearance = Appearance(
        rating=rating,
        episode_id=episode_id,
        guest_id=guest_id
    )

    try:
        db.session.add(appearance)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["Database error: could not create appearance."]}), 500

    # Return the newly created appearance with nested episode and guest
    return jsonify(appearance.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)

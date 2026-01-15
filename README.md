LateShow API

A simple Flask API to manage Episodes, Guests, and their Appearances.

Author

Peter Emu

Features

List all episodes and guests.

View episode details with appearances.

Create a guest appearance for an episode.

Delete episodes (cascading deletes for appearances).

Rating validation for appearances (1–5).

Setup

Clone the repo:

git clone https://github.com/peterEmu-spec/lateshow-peter-emu.git
cd lateshow-peter-emu


Activate virtual environment:

pipenv shell


Install dependencies:

pip install -r requirements.txt


Initialize the database:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


Seed the database:

python seed.py


Run the app:

python app.py

API Endpoints
Method	Endpoint	Description
GET	/episodes	List all episodes
GET	/episodes/<id>	Get episode with appearances
DELETE	/episodes/<id>	Delete an episode
GET	/guests	List all guests
POST	/appearances	Create a new appearance
Example POST /appearances
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}

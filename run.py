from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# DATA BASE
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(100), nullable=False)
    options = db.relationship('Option', backref='op', lazy=True, cascade='all,delete')

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    votes = db.relationship('Vote', backref='vt', lazy=True, cascade='all,delete')


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)


# API ROUTES

# POST POLL
@app.route('/api/poll', methods=['POST'])
def create_poll():
    try:
        data = request.get_json()
        new_poll = Poll(name = data['name'], content = data['content'],)
        db.session.add(new_poll)
        db.session.commit()
        return jsonify({"message": "Poll added!"}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


# LIST POLLS
@app.route('/api/polls', methods=['GET'])
def get_polls():
    try:
        polls = Poll.query.all()
        poll_list = []

        for poll in polls:
            poll_data = {
                "id": poll.id,
                "name": poll.name,
                "content": poll.content,
                "options": [{"id": option.id, "desc": option.desc} for option in poll.options]
            }
            poll_list.append(poll_data)
        return jsonify(poll_list), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

# ADD OPTIONS
@app.route('/api/options/add', methods=['POST'])
def add_option():
    #Option(id, desc, poll__id)
    try:
        data = request.get_json()
        poll = Poll.query.get(data['poll_id'])
        if poll:
            new_option = Option(desc=data['desc'], poll_id=data['poll_id'], op=poll)
            db.session.add(new_option)
            db.session.commit()
            return jsonify({'message': 'Option added!'}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500



# SINGLE POLL DETAILS
@app.route('/api/polls/<int:poll_id>', methods={'GET'})
def show_poll_details(poll_id):
    try:
        poll = Poll.query.get(poll_id)
        if poll:
            print(poll)
            return jsonify({'message': 'poll detais'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
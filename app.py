from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Fix Heroku PostgreSQL URL issue
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/add', methods=['POST'])
def add_data():
    data = request.json.get('content')
    if not data:
        return jsonify({'error': 'No content provided'}), 400
    new_entry = Data(content=data)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Data added!', 'id': new_entry.id})

@app.route('/get', methods=['GET'])
def get_data():
    data_list = Data.query.all()
    return jsonify([{'id': d.id, 'content': d.content} for d in data_list])

if __name__ == '__main__':
    app.run(debug=True)


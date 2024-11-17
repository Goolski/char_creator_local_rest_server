from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for characters
characters = []

@app.route('/characters', methods=['GET'])
def get_characters():
    """Return all characters."""
    return jsonify(characters)

@app.route('/characters', methods=['POST'])
def create_character():
    """Create a new character."""
    data = request.get_json()
    new_character = {
        "id": len(characters) + 1,
        "name": data.get("name"),
        "race": data.get("race"),
        "character_class": data.get("character_class"),
        "level": data.get("level", 1),
        "background": data.get("background", ""),
    }
    characters.append(new_character)
    return jsonify(new_character), 201

if __name__ == '__main__':
    app.run(debug=True)

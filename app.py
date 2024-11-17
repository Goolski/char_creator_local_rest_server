from flask import Flask, request, jsonify
from character import Character, CharacterException, NoteNotFoundException, TargetFieldNotFoundException, DuplicateFieldNameException
from field import Field

app = Flask(__name__)

# In-memory storage for characters
characters = []

@app.route('/characters', methods=['GET'])
def get_characters():
    """Return all characters."""
    return jsonify([character.to_json() for character in characters])

@app.route('/characters/<character_id>', methods=['GET'])
def get_character(character_id):
    """Return a single character by ID."""
    character = next((char for char in characters if char.id == character_id), None)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.to_json())

@app.route('/characters', methods=['POST'])
def create_character():
    """Create a new character."""
    data = request.get_json()
    fields = [Field.from_json(field) for field in data.get("fields", [])]
    try:
        new_character = Character.create(fields=fields)
        characters.append(new_character)
        return jsonify(new_character.to_json()), 201
    except CharacterException as e:
        return jsonify({"error": str(e)}), 400

@app.route('/characters/<character_id>', methods=['PUT'])
def update_character(character_id):
    """Update an existing character."""
    character = next((char for char in characters if char.id == character_id), None)
    if character is None:
        return jsonify({"error": "Character not found"}), 404

    data = request.get_json()
    fields = [Field.from_json(field) for field in data.get("fields", [])]
    try:
        updated_character = character.copy_with(fields=fields)
        characters[characters.index(character)] = updated_character
        return jsonify(updated_character.to_json())
    except CharacterException as e:
        return jsonify({"error": str(e)}), 400

@app.route('/characters/<character_id>', methods=['DELETE'])
def delete_character(character_id):
    """Delete a character."""
    global characters
    characters = [char for char in characters if char.id != character_id]
    return '', 204

@app.route('/not_found', methods=['GET'])
def not_found():
    """Always return a 404 response."""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
from note import Note

class Field:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        self.validate_notes()

    def validate_notes(self):
        note_ids = {note.id for note in self.notes}
        if len(note_ids) != len(self.notes):
            raise Exception('Field cannot store 2 notes with the same id')
        return True

    @classmethod
    def create(cls, name=None, notes=None):
        return cls(name or 'New Field', notes or [])

    def copy_with(self, name=None, notes=None):
        return Field(
            name=name if name is not None else self.name,
            notes=notes if notes is not None else self.notes
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            name=json_data['name'],
            notes=[Note.from_json(note) for note in json_data['notes']]
        )

    def to_json(self):
        return {
            'name': self.name,
            'notes': [note.to_json() for note in self.notes]
        }
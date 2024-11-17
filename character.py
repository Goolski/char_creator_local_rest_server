import uuid
from field import Field
from note import Note

class CharacterException(Exception):
    pass

class NoteNotFoundException(CharacterException):
    def __init__(self, note_id):
        super().__init__(f'Note with id {note_id} not found in any field')

class TargetFieldNotFoundException(CharacterException):
    def __init__(self, field_name):
        super().__init__(f'Target field with name {field_name} does not exist in character')

class DuplicateFieldNameException(CharacterException):
    def __init__(self):
        super().__init__('Fields must have unique names')

class Character:
    def __init__(self, id, fields):
        self._id = id
        self._fields = fields
        self.field_validator(fields)

    @property
    def id(self):
        return self._id

    @property
    def fields(self):
        return self._fields

    def field_validator(self, fields):
        field_names = [field.name for field in fields]
        if len(field_names) != len(set(field_names)):
            raise DuplicateFieldNameException()

    @classmethod
    def create(cls, fields):
        id = str(uuid.uuid4())  # Generate a unique ID
        return cls(id, fields)

    def copy_with(self, fields=None):
        return Character(self._id, fields or self._fields)

    # Field Related
    def add_new_field(self, field):
        updated_fields = self._fields + [field]
        return self.copy_with(fields=updated_fields)

    # Note Related
    def move_note_between_fields(self, target_field_name, moved_note_id):
        from_field = next((field for field in self._fields if any(note.id == moved_note_id for note in field.notes)), None)
        if from_field is None:
            raise NoteNotFoundException(moved_note_id)

        moved_note = next(note for note in from_field.notes if note.id == moved_note_id)

        target_field = next((field for field in self._fields if field.name == target_field_name), None)
        if target_field is None:
            raise TargetFieldNotFoundException(target_field_name)

        if from_field == target_field:
            return self

        updated_from_field = from_field.copy_with(notes=[note for note in from_field.notes if note.id != moved_note_id])
        updated_to_field = target_field.copy_with(notes=target_field.notes + [moved_note])

        updated_fields = [updated_from_field if field == from_field else updated_to_field if field == target_field else field for field in self._fields]
        return self.copy_with(fields=updated_fields)

    def add_or_update_note_in_field(self, field_name, note):
        field = next((f for f in self._fields if f.name == field_name), None)
        if field is None:
            raise TargetFieldNotFoundException(field_name)

        is_note_in_the_field = any(n.id == note.id for n in field.notes)

        if is_note_in_the_field:
            updated_notes = [note if n.id == note.id else n for n in field.notes]
        else:
            updated_notes = field.notes + [note]

        updated_field = field.copy_with(notes=updated_notes)
        updated_fields = [updated_field if f == field else f for f in self._fields]
        return self.copy_with(fields=updated_fields)

    def delete_note_in_field(self, field, note):
        is_note_in_the_field = any(n.id == note.id for n in field.notes)
        if not is_note_in_the_field:
            raise NoteNotFoundException(note.id)

        updated_notes = [n for n in field.notes if n.id != note.id]
        updated_field = field.copy_with(notes=updated_notes)
        updated_fields = [updated_field if f == field else f for f in self._fields]
        return self.copy_with(fields=updated_fields)

    def to_json(self):
        return {
            'id': self._id,
            'fields': [field.to_json() for field in self._fields]
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data['id'],
            fields=[Field.from_json(field) for field in json_data['fields']]
        )
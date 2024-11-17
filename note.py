import uuid

class Note:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.validate_value(value)

    @classmethod
    def create(cls, value):
        return cls(str(uuid.uuid4()), value)

    @staticmethod
    def validate_value(value):
        if value is None:
            raise ValueError('Value cannot be null')
        if not value:
            raise ValueError('Value cannot be empty')

    def copy_with(self, value=None):
        return Note(
            id=self.id,
            value=value if value is not None else self.value
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data['id'],
            value=json_data['value']
        )

    def to_json(self):
        return {
            'id': self.id,
            'value': self.value
        }
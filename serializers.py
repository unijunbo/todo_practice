from app import ma


class TodoFolderSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "title")

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "content")
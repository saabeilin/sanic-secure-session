import uuid


class Session(dict):
    sid: None

    def __init__(self, sid=None, **kwargs):
        super().__init__(**kwargs)
        self.sid = sid or str(uuid.uuid4())
        print(self.sid)

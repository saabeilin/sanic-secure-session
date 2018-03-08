import uuid


class Session(dict):
    sid: None

    def __init__(self, sid: str = None, **kwargs):
        super().__init__(**kwargs)
        self.sid = sid or self._new_sid()
        self.refresh: bool = False

    def _new_sid(self) -> str:
        return str(uuid.uuid4())

    def new_sid(self) -> None:
        self.sid = self._new_sid()

    def is_empty(self) -> bool:
        return dict(self) == {}

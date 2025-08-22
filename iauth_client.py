from typing import Protocol

class IAuthClient(Protocol):
    def authenticate(self):
        ...
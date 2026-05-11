from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class Seeder(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def run(self) -> None:
        """Execute the seeder."""

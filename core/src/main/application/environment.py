from abc import ABC, abstractmethod

from core.src.main.domain.models.country import Country


class Environment(ABC):

    @abstractmethod
    async def get_countries(self) -> list[Country]:
        pass
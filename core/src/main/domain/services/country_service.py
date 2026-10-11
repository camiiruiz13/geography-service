from abc import abstractmethod, ABC

from core.src.main.domain.models.country import Country


class CountryService(ABC):

    @abstractmethod
    async def get_countries(self) -> list[Country]:
        pass

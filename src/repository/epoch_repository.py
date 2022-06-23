from src.entity.cardano import Epoch
from src.repository.base_repository import BaseRepository


class EpochRepository(BaseRepository):
    entity = Epoch

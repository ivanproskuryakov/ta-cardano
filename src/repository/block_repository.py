from src.entity.cardano import Block
from src.repository.base_repository import BaseRepository


class BlockRepository(BaseRepository):
    entity = Block

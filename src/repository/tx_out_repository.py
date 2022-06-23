from src.entity.cardano import TxOut
from src.repository.base_repository import BaseRepository


class TxOutRepository(BaseRepository):
    entity = TxOut

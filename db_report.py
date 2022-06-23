from src.repository.tx_out_repository import TxOutRepository

repo = TxOutRepository()

df = repo.find_all()

print(df)

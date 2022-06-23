### Installation

```
pip install -r requirements.txt
pip install -r requirements-linux.txt
pip install --force-reinstall -r requirements.txt

python -m venv .env
source .env/bin/activate
```

### Overview

Database connector to ease data fetching from postgres db, sync from cardano ledger with cardano-db-sync


### Dependencies 
https://github.com/input-output-hk/cardano-db-sync

A component that follows the Cardano chain and stores blocks and transactions in PostgreSQL
The purpose of Cardano DB Sync is to follow the Cardano chain and take information from the chain and an 
internally maintained copy of ledger state. 
Data is then extracted from the chain and inserted into a PostgreSQL database.

https://github.com/input-output-hk/cardano-node

The core component that is used to participate in a Cardano decentralised blockchain.


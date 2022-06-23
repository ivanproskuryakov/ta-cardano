from sqlalchemy import BigInteger, Boolean, Column, \
    DateTime, Enum, Float, ForeignKey, \
    Integer, LargeBinary, Numeric, \
    SmallInteger, String, Table, \
    UniqueConstraint, text, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('admin_user_id_seq'::regclass)"))
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class DelistedPool(Base):
    __tablename__ = 'delisted_pool'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('delisted_pool_id_seq'::regclass)"))
    hash_raw = Column(LargeBinary, nullable=False, unique=True)


class Epoch(Base):
    __tablename__ = 'epoch'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('epoch_id_seq'::regclass)"))
    out_sum = Column(Numeric, nullable=False)
    fees = Column(Numeric, nullable=False)
    tx_count = Column(Integer, nullable=False)
    blk_count = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False, unique=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)


class EpochRewardTotalReceived(Base):
    __tablename__ = 'epoch_reward_total_received'

    id = Column(BigInteger, primary_key=True,
                server_default=text("nextval('epoch_reward_total_received_id_seq'::regclass)"))
    earned_epoch = Column(Integer, nullable=False, unique=True)
    amount = Column(Numeric, nullable=False)


class EpochSyncTime(Base):
    __tablename__ = 'epoch_sync_time'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('epoch_sync_time_id_seq'::regclass)"))
    no = Column(BigInteger, nullable=False, unique=True)
    seconds = Column(BigInteger, nullable=False)
    state = Column(Enum('lagging', 'following', name='syncstatetype'), nullable=False)


class Meta(Base):
    __tablename__ = 'meta'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('meta_id_seq'::regclass)"))
    start_time = Column(DateTime, nullable=False, unique=True)
    network_name = Column(String, nullable=False)
    version = Column(String, nullable=False)


class MultiAsset(Base):
    __tablename__ = 'multi_asset'
    __table_args__ = (
        UniqueConstraint('policy', 'name'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('multi_asset_id_seq'::regclass)"))
    policy = Column(LargeBinary, nullable=False)
    name = Column(LargeBinary, nullable=False)
    fingerprint = Column(String, nullable=False)


class PoolHash(Base):
    __tablename__ = 'pool_hash'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_hash_id_seq'::regclass)"))
    hash_raw = Column(LargeBinary, nullable=False, unique=True)
    view = Column(String, nullable=False)


class ReservedPoolTicker(Base):
    __tablename__ = 'reserved_pool_ticker'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('reserved_pool_ticker_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    pool_hash = Column(LargeBinary, nullable=False, index=True)


class SchemaVersion(Base):
    __tablename__ = 'schema_version'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('schema_version_id_seq'::regclass)"))
    stage_one = Column(BigInteger, nullable=False)
    stage_two = Column(BigInteger, nullable=False)
    stage_three = Column(BigInteger, nullable=False)


t_utxo_byron_view = Table(
    'utxo_byron_view', metadata,
    Column('id', BigInteger),
    Column('tx_id', BigInteger),
    Column('index', SmallInteger),
    Column('address', String),
    Column('address_raw', LargeBinary),
    Column('address_has_script', Boolean),
    Column('payment_cred', LargeBinary),
    Column('stake_address_id', BigInteger),
    Column('value', Numeric),
    Column('data_hash', LargeBinary)
)

t_utxo_view = Table(
    'utxo_view', metadata,
    Column('id', BigInteger),
    Column('tx_id', BigInteger),
    Column('index', SmallInteger),
    Column('address', String),
    Column('address_raw', LargeBinary),
    Column('address_has_script', Boolean),
    Column('payment_cred', LargeBinary),
    Column('stake_address_id', BigInteger),
    Column('value', Numeric),
    Column('data_hash', LargeBinary)
)


class SlotLeader(Base):
    __tablename__ = 'slot_leader'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('slot_leader_id_seq'::regclass)"))
    hash = Column(LargeBinary, nullable=False, unique=True)
    pool_hash_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)
    description = Column(String, nullable=False)

    pool_hash = relationship('PoolHash')


class Block(Base):
    __tablename__ = 'block'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('block_id_seq'::regclass)"))
    hash = Column(LargeBinary, nullable=False, unique=True)
    epoch_no = Column(Integer, index=True)
    slot_no = Column(Integer, index=True)
    epoch_slot_no = Column(Integer)
    block_no = Column(Integer, index=True)
    previous_id = Column(ForeignKey('block.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)
    slot_leader_id = Column(ForeignKey('slot_leader.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                            index=True)
    size = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False, index=True)
    tx_count = Column(BigInteger, nullable=False)
    proto_major = Column(Integer, nullable=False)
    proto_minor = Column(Integer, nullable=False)
    vrf_key = Column(String)
    op_cert = Column(LargeBinary)
    op_cert_counter = Column(BigInteger)

    previous = relationship('Block', remote_side=[id])
    slot_leader = relationship('SlotLeader')


class AdaPot(Base):
    __tablename__ = 'ada_pots'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('ada_pots_id_seq'::regclass)"))
    slot_no = Column(Integer, nullable=False)
    epoch_no = Column(Integer, nullable=False)
    treasury = Column(Numeric, nullable=False)
    reserves = Column(Numeric, nullable=False)
    rewards = Column(Numeric, nullable=False)
    utxo = Column(Numeric, nullable=False)
    deposits = Column(Numeric, nullable=False)
    fees = Column(Numeric, nullable=False)
    block_id = Column(ForeignKey('block.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, unique=True)

    block = relationship('Block', uselist=False)


class CostModel(Base):
    __tablename__ = 'cost_model'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('cost_model_id_seq'::regclass)"))
    costs = Column(JSONB(astext_type=Text()), nullable=False, unique=True)
    block_id = Column(ForeignKey('block.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)

    block = relationship('Block')


class Tx(Base):
    __tablename__ = 'tx'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('tx_id_seq'::regclass)"))
    hash = Column(LargeBinary, nullable=False, unique=True)
    block_id = Column(ForeignKey('block.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    block_index = Column(Integer, nullable=False)
    out_sum = Column(Numeric, nullable=False)
    fee = Column(Numeric, nullable=False)
    deposit = Column(BigInteger, nullable=False)
    size = Column(Integer, nullable=False)
    invalid_before = Column(Numeric)
    invalid_hereafter = Column(Numeric)
    valid_contract = Column(Boolean, nullable=False)
    script_size = Column(Integer, nullable=False)

    block = relationship('Block')


class CollateralTxIn(Base):
    __tablename__ = 'collateral_tx_in'
    __table_args__ = (
        UniqueConstraint('tx_in_id', 'tx_out_id', 'tx_out_index'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('collateral_tx_in_id_seq'::regclass)"))
    tx_in_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    tx_out_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    tx_out_index = Column(SmallInteger, nullable=False)

    tx_in = relationship('Tx', primaryjoin='CollateralTxIn.tx_in_id == Tx.id')
    tx_out = relationship('Tx', primaryjoin='CollateralTxIn.tx_out_id == Tx.id')


class Datum(Base):
    __tablename__ = 'datum'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('datum_id_seq'::regclass)"))
    hash = Column(LargeBinary, nullable=False, unique=True)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    value = Column(JSONB(astext_type=Text()))

    tx = relationship('Tx')


class EpochParam(Base):
    __tablename__ = 'epoch_param'
    __table_args__ = (
        UniqueConstraint('epoch_no', 'block_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('epoch_param_id_seq'::regclass)"))
    epoch_no = Column(Integer, nullable=False)
    min_fee_a = Column(Integer, nullable=False)
    min_fee_b = Column(Integer, nullable=False)
    max_block_size = Column(Integer, nullable=False)
    max_tx_size = Column(Integer, nullable=False)
    max_bh_size = Column(Integer, nullable=False)
    key_deposit = Column(Numeric, nullable=False)
    pool_deposit = Column(Numeric, nullable=False)
    max_epoch = Column(Integer, nullable=False)
    optimal_pool_count = Column(Integer, nullable=False)
    influence = Column(Float(53), nullable=False)
    monetary_expand_rate = Column(Float(53), nullable=False)
    treasury_growth_rate = Column(Float(53), nullable=False)
    decentralisation = Column(Float(53), nullable=False)
    entropy = Column(LargeBinary)
    protocol_major = Column(Integer, nullable=False)
    protocol_minor = Column(Integer, nullable=False)
    min_utxo_value = Column(Numeric, nullable=False)
    min_pool_cost = Column(Numeric, nullable=False)
    nonce = Column(LargeBinary)
    coins_per_utxo_word = Column(Numeric)
    cost_model_id = Column(ForeignKey('cost_model.id', ondelete='CASCADE', onupdate='RESTRICT'))
    price_mem = Column(Float(53))
    price_step = Column(Float(53))
    max_tx_ex_mem = Column(Numeric)
    max_tx_ex_steps = Column(Numeric)
    max_block_ex_mem = Column(Numeric)
    max_block_ex_steps = Column(Numeric)
    max_val_size = Column(Numeric)
    collateral_percent = Column(Integer)
    max_collateral_inputs = Column(Integer)
    block_id = Column(ForeignKey('block.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    block = relationship('Block')
    cost_model = relationship('CostModel')


class MaTxMint(Base):
    __tablename__ = 'ma_tx_mint'
    __table_args__ = (
        UniqueConstraint('ident', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('ma_tx_mint_id_seq'::regclass)"))
    quantity = Column(Numeric, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    ident = Column(ForeignKey('multi_asset.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    multi_asset = relationship('MultiAsset')
    tx = relationship('Tx')


class ParamProposal(Base):
    __tablename__ = 'param_proposal'
    __table_args__ = (
        UniqueConstraint('key', 'registered_tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('param_proposal_id_seq'::regclass)"))
    epoch_no = Column(Integer, nullable=False)
    key = Column(LargeBinary, nullable=False)
    min_fee_a = Column(Numeric)
    min_fee_b = Column(Numeric)
    max_block_size = Column(Numeric)
    max_tx_size = Column(Numeric)
    max_bh_size = Column(Numeric)
    key_deposit = Column(Numeric)
    pool_deposit = Column(Numeric)
    max_epoch = Column(Numeric)
    optimal_pool_count = Column(Numeric)
    influence = Column(Float(53))
    monetary_expand_rate = Column(Float(53))
    treasury_growth_rate = Column(Float(53))
    decentralisation = Column(Float(53))
    entropy = Column(LargeBinary)
    protocol_major = Column(Integer)
    protocol_minor = Column(Integer)
    min_utxo_value = Column(Numeric)
    min_pool_cost = Column(Numeric)
    coins_per_utxo_word = Column(Numeric)
    cost_model_id = Column(ForeignKey('cost_model.id', ondelete='CASCADE', onupdate='RESTRICT'))
    price_mem = Column(Float(53))
    price_step = Column(Float(53))
    max_tx_ex_mem = Column(Numeric)
    max_tx_ex_steps = Column(Numeric)
    max_block_ex_mem = Column(Numeric)
    max_block_ex_steps = Column(Numeric)
    max_val_size = Column(Numeric)
    collateral_percent = Column(Integer)
    max_collateral_inputs = Column(Integer)
    registered_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    cost_model = relationship('CostModel')
    registered_tx = relationship('Tx')


class PoolMetadataRef(Base):
    __tablename__ = 'pool_metadata_ref'
    __table_args__ = (
        UniqueConstraint('pool_id', 'url', 'hash'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_metadata_ref_id_seq'::regclass)"))
    pool_id = Column(ForeignKey('pool_hash.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    url = Column(String, nullable=False)
    hash = Column(LargeBinary, nullable=False)
    registered_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    pool = relationship('PoolHash')
    registered_tx = relationship('Tx')


class PoolRetire(Base):
    __tablename__ = 'pool_retire'
    __table_args__ = (
        UniqueConstraint('hash_id', 'announced_tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_retire_id_seq'::regclass)"))
    hash_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    cert_index = Column(Integer, nullable=False)
    announced_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    retiring_epoch = Column(Integer, nullable=False)

    announced_tx = relationship('Tx')
    hash = relationship('PoolHash')


class PotTransfer(Base):
    __tablename__ = 'pot_transfer'
    __table_args__ = (
        UniqueConstraint('tx_id', 'cert_index'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pot_transfer_id_seq'::regclass)"))
    cert_index = Column(Integer, nullable=False)
    treasury = Column(Numeric, nullable=False)
    reserves = Column(Numeric, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)

    tx = relationship('Tx')


class Script(Base):
    __tablename__ = 'script'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('script_id_seq'::regclass)"))
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    hash = Column(LargeBinary, nullable=False, unique=True)
    type = Column(Enum('multisig', 'timelock', 'plutus', name='scripttype'), nullable=False)
    json = Column(JSONB(astext_type=Text()))
    bytes = Column(LargeBinary)
    serialised_size = Column(Integer)

    tx = relationship('Tx')


class StakeAddres(Base):
    __tablename__ = 'stake_address'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stake_address_id_seq'::regclass)"))
    hash_raw = Column(LargeBinary, nullable=False, unique=True)
    view = Column(String, nullable=False, index=True)
    script_hash = Column(LargeBinary)
    registered_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    registered_tx = relationship('Tx')


class TxMetadatum(Base):
    __tablename__ = 'tx_metadata'
    __table_args__ = (
        UniqueConstraint('key', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('tx_metadata_id_seq'::regclass)"))
    key = Column(Numeric, nullable=False)
    json = Column(JSONB(astext_type=Text()))
    bytes = Column(LargeBinary, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    tx = relationship('Tx')


class EpochStake(Base):
    __tablename__ = 'epoch_stake'
    __table_args__ = (
        UniqueConstraint('epoch_no', 'addr_id', 'pool_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('epoch_stake_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    pool_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    amount = Column(Numeric, nullable=False)
    epoch_no = Column(Integer, nullable=False, index=True)

    addr = relationship('StakeAddres')
    pool = relationship('PoolHash')


class PoolOfflineDatum(Base):
    __tablename__ = 'pool_offline_data'
    __table_args__ = (
        UniqueConstraint('pool_id', 'hash'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_offline_data_id_seq'::regclass)"))
    pool_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    ticker_name = Column(String, nullable=False)
    hash = Column(LargeBinary, nullable=False)
    json = Column(JSONB(astext_type=Text()), nullable=False)
    bytes = Column(LargeBinary, nullable=False)
    pmr_id = Column(ForeignKey('pool_metadata_ref.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                    index=True)

    pmr = relationship('PoolMetadataRef')
    pool = relationship('PoolHash')


class PoolOfflineFetchError(Base):
    __tablename__ = 'pool_offline_fetch_error'
    __table_args__ = (
        UniqueConstraint('pool_id', 'fetch_time', 'retry_count'),
    )

    id = Column(BigInteger, primary_key=True,
                server_default=text("nextval('pool_offline_fetch_error_id_seq'::regclass)"))
    pool_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    fetch_time = Column(DateTime, nullable=False)
    pmr_id = Column(ForeignKey('pool_metadata_ref.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                    index=True)
    fetch_error = Column(String, nullable=False)
    retry_count = Column(Integer, nullable=False)

    pmr = relationship('PoolMetadataRef')
    pool = relationship('PoolHash')


class PoolOwner(Base):
    __tablename__ = 'pool_owner'
    __table_args__ = (
        UniqueConstraint('addr_id', 'pool_hash_id', 'registered_tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_owner_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    pool_hash_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                          index=True)
    registered_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    addr = relationship('StakeAddres')
    pool_hash = relationship('PoolHash')
    registered_tx = relationship('Tx')


class PoolUpdate(Base):
    __tablename__ = 'pool_update'
    __table_args__ = (
        UniqueConstraint('hash_id', 'registered_tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_update_id_seq'::regclass)"))
    hash_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    cert_index = Column(Integer, nullable=False)
    vrf_key_hash = Column(LargeBinary, nullable=False)
    pledge = Column(Numeric, nullable=False)
    reward_addr = Column(LargeBinary, nullable=False, index=True)
    active_epoch_no = Column(BigInteger, nullable=False, index=True)
    meta_id = Column(ForeignKey('pool_metadata_ref.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)
    margin = Column(Float(53), nullable=False)
    fixed_cost = Column(Numeric, nullable=False)
    registered_tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    hash = relationship('PoolHash')
    meta = relationship('PoolMetadataRef')
    registered_tx = relationship('Tx')


class Redeemer(Base):
    __tablename__ = 'redeemer'
    __table_args__ = (
        UniqueConstraint('tx_id', 'purpose', 'index'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('redeemer_id_seq'::regclass)"))
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    unit_mem = Column(BigInteger, nullable=False)
    unit_steps = Column(BigInteger, nullable=False)
    fee = Column(Numeric, nullable=False)
    purpose = Column(Enum('spend', 'mint', 'cert', 'reward', name='scriptpurposetype'), nullable=False)
    index = Column(Integer, nullable=False)
    script_hash = Column(LargeBinary)
    datum_id = Column(ForeignKey('datum.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)

    datum = relationship('Datum')
    tx = relationship('Tx')


class Reserve(Base):
    __tablename__ = 'reserve'
    __table_args__ = (
        UniqueConstraint('addr_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('reserve_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    cert_index = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    addr = relationship('StakeAddres')
    tx = relationship('Tx')


class Reward(Base):
    __tablename__ = 'reward'
    __table_args__ = (
        UniqueConstraint('addr_id', 'type', 'earned_epoch', 'pool_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('reward_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    type = Column(Enum('leader', 'member', 'reserves', 'treasury', 'refund', name='rewardtype'), nullable=False)
    amount = Column(Numeric, nullable=False)
    earned_epoch = Column(BigInteger, nullable=False, index=True)
    spendable_epoch = Column(BigInteger, nullable=False)
    pool_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)

    addr = relationship('StakeAddres')
    pool = relationship('PoolHash')


class StakeRegistration(Base):
    __tablename__ = 'stake_registration'
    __table_args__ = (
        UniqueConstraint('addr_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stake_registration_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    cert_index = Column(Integer, nullable=False)
    epoch_no = Column(Integer, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    addr = relationship('StakeAddres')
    tx = relationship('Tx')


class Treasury(Base):
    __tablename__ = 'treasury'
    __table_args__ = (
        UniqueConstraint('addr_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('treasury_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    cert_index = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    addr = relationship('StakeAddres')
    tx = relationship('Tx')


class TxOut(Base):
    __tablename__ = 'tx_out'
    __table_args__ = (
        UniqueConstraint('tx_id', 'index'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('tx_out_id_seq'::regclass)"))
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    index = Column(SmallInteger, nullable=False)
    address = Column(String, nullable=False, index=True)
    address_raw = Column(LargeBinary, nullable=False)
    address_has_script = Column(Boolean, nullable=False)
    payment_cred = Column(LargeBinary, index=True)
    stake_address_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)
    value = Column(Numeric, nullable=False)
    data_hash = Column(LargeBinary)

    stake_address = relationship('StakeAddres')
    tx = relationship('Tx')


class Delegation(Base):
    __tablename__ = 'delegation'
    __table_args__ = (
        UniqueConstraint('addr_id', 'pool_hash_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('delegation_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    cert_index = Column(Integer, nullable=False)
    pool_hash_id = Column(ForeignKey('pool_hash.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                          index=True)
    active_epoch_no = Column(BigInteger, nullable=False, index=True)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    slot_no = Column(Integer, nullable=False)
    redeemer_id = Column(ForeignKey('redeemer.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)

    addr = relationship('StakeAddres')
    pool_hash = relationship('PoolHash')
    redeemer = relationship('Redeemer')
    tx = relationship('Tx')


class MaTxOut(Base):
    __tablename__ = 'ma_tx_out'
    __table_args__ = (
        UniqueConstraint('ident', 'tx_out_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('ma_tx_out_id_seq'::regclass)"))
    quantity = Column(Numeric, nullable=False)
    tx_out_id = Column(ForeignKey('tx_out.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    ident = Column(ForeignKey('multi_asset.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    multi_asset = relationship('MultiAsset')
    tx_out = relationship('TxOut')


class PoolRelay(Base):
    __tablename__ = 'pool_relay'
    __table_args__ = (
        UniqueConstraint('update_id', 'ipv4', 'ipv6', 'dns_name'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('pool_relay_id_seq'::regclass)"))
    update_id = Column(ForeignKey('pool_update.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                       index=True)
    ipv4 = Column(String)
    ipv6 = Column(String)
    dns_name = Column(String)
    dns_srv_name = Column(String)
    port = Column(Integer)

    update = relationship('PoolUpdate')


class StakeDeregistration(Base):
    __tablename__ = 'stake_deregistration'
    __table_args__ = (
        UniqueConstraint('addr_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('stake_deregistration_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    cert_index = Column(Integer, nullable=False)
    epoch_no = Column(Integer, nullable=False)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    redeemer_id = Column(ForeignKey('redeemer.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)

    addr = relationship('StakeAddres')
    redeemer = relationship('Redeemer')
    tx = relationship('Tx')


class TxIn(Base):
    __tablename__ = 'tx_in'
    __table_args__ = (
        UniqueConstraint('tx_out_id', 'tx_out_index'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('tx_in_id_seq'::regclass)"))
    tx_in_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    tx_out_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)
    tx_out_index = Column(SmallInteger, nullable=False)
    redeemer_id = Column(ForeignKey('redeemer.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)

    redeemer = relationship('Redeemer')
    tx_in = relationship('Tx', primaryjoin='TxIn.tx_in_id == Tx.id')
    tx_out = relationship('Tx', primaryjoin='TxIn.tx_out_id == Tx.id')


class Withdrawal(Base):
    __tablename__ = 'withdrawal'
    __table_args__ = (
        UniqueConstraint('addr_id', 'tx_id'),
    )

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('withdrawal_id_seq'::regclass)"))
    addr_id = Column(ForeignKey('stake_address.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False,
                     index=True)
    amount = Column(Numeric, nullable=False)
    redeemer_id = Column(ForeignKey('redeemer.id', ondelete='CASCADE', onupdate='RESTRICT'), index=True)
    tx_id = Column(ForeignKey('tx.id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False, index=True)

    addr = relationship('StakeAddres')
    redeemer = relationship('Redeemer')
    tx = relationship('Tx')

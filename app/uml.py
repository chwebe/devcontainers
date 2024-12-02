from sqlalchemy.dialects.postgresql import BYTEA

#region platform
class PlatformBase(Database):
    ID = Column(Integer, primary_key=True)
    Name = Column(String(50), nullable=False, unique=True) # Nom de l'exchange ou de la blockchain
    APIKey = Column(BYTEA, nullable=True)
    endpointUrl = Column(String(50), nullable=False) #nom de l'api ou du RPC URL 
    CreatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ExchangePlatform(PlatformBase):
    SecretKey = Column(BYTEA, nullable=True)

class Blockchain(PlatformBase):
    pass  # Additional fields can be added later   
#endregion

class FiatCurrency(Base):
    __tablename__ = 'fiat_currency'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)  # Identifiant unique pour chaque devise
    Code = Column(String(3), nullable=False, unique=True)  # Code ISO 4217 (e.g., USD, EUR)
    Name = Column(String(50), nullable=False)  # Nom complet (e.g., US Dollar, Euro)
    ConversionRateToUSD = Column(Numeric(20, 8), nullable=False, default=1.0)  # Taux de conversion vers l'USD
    CreatedAt = Column(String, nullable=False, default=datetime.datetime.utcnow)  # Date de création
    UpdatedAt = Column(String, nullable=True, onupdate=datetime.datetime.utcnow)  # Dernière mise à jour

# region transactionBase
class TransactionBase(Database):
    ID = Column(Integer, primary_key=TFalse)
    PlatformBaseID = Column(Integer, ForeignKey('exchange_platform.id'), nullable=False)
    OrderNo = Column(String(255), nullable=False)
    sourceAmount = Column(Numeric(20, 8), nullable=False)
    ObtainAmount = Column(Numeric(20, 8), nullable=False)
    Fee = Column(Numeric(20, 8), nullable=False)
    Status = Column(Enum('PENDING', 'CONFIRMED', 'FAILED', name='transaction_status_enum'), default='PENDING')
    datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

class WithdrawalHistory(TransactionBase):
    pass


class TradeHistory(TransactionBase):
    TradingPairID = Column(Integer, ForeignKey('trading_pair.id', ondelete='CASCADE'), nullable=False)
    Price = Column(Numeric(20, 8), nullable=False)
    Quantity = Column(Numeric(20, 8), nullable=False)
    QuoteQuantity = Column(Numeric(20, 8), nullable=False)
    FeeAsset = Column(String(50), nullable=False)

class BlockchainTransaction(TransactionBase):
    BlockchainID = Column(Integer, ForeignKey('blockchain.id', ondelete='CASCADE'), nullable=False)
    AddressID = Column(Integer, ForeignKey('blockchain_address.id', ondelete='CASCADE'), nullable=False)
    TxHash = Column(String(100), nullable=False, unique=True)
    FromAddress = Column(String(100), nullable=False)
    ToAddress = Column(String(100), nullable=False)
    #---> UniqueConstraint('BlockchainID', 'AddressID', 'TxHash', name='uq_blockchain_transaction') ==> Ajoutez des contraintes uniques pour éviter les doublons, par exemple sur

class DepositHistory(TransactionBase):
    FiatCurrencyID = Column(Integer, ForeignKey('fiat_currency.id'), nullable=False)
    Method = Column(String(50), nullable=False)
    createdAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Payment(DepositHistory):
    CryptoCurrency = Column(String(10), nullable=False)  # Crypto-monnaie obtenue (e.g., USDT)
    PriceConvertion = Column(Numeric(20, 8), nullable=False)  # Prix de la conversion

class Deposit(DepositHistory):
    pass
    Method : ConvertFiatToUSDC

#end region

#region FinancialEntity
class FinancialEntity(Database):
    ID = Column(Integer, primary_key=True)
    PlatformID = Column(Integer, ForeignKey('platform.id', ondelete='SET NULL'), nullable=True)
    Name = Column(String(100), nullable=False)  # Nom du symbole, de l'actif ou de l'adresse
    CreatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class TradingPair(FinancialEntity):
    BaseAsset = Column(String(10), nullable=False)  # Actif de base, e.g., BTC
    QuoteAsset = Column(String(10), nullable=False)  # Actif de cotation, e.g., USDT
    isTrade = Column(Boolean, nullable=False)  # Indique si cette paire est échangeable

class Asset(FinancialEntity):
    IsBuyer = Column(Boolean, nullable=False)  # Indique si cet actif est acheteur

class BlockchainAddress(FinancialEntity):
    BlockchainID = Column(Integer, ForeignKey('blockchain.id', ondelete='CASCADE'), nullable=False)
    Label = Column(String(50), nullable=True)  # Nom ou description de l'adresse (e.g., "Wallet principal")

#endregion

# region table intermediaire

class platform_trading_pair(Database):
    PlatformID = Column(Integer, ForeignKey('platform.id', ondelete='CASCADE'), primary_key=True)
    TradingPairID = Column(Integer, ForeignKey('trading_pair.id', ondelete='CASCADE'), primary_key=True)
    CreatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class platform_financial_entity(Database):
    PlatformID = Column(Integer, ForeignKey('platform.id', ondelete='CASCADE'), primary_key=True)
    FinancialEntityID = Column(Integer, ForeignKey('financial_entity.id')), ondelete
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# region LATER
class User(Database):
    ID = Column(Integer, primary_key=True)
    Username = Column(String(50), nullable=False)
    Role = Column(Enum('ADMIN', 'USER', 'READ_ONLY', name='role_enum'), nullable=False)

# LOGS
class APILog(Database):
    ID = Column(Integer, primary_key=True)
    ExchangeID = Column(Integer, ForeignKey('exchange_platform.id'), nullable=False)
    Endpoint = Column(String(255), nullable=False)
    ResponseTime = Column(Float, nullable=False)
    StatusCode = Column(Integer, nullable=False)
    Timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

class AuditLog(Database):
    ID = Column(Integer, primary_key=True)
    TableName = Column(String(50), nullable=False)
    RecordID = Column(Integer, nullable=False)
    Action = Column(Enum('INSERT', 'UPDATE', 'DELETE', name='action_enum'), nullable=False)
    ModifiedBy = Column(String(50), nullable=True)
    Timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    ChangeDetails = Column(JSON, nullable=True)
#endregion

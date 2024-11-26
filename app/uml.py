from sqlalchemy.dialects.postgresql import BYTEA

#region platform
class PlatformBase(Database):
    ID = Column(Integer, primary_key=True)
    Name = Column(String(50), nullable=False, unique=True) # Nom de l'exchange ou de la blockchain
    APIKey = Column(BYTEA, nullable=True)
    endpoints = Column(String(50), nullable=False) #nom de l'api ou du RPC URL 
    CreatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ExchangePlatform(PlatformBase):
    SecretKey = Column(BYTEA, nullable=True)

class Blockchain(PlatformBase):
    Pass  # Additional fields can be added later   
#endregion

# region transactionBase
class TransactionBase(Database):
    ID = Column(Integer, primary_key=TFalse
    Timestamp = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    Amount = Column(Numeric(20, 8), nullable=False)
    Status = Column(Enum('PENDING', 'CONFIRMED', 'FAILED', name='transaction_status_enum'), default='PENDING')

class TradeHistory(TransactionBase):
    Symbol = Column(String(50), nullable=False)
    OrderID = Column(BigInteger, nullable=False)
    Price = Column(Numeric(20, 8), nullable=False)
    Quantity = Column(Numeric(20, 8), nullable=False)
    QuoteQuantity = Column(Numeric(20, 8), nullable=False)
    Commission = Column(Numeric(20, 8), nullable=False)
    CommissionAsset = Column(String(50), nullable=False)

class BlockchainTransaction(TransactionBase):
    BlockchainID = Column(Integer, ForeignKey('blockchain.id', ondelete='CASCADE'), nullable=False)
    AddressID = Column(Integer, ForeignKey('blockchain_address.id', ondelete='CASCADE'), nullable=False)
    TxHash = Column(String(100), nullable=False, unique=True)
    FromAddress = Column(String(100), nullable=False)
    ToAddress = Column(String(100), nullable=False)
    Fee = Column(Numeric(20, 8), nullable=True)

class DepositHistory(TransactionBase):
    OrderNo = Column(String(255), nullable=False)
    FiatCurrency = Column(String(10), nullable=False)
    Price = Column(Numeric(20, 8), nullable=False)
    TotalFee = Column(Numeric(20, 8), nullable=False)
    Method = Column(String(50), nullable=False)

class Payment(DepositHistory):
    SourceAmount = Column(Numeric(20, 8), nullable=False)  # Montant initial en fiat
    ObtainAmount = Column(Numeric(20, 8), nullable=False)  # Montant obtenu en crypto
    CryptoCurrency = Column(String(10), nullable=False)  # Crypto-monnaie obtenue (e.g., USDT)
    Price = Column(Numeric(20, 8), nullable=False)  # Prix de la conversion

class Deposit(DepositHistory):
    IndicatedAmount = Column(Numeric(20, 8), nullable=False)  # Montant indiqué par l'utilisateur
    Amount = Column(Numeric(20, 8), nullable=False)  # Montant final reçu après frais

#end region
class TradingPair(Database):
    ID = Column(Integer, primary_key=True)
    ExchangeID = Column(Integer, ForeignKey('exchange_platform.id'), nullable=False)
    Symbol = Column(String(10), nullable=False)
    BaseAsset = Column(String(10), nullable=False) # 
    QuoteAsset = Column(String(10), nullable=False)

#region FinancialEntity
class FinancialEntity(Database):
    ID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)  # Nom du symbole, de l'actif ou de l'adresse
    PlatformID = Column(Integer, nullable=True)  # ID de la plateforme d'échange ou de la blockchain
    CreatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    UpdatedAt = Column(DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class TradingPair(FinancialEntity):
    BaseAsset = Column(String(10), nullable=False)  # Actif de base, e.g., BTC
    QuoteAsset = Column(String(10), nullable=False)  # Actif de cotation, e.g., USDT

class Asset(FinancialEntity):
    IsBuyer = Column(Boolean, nullable=False)  # Indique si cet actif est acheteur

class BlockchainAddress(FinancialEntity):
    BlockchainID = Column(Integer, ForeignKey('blockchain.id', ondelete='CASCADE'), nullable=False)
    Label = Column(String(50), nullable=True)  # Nom ou description de l'adresse (e.g., "Wallet principal")

#endregion

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
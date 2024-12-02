
-- create table platform
CREATE TYPE platform_type AS ENUM ('ExchangePlatform', 'Blockchain');

CREATE TABLE platform (
    ID SERIAL PRIMARY KEY, -- SERIAL pour auto-incrémentation
    Name VARCHAR(50) NOT NULL UNIQUE,
    APIKey BYTEA,
    endpointUrl VARCHAR(50) NOT NULL,
    Type platform_type NOT NULL, -- Utilisation de l'ENUM personnalisé
    SecretKey BYTEA, -- Nullable, utilisé uniquement si Type = 'ExchangePlatform'
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to update UpdatedAt field
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.UpdatedAt = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON platform
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- create trabnsaction transaction_base table

CREATE TYPE transaction_status AS ENUM ('PENDING', 'CONFIRMED', 'FAILED');
CREATE TYPE transaction_type AS ENUM ('TRADE','DEPOSIT', 'WITHDRAWAL') NOT NULL; 

-- Étape 2: Créer la table
CREATE TABLE transaction_base (
    ID SERIAL PRIMARY KEY,
    PlatformID INT NOT NULL,
    OrderNo VARCHAR(255) NOT NULL,
    sourceAmount NUMERIC(20, 8) NOT NULL,
    ObtainAmount NUMERIC(20, 8) NOT NULL,
    Fee NUMERIC(20, 8) NOT NULL,
    Status transaction_status DEFAULT 'PENDING',
    Type transaction_type NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (PlatformID) REFERENCES platform(ID)
);

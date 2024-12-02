| **Entité 1**          | **Relation**           | **Entité 2**              | **Table d'association (si nécessaire)** | **Colonnes clés**                                    |
|-----------------------|------------------------|---------------------------|------------------------------------------|-----------------------------------------------------|
| **PlatformBase**      | 1 → N                 | **FinancialEntity**       | N/A                                      | `PlatformBase.ID` → `FinancialEntity.PlatformID`    |
| **PlatformBase**      | 1 → N                 | **TransactionBase**       | N/A                                      | `PlatformBase.ID` → `TransactionBase.PlatformBaseID`|
| **TransactionBase**   | 1 → 1 (inheritance)   | **WithdrawalHistory**     | N/A                                      | Inherited from `TransactionBase`                   |
| **TransactionBase**   | 1 → 1 (inheritance)   | **TradeHistory**          | N/A                                      | Inherited from `TransactionBase`                   |
| **TransactionBase**   | 1 → 1 (inheritance)   | **BlockchainTransaction** | N/A                                      | Inherited from `TransactionBase`                   |
| **TransactionBase**   | 1 → 1 (inheritance)   | **DepositHistory**        | N/A                                      | Inherited from `TransactionBase`                   |
| **FiatCurrency**      | 1 → N                 | **DepositHistory**        | N/A                                      | `FiatCurrency.ID` → `DepositHistory.FiatCurrencyID`|
| **Blockchain**        | 1 → N                 | **BlockchainTransaction** | N/A                                      | `Blockchain.ID` → `BlockchainTransaction.BlockchainID`|
| **Blockchain**        | 1 → N                 | **BlockchainAddress**     | N/A                                      | `Blockchain.ID` → `BlockchainAddress.BlockchainID` |
| **TradingPair**       | N → N                 | **PlatformBase**          | **platform_trading_pair**                | `TradingPair.ID`, `PlatformBase.ID`                |
| **PlatformBase**      | N → N                 | **FinancialEntity**       | **platform_financial_entity**            | `PlatformBase.ID`, `FinancialEntity.ID`            |

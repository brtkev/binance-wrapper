
class WrapperError(Exception):
    pass

class ConnectionError(WrapperError):
    pass

class InsuficientBalance(WrapperError):
    pass
    # def __init__(self, balance, transactionQty, message = "Account has insufficient balance for requested action.")
    #     self.balance = balance
    #     self.transactionQty = transactionQty
    #     self.message = message
    #     super().__init__(self.message)

    # def __str__(self):
    #     return f'{balance} less than {transactionQty} -> {self.message}'

class RepayExceedsBorrow(WrapperError):
    pass
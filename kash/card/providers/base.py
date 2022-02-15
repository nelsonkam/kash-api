

class BaseCardProvider:
    def issue(self, card, initial_amount):
        raise NotImplementedError()

    def fund(self, card, amount):
        raise NotImplementedError()

    def withdraw(self, card, amount):
        raise NotImplementedError()

    def freeze(self, card):
        raise NotImplementedError()

    def unfreeze(self, card):
        raise NotImplementedError()

    def terminate(self, card):
        raise NotImplementedError()

    def get_details(self, card):
        raise NotImplementedError()

    def get_statement(self, card):
        raise NotImplementedError()

    def get_transactions(self, card):
        raise NotImplementedError()

    def is_balance_sufficient(self, amount):
        raise NotImplementedError()
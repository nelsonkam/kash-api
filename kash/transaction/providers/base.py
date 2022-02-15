

class BaseProvider:
    def process(self, transaction):
        raise NotImplementedError()

    def payout(self, transaction):
        raise NotImplementedError()

    def refund(self, transaction):
        raise NotImplementedError()

    def retry(self, transaction):
        raise NotImplementedError()

    def check_status(self, transaction):
        raise NotImplementedError()
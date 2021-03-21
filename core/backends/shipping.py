from djmoney.money import Money



class DHLExpressBackend:

    def get_rates(self,  region, **kwargs):
        origin = kwargs.get('origin')
        items = kwargs.get('items')
        if origin in ['benin', 'bj']:
            return []
        weight = 0
        for item in items:
            weight += (item.product.weight or 1) * item.quantity
        price = 22000 if weight <= 2 else 22000 + (6300 * (weight - 2))
        return [{'name': 'Express', 'description': '3-5 jours ouvrables', 'price': Money(price, "XOF")}]


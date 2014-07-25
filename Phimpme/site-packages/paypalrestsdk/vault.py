from paypalrestsdk.resource import Find, Create, Delete


class CreditCard(Find, Create, Delete):
    """Use vault api to avoid having to store sensitive information
    such as credit card related details on your server. API docs at
    https://developer.paypal.com/docs/api/#vault

    Usage::

        >>> credit_card = CreditCard.find("CARD-5BT058015C739554AKE2GCEI")
        >>> credit_card = CreditCard.new({'type': 'visa'})

        >>> credit_card.create()  # return True or False
    """
    path = "v1/vault/credit-card"

CreditCard.convert_resources['credit_card'] = CreditCard

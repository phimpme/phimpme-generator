import paypalrestsdk.util as util
from paypalrestsdk.resource import List, Find, Delete, Create, Update, Post, Resource
from paypalrestsdk.api import default as default_api


class Invoice(List, Find, Create, Delete, Update, Post):
    """Invoice class wrapping the REST v1/invoices/invoice endpoint

    Usage::

        >>> invoice_histroy = Invoice.all({"count": 5})

        >>> invoice = Invoice.new({})
        >>> invoice.create()     # return True or False
    """
    path = "v1/invoicing/invoices"

    def send(self):
        return self.post('send', {}, self)

    def remind(self, attributes):
        return self.post('remind', attributes, self)

    def cancel(self, attributes):
        return self.post('cancel', attributes, self)

    @classmethod
    def search(cls, params=None, api=None):
        api = api or default_api()
        params = params or {}

        url = util.join_url(cls.path, 'search')

        return Resource(api.post(url, params), api=api)

Invoice.convert_resources['invoices'] = Invoice
Invoice.convert_resources['invoice'] = Invoice

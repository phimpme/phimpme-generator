import uuid

import paypalrestsdk.util as util
from paypalrestsdk.api import default as default_api


class Resource(object):
    """Base class for all REST services
    """
    convert_resources = {}

    def __init__(self, attributes=None, api=None):
        attributes = attributes or {}
        self.__dict__['api'] = api or default_api()

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('error', None)
        super(Resource, self).__setattr__('headers', {})
        super(Resource, self).__setattr__('header', {})
        super(Resource, self).__setattr__('request_id', None)
        self.merge(attributes)

    def generate_request_id(self):
        """Generate uniq request id
        """
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())
        return self.request_id

    def http_headers(self):
        """Generate HTTP header
        """
        return util.merge_dict(self.header, self.headers,
                               {'PayPal-Request-Id': self.generate_request_id()})

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        try:
            # Handle attributes(error, header, request_id)
            super(Resource, self).__getattribute__(name)
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def success(self):
        return self.error is None

    def merge(self, new_attributes):
        """Merge new attributes e.g. response from a post to Resource
        """
        for k, v in new_attributes.items():
            setattr(self, k, v)

    def convert(self, name, value):
        """Convert the attribute values to configured class
        """
        if isinstance(value, dict):
            cls = self.convert_resources.get(name, Resource)
            return cls(value, api=self.api)
        elif isinstance(value, list):
            new_list = []
            for obj in value:
                new_list.append(self.convert(name, obj))
            return new_list
        else:
            return value

    def __getitem__(self, key):
        return self.__data__[key]

    def __setitem__(self, key, value):
        self.__data__[key] = self.convert(key, value)

    def to_dict(self):

        def parse_object(value):
            if isinstance(value, Resource):
                return value.to_dict()
            elif isinstance(value, list):
                new_list = []
                for obj in value:
                    new_list.append(parse_object(obj))
                return new_list
            else:
                return value

        data = {}
        for key in self.__data__:
            data[key] = parse_object(self.__data__[key])
        return data


class Find(Resource):

    @classmethod
    def find(cls, resource_id, api=None):
        """Locate resource e.g. payment with given id

        Usage::
            >>> payment = Payment.find("PAY-1234")
        """
        api = api or default_api()

        url = util.join_url(cls.path, str(resource_id))
        return cls(api.get(url), api=api)


class List(Resource):

    list_class = Resource

    @classmethod
    def all(cls, params=None, api=None):
        """Get list of payments as on
        https://developer.paypal.com/docs/api/#list-payment-resources

        Usage::

            >>> payment_histroy = Payment.all({'count': 2})
        """
        api = api or default_api()

        if params is None:
            url = cls.path
        else:
            url = util.join_url_params(cls.path, params)
        return cls.list_class(api.get(url), api=api)


class Create(Resource):

    def create(self, refresh_token=None, correlation_id=None):
        """Creates a resource e.g. payment

        Usage::

            >>> payment = Payment({})
            >>> payment.create() # return True or False
        """

        headers = {}
        if correlation_id is not None:
            headers = util.merge_dict(
                self.http_headers(),
                {'Paypal-Application-Correlation-Id': correlation_id}
            )
        else:
            headers = self.http_headers()

        new_attributes = self.api.post(self.path, self.to_dict(), headers, refresh_token)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Update(Resource):
    """Update a resource

    Usage::

        >>> invoice.update()
    """

    def update(self, attributes=None, refresh_token=None):
        attributes = attributes or self.to_dict()
        url = util.join_url(self.path, str(self['id']))
        new_attributes = self.api.put(url, attributes, self.http_headers(), refresh_token)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Replace(Resource):
    """Partial update or modify resource

    Usage::

        >>> billing_plan.replace([ { 'op': 'replace', 'path': '/merchant-preferences', 'value': {}} ])
    """

    def replace(self, attributes=None, refresh_token=None):
        attributes = attributes or self.to_dict()
        url = util.join_url(self.path, str(self['id']))
        new_attributes = self.api.patch(url, attributes, self.http_headers(), refresh_token)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Delete(Resource):

    def delete(self):
        """Deletes a resource e.g. credit_card

        Usage::

            >>> credit_card.delete()
        """
        url = util.join_url(self.path, str(self['id']))
        new_attributes = self.api.delete(url)
        self.error = None
        self.merge(new_attributes)
        return self.success()


class Post(Resource):

    def post(self, name, attributes=None, cls=Resource, fieldname='id'):
        """Constructs url with passed in headers and makes post request via
        post method in api class.

        Usage::

            >>> payment.post("execute", {'payer_id': '1234'}, payment)  # return True or False
            >>> sale.post("refund", {'payer_id': '1234'})  # return Refund object
        """
        attributes = attributes or {}
        url = util.join_url(self.path, str(self[fieldname]), name)
        if not isinstance(attributes, Resource):
            attributes = Resource(attributes, api=self.api)
        new_attributes = self.api.post(url, attributes.to_dict(), attributes.http_headers())
        if isinstance(cls, Resource):
            cls.error = None
            cls.merge(new_attributes)
            return self.success()
        else:
            return cls(new_attributes, api=self.api)

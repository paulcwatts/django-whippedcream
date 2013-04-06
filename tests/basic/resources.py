from datetime import datetime

from tastypie.resources import Resource
from tastypie import fields
from whippedcream.fields import DateTimeField
from whippedcream.mixins import PyAccessMixin
from whippedcream.serializer import Serializer


class Name(object):
    def __init__(self, id=0, name=None):
        self.id = id
        self.name = name


class DateTime(object):
    def __init__(self, dt=None):
        self.dt = dt
        try:
            import pytz
            if dt:
                self.dt_aware = dt.replace(tzinfo=pytz.utc)
        except ImportError:
            # We can't test this...
            pass


NAMES = [
    Name(1, 'John Lennon'),
    Name(2, 'Paul McCartney'),
    Name(3, 'George Harrison'),
    Name(4, 'Ringo Starr')
]


class NamesResourceDefault(Resource):
    id = fields.IntegerField('id')
    name = fields.CharField('name')

    class Meta:
        resource_name = 'names_default'
        detail_uri_name = 'id'
        object_class = Name
        list_allowed_methods = ('get',)
        detail_allowed_methods = ('get',)

    def obj_get_list(self, bundle, **kwargs):
        return NAMES


class NamesResource(PyAccessMixin, Resource):
    id = fields.IntegerField('id')
    name = fields.CharField('name')

    class Meta:
        resource_name = 'names'
        object_class = Name
        serializer = Serializer()
        detail_uri_name = 'id'
        list_allowed_methods = ('get',)
        detail_allowed_methods = ('get',)

    def obj_get_list(self, bundle, **kwargs):
        return NAMES


class DateTimeResource(Resource):
    dt_default = fields.DateTimeField('dt')
    dt_normalized = DateTimeField('dt', normalize=True)
    dt = DateTimeField('dt', normalize=False)

    dt_aware_default = fields.DateTimeField('dt_aware')
    dt_aware_normalized = DateTimeField('dt_aware', normalize=True)
    dt_aware = DateTimeField('dt_aware', normalize=False)

    class Meta:
        resource_name = 'dt'
        object_class = DateTime
        serializer = Serializer(allow_aware_datetime=True)
        detail_uri_name = 'id'
        detail_allowed_methods = ('get',)

    def obj_get(self, bundle, **kwargs):
        id = kwargs.get('id')
        # Replace the '_' with a '.' to make this a timestamp
        # (Yes, I know this is ugly, it's just for testing)
        ts = float(id.replace('_', '.'))
        return DateTime(datetime.utcfromtimestamp(ts))

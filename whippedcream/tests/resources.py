import six

from datetime import datetime

from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound
from tastypie.resources import Resource
from tastypie import fields
from whippedcream.fields import DateTimeField, FileField
from whippedcream.mixins import PyAccessMixin, MultiPartFormDataMixin
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


class FileObj(object):
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


FILES = []


class FileResource(MultiPartFormDataMixin, Resource):
    myfile = FileField('myfile', null=True)
    myabsfile = FileField('absfile', absolute=True, null=True)

    class Meta:
        resource_name = 'file'
        object_class = FileObj
        list_allowed_methods = ('post',)
        detail_allowed_methods = ('get',)
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle.obj = self._meta.object_class()
        for key, value in six.iteritems(kwargs):
            setattr(bundle.obj, key, value)

        setattr(bundle.obj, 'pk', len(FILES) + 1)
        bundle = self.full_hydrate(bundle)
        return self.save(bundle)

    def save(self, bundle, skip_errors=False):
        FILES.append(bundle.obj)
        return bundle

    def obj_get(self, bundle, **kwargs):
        try:
            bundle.obj = FILES[int(kwargs['pk']) - 1]
            return bundle.obj
        except (KeyError, ValueError):
            raise NotFound("Invalid resource lookup data provided (mismatched type).")

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj.obj, self._meta.detail_uri_name)
        else:
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj, self._meta.detail_uri_name)

        return kwargs

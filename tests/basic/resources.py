from tastypie.resources import Resource
from tastypie import fields
from whippedcream.serializer import Serializer


class Name(object):
    def __init__(self, id=0, name=None):
        self.id = id
        self.name = name


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


class NamesResource(Resource):
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

from tastypie.api import Api

from resources import NamesResourceDefault, \
    NamesResource, \
    DateTimeResource


v1_api = Api(api_name='v1')
v1_api.register(NamesResourceDefault())
v1_api.register(NamesResource())
v1_api.register(DateTimeResource())

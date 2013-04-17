from tastypie.api import Api as BaseApi

from whippedcream.api import Api
from resources import NamesResourceDefault, \
    NamesResource, \
    DateTimeResource


v1_api = BaseApi(api_name='v1')
v1_api.register(NamesResourceDefault())
v1_api.register(NamesResource())
v1_api.register(DateTimeResource())


noname_api = Api()
noname_api.register(NamesResourceDefault())
noname_api.register(NamesResource())

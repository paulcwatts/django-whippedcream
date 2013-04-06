

class PyAccessMixin(object):
    """
    Provides a simple way of getting serialized JSON from
    a resource from python. This is basically a simple way
    of implementing this recipe:
    http://django-tastypie.readthedocs.org/en/latest/cookbook.html#using-your-resource-in-regular-views
    """

    def get_json(self, request, obj):
        bundle = self.build_bundle(obj=obj, request=request)
        return self.serialize(None, self.full_dehydrate(bundle),
                              'application/json')

    def get_json_list(self, request, obj_list):
        bundles = [self.build_bundle(obj=obj, request=request)
                   for obj in obj_list]
        to_be_serialized = [self.full_dehydrate(bundle) for bundle in bundles]
        return self.serialize(None, to_be_serialized, 'application/json')

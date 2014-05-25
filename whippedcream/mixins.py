import warnings

from django.http import HttpResponse
from tastypie import http
from tastypie.utils import dict_strip_unicode_keys
from tastypie.utils.mime import build_content_type


class PyAccessMixin(object):
    """
    Allows "dict" access to resources within Python. Used in views.

    Copied from tastypie, but implemented similarly to a pattern
    described here:
    http://django-tastypie.readthedocs.org/en/latest/cookbook.html#using-your-resource-in-regular-views
    """
    def get_json(self, request, obj):
        warnings.warn("use obj_to_simple instead", DeprecationWarning)
        bundle = self.build_bundle(obj=obj, request=request)
        return self.serialize(None, self.full_dehydrate(bundle),
                              'application/json')

    def get_json_list(self, request, obj_list):
        warnings.warn("use list_to_simple instead", DeprecationWarning)
        bundles = [self.build_bundle(obj=obj, request=request)
                   for obj in obj_list]
        to_be_serialized = [self.full_dehydrate(bundle) for bundle in bundles]
        return self.serialize(None, to_be_serialized, 'application/json')

    def get_queryset(self):
        return self._meta.queryset

    def obj_to_simple(self, request, obj):
        bundle = self.build_bundle(obj=obj, request=request)
        return self._meta.serializer.to_simple(self.full_dehydrate(bundle), {})

    def list_to_simple(self, request, obj_list, limit=None):
        limit = limit if limit is not None else self._meta.limit
        paginator = self._meta.paginator_class(request.GET, obj_list,
                                               resource_uri=self.get_resource_uri(),
                                               limit=limit,
                                               max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle))

        to_be_serialized[self._meta.collection_name] = bundles
        return self._meta.serializer.to_simple(to_be_serialized, {})


class MultiPartFormDataMixin(object):
    """
    This is a mixin class that allows creating new objects by posting
    multi-part/form data rather than the normal serialized type.

    Specifically, this allows file upload as well by dehydrating request.FILES
    """

    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """
        bundle = self.build_bundle(data=dict_strip_unicode_keys(request.POST), request=request)
        bundle.files = request.FILES

        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_upload_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def create_upload_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        A version of create_response that includes the XMLHttpRequest/IE detailed hack here:
        https://github.com/blueimp/jQuery-File-Upload/wiki/Setup, Content-Type Negotiation section
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)

        if 'HTTP_ACCEPT' in request.META:
            types = [t.strip() for t in request.META['HTTP_ACCEPT'].split(',')]
            if desired_format not in types:
                desired_format = 'text/plain'

        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

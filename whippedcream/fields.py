from tastypie.fields import DateTimeField as BaseDateTimeField, FileField as BaseFileField


class DateTimeField(BaseDateTimeField):
    """Normalizes a datetime field by removing the microseconds."""
    def __init__(self, *args, **kwargs):
        self.normalize = kwargs.pop('normalize', True)
        super(DateTimeField, self).__init__(*args, **kwargs)

    def dehydrate(self, bundle, for_list=True):
        value = super(DateTimeField, self).dehydrate(bundle)
        if value:
            value = value.replace(microsecond=0)
        return value

    def hydrate(self, bundle):
        value = super(DateTimeField, self).hydrate(bundle)
        if value:
            value = value.replace(microsecond=0)
        return value


class FileField(BaseFileField):
    """
    Provides a way of dehydrating the file URL as an absolute URL,
    as well as hydrating using the 'files' bundle attribute to use
    multipart/form-data to upload a file. To use this, you can
    also use the FileUploadMixin to handle multipart/form-data
    in a post_list handler.
    """
    def __init__(self, *args, **kwargs):
        self.absolute = kwargs.pop('absolute', False)
        super(FileField, self).__init__(*args, **kwargs)

    def dehydrate(self, bundle, for_list=True):
        value = super(FileField, self).dehydrate(bundle)
        if value and self.absolute and hasattr(bundle, 'request'):
            value = bundle.request.build_absolute_uri(str(value))
        return value

    def hydrate(self, bundle):
        "The only difference with the base class is we check the 'files' bundle attribute."
        if self.readonly:
            return None
        if not hasattr(bundle, 'files'):
            return None

        if self.instance_name not in bundle.files:
            return super(FileField, self).hydrate(bundle)

        return bundle.files[self.instance_name]

from tastypie.fields import DateTimeField as BaseDateTimeField


class DateTimeField(BaseDateTimeField):
    """Normalizes a datetime field by removing the microseconds."""
    def __init__(self, *args, **kwargs):
        self.normalize = kwargs.pop('normalize', True)
        super(DateTimeField, self).__init__(*args, **kwargs)

    def dehydrate(self, bundle):
        value = super(DateTimeField, self).dehydrate(bundle)
        if value:
            value = value.replace(microsecond=0)
        return value

    def hydrate(self, bundle):
        value = super(DateTimeField, self).hydrate(bundle)
        if value:
            value = value.replace(microsecond=0)
        return value

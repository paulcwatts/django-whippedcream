from tastypie.serializers import Serializer as BaseSerializer
from tastypie.utils import format_datetime, make_naive


class Serializer(BaseSerializer):
    """
    This serializer allows you to pass aware-datetime objects through and
    have them serialized with a timezone value. Pass allow_aware_datetime=True
    to the constructor.
    """
    def __init__(self, *args, **kwargs):
        self.allow_aware_datetime = kwargs.pop('allow_aware_datetime', False)
        super(Serializer, self).__init__(*args, **kwargs)

    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14".
        """
        if not self.allow_aware_datetime:
            data = make_naive(data)
        if self.datetime_formatting == 'rfc-2822':
            return format_datetime(data)

        return data.isoformat()

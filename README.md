# django-whippedcream

The perfect counterpart to [django-tastypie](https://github.com/toastdriven/django-tastypie).

django-whippedcream provides a few mixins and utilities that I've used to make
my life with tastypie easier. 

## Requirements

django-tastypie, of course. pytz is also recommended, and required for <code>UTCDateTimeField</code>

## Serializer

Want to browse your API through the browser? Try doing that but not adding format=json,
you get an error that format=html isn't implement.

Now it is -- very simply. But it allows you to view a GET request from the browser.
What's best, if you have django-debug-toolbar installed (and why wouldn't you)
you can see the DB queries used to create this request.

    from whippedcream.serializer import Serializer

    class MyResource(Resource):
        # fields...

        class Meta:
            serializer = Serializer()

## UTCDateTimeField

This returns a normalized version of a DateTimeField. It removes any milliseconds
and converted naive datetimes to aware datetimes.

    from whippedcream.fields import UTCDateTimeField

## Mixins

### ViewAccessMixin


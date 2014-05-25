# django-whippedcream

[![Build Status](https://travis-ci.org/paulcwatts/django-whippedcream.svg)](https://travis-ci.org/paulcwatts/django-whippedcream)

The perfect counterpart to [django-tastypie](https://github.com/toastdriven/django-tastypie).

django-whippedcream provides a few mixins and utilities that I've used to make
my life with tastypie easier. 

## Requirements

django-tastypie, of course. 

## Serializer

Want to browse your API through the browser? Try doing that but not adding format=json,
you get an error that format=html isn't implement.

Now it is -- very simply. But it allows you to view a GET request from the browser.
What's best, if you have django-debug-toolbar installed (and why wouldn't you)
you can see the DB queries used to create this request.

    from whippedcream.serializer import Serializer

    class MyResource(Resource):
        class Meta:
            serializer = Serializer()

In addition, the serializer allows you to serialize aware datetimes, something
which the default serialized can't (at the time of this writing).

## DateTimeField

This is a simple addition to the DateTimeField that removes milliseconds
from the field. This is useful if you don't want to provide that level
of accuracy, but also if your database engine doesn't store that level
of accuracy (MySQL).

    from whippedcream.fields import DateTimeField

    class MyResource(Resource):
        dt = DateTimeField('dt', normalize=True)

## PyAccessMixin

This mixin class can be added to any resource where you may want to 
access a serialized (JSON) version in any of your regular python code.
It basically implements this pattern:

http://django-tastypie.readthedocs.org/en/latest/cookbook.html#using-your-resource-in-regular-views

    from whippedcream.mixins import PyAccessMixin

    class MyResource(MyAccessMixin, Resource):
        pass

    # elsewhere...
    result = MyResource().get_json(request, obj)


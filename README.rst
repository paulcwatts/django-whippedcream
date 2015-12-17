===================
django-whippedcream
===================

.. image:: https://travis-ci.org/paulcwatts/django-whippedcream.png?branch=master   
   :target: https://travis-ci.org/paulcwatts/django-whippedcream

The perfect counterpart to django-tastypie_.

django-whippedcream provides a few mixins and utilities that I've used to make
my life with tastypie easier. 

Tested using django-tastypie>0.12, Django>1.7, and Python 2.7 and >3.4

Requirements
============

django-tastypie, of course. Also pytz if you want to use the DateTimeSerializer.

Installation
============

1. Install: ``pip install django-whippedcream``
2. Add ``whippedcream`` to your ``INSTALLED_APPS``.

DateTimeField
-------------

This is a simple addition to the DateTimeField that removes milliseconds
from the field. This is useful if you don't want to provide that level
of accuracy, but also if your database engine doesn't store that level
of accuracy (MySQL).

::

    from whippedcream.fields import DateTimeField

    class MyResource(Resource):
        dt = DateTimeField('dt', normalize=True)

PyAccessMixin
-------------

This mixin class can be added to any resource where you may want to 
access a serialized (JSON) version in any of your regular python code.
It basically implements this pattern:

http://django-tastypie.readthedocs.org/en/latest/cookbook.html#using-your-resource-in-regular-views

::

    from whippedcream.mixins import PyAccessMixin

    class MyResource(MyAccessMixin, Resource):
        pass

    # elsewhere...
    result = MyResource().obj_to_simple(request, obj)


.. _django-tastypie: https://github.com/toastdriven/django-tastypie
.. _intro:

Introduction
============

Achilles provides a framework to create Django applications using AJAX. Trough the use of some primitives it allows you to build asynchronous without the need of writting javascript to manage client side.

The name of the project comes from ancient Greek mythology, Achilles and Ajax where soldiers who fough together in Trojan War.

.. figure:: static/img/ajax_achilles.jpg
    :align: center
    :alt: Ajax and Achilles amphora
    :figclass: align-center

    Ajax and Achilles amphora
    painted by Exekias (Greek, 540 BCE)

Features
--------

This is a basic list of features provided by Achilles:

* Integration with JQuery and Django (>=1.4)
* Asynchronous server side action calling (with return values)
* Dynamically loaded (HTML) blocks

Installation
------------

#. Run ``pip install django-achilles``
#. Add ``achilles`` to `INSTALLED_APPS` in Django settings:

.. code-block:: django
    :emphasize-lines: 7

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'myapp',
        'achilles',
    )

#. Create achilles endpoint adding ``achilles.urls`` to your `urls.py` file:

.. code-block:: django
    :emphasize-lines: 6

    from django.conf.urls import patterns, url, include
    from myapp.views import SomeView

    urlpatterns = patterns('',
        url(r'^$', SomeView.as_view(), name='home'),
        url(r'^achilles$', include('achilles.urls')),
    )

You are ready to start using Achilles! Now you can follow with the :ref:`tutorial`

ESP SDK Python
==============

A Python interface for calling the Evident.io_ API.

.. _Evident.io: https://evident.io

This is still being built and subject to changes.

Installation
------------

Install the latest stable using pip::

    pip install esp

If you prefer to install from the latest git HEAD, you can use the setup.py script::

    git clone https://github.com/EvidentSecurity/esp-sdk-python
    cd esp-sdk-python
    python setup.py install

Configuration
-------------

The recommended way to set your keys is with environment variables. Export one
for your access key and another one for your secret access key::

    export ENV['ESP_ACCESS_KEY_ID']='access key from ESP'
    export ENV['ESP_SECRET_ACCESS_KEY']='secret access key from ESP'

You can also set them in the ESP module directly::

    from esp.settings import settings
    
    settings.access_key_id = 'access key from ESP'
    settings.secret_access_key = 'secret access key from ESP'

If you need to use an http proxy to hit the ESP API, you can set that using the
settings as well::

    settings.http_proxy = 'your-proxy-uri:8080'

For appliance users, you can change the host the SDK points at in the settings::

    settings.host = 'esp.my-host'

Usage
-----

All resources provided are class objects. You they export common methods to help
you interact with the ESP API. Below are a few examples that describe how the
SDK can be used.

Import the SDK using the "esp" namespace::

    In [1]: import esp

Fetching reports is simple::

    In [2]: reports = esp.Report.find()

    In [3]: reports
    Out[3]: <esp.resource.PaginatedCollection at 0x10b291dd8>

This returns a paginated collection object that will let you navigate the pages returned::

    In [4]: reports.current_page_number
    Out[4]: '1'

    In [5]: reports = reports.next_page()

    In [6]: reports.current_page_number
    Out[6]: '2'

This object acts like a list and supports indexing and the len() function::

    In [7]: len(reports)
    Out[7]: 20

    In [8]: reports[0]
    Out[8]: <esp.report.Report at 0x10b2ce278>

Lets checkout that report::

    In [10]: report.id_
    Out[10]: '592'

    In [11]: report.status
    Out[11]: 'complete'

    In [12]: report.alerts
    Out[12]: <esp.resource.PaginatedCollection at 0x10b2d68d0>

Looks like it's complete and we have alerts attached to it. calling .alerts
returns a PaginatedCollection of Alert objects, lets look at one::

    In [14]: alert = report.alerts[0]

    In [15]: alert.id_
    Out[15]: '97'

    In [16]: alert.resource
    Out[16]: 'fisheye-rel-build'

    In [17]: alert.status
    Out[17]: 'pass'

    In [19]: alert.signature.name
    Out[19]: 'VPC ELB Security Groups'

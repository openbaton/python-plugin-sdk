Copyright © 2015-2016 `Open Baton`_. Licensed under `Apache v2
License`_.

Python version of the plugin-sdk
================================

This project contains a Python SDK for writing VIM Drivers for Open
Baton.


Technical Requirements
----------------------

This section covers the requirements that must be met by the plugin-sdk in order to satisfy the demands for such a component:

-  python 3.5
-  pika


How to install python-plugin-sdk
--------------------------------

The safer way to start is to use a `virtal environment`_. Once
activated, just run

.. code:: bash

   pip install python-plugin-sdk

How to use the SDK
------------------

After it is installed you can import the following modules into your
project:

-  org.openbaton.plugin.sdk.catalogue
-  org.openbaton.plugin.sdk.utils
-  org.openbaton.plugin.sdk.vim

The catalogue module contains classes that resemble their counterparts in the Java version of the catalogue e.g. a class for VIM instances, a class for NFVImages, etc.
The vim module contains the ```VimDriver``` class which should be extended by your specific VIM Driver class and which contains all the abstract methods that you have to implement for a working VIM Driver.
The utils module contains the logic for handling the VIM Driver's connection to the NFVO and the scheduling of tasks so that you do not have to handle these things at all. The most important function for you in this module is the ```start_vim_driver``` function.

In order to write your own VIM Driver you only have to implement the
abstract methods of the ``org.openbaton.plugin.sdk.vim.VimDriver`` class
and pass it to the ``org.openbaton.plugin.sdk.utils.start_vim_driver``
function. For an example have a look at the
`openstack-python-vim-driver`_ implementation.

The SDK requires a configuration file that has to be passed to the
``start_vim_driver`` function. This configuration file should be an INI
file with the following section:

.. code:: ini

   [rabbitmq]
   username = openbaton-manager-user
   password = openbaton
   broker_ip = 127.0.0.1
   port = 5672
   heartbeat = 1
   exchange-name = openbaton-exchange

These values are need for the SDK to connect to RabbitMQ and to
communicate with the NFVO.

Issue tracker
-------------

Issues and bug reports should be posted to the GitHub Issue Tracker of this project

What is Open Baton?
-------------------

OpenBaton is an open source project providing a comprehensive implementation of the ETSI Management and Orchestration (MANO) specification.

Open Baton is a ETSI NFV MANO compliant framework. Open Baton was part of the OpenSDNCore (www.opensdncore.org) project started almost three years ago by Fraunhofer FOKUS with the objective of providing a compliant implementation of the ETSI NFV specification.

Open Baton is easily extensible. It integrates with OpenStack, and provides a plugin mechanism for supporting additional VIM types. It supports Network Service management either using a generic VNFM or interoperating with VNF-specific VNFM. It uses different mechanisms (REST or PUB/SUB) for interoperating with the VNFMs. It integrates with additional components for the runtime management of a Network Service. For instance, it provides autoscaling and fault management based on monitoring information coming from the the monitoring system available at the NFVI level.

Source Code and documentation
-----------------------------

The Source Code of the other Open Baton projects can be found `here`_
and the documentation can be found
`here <http://openbaton.org/documentation>`__ .

News and Website
----------------

Check the `Open Baton Website`_ Follow us on Twitter @\ `openbaton`_.

Licensing and distribution
--------------------------

Copyright [2015-2016] Open Baton project

Licensed under the Apache License, Version 2.0 (the “License”);

you may not use this file except in compliance with the License. You may
obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
-------

The Open Baton project provides community support through the Open Baton
Public Mailing List and through StackOverflow using the tags openbaton.

Supported by
------------

.. _Open Baton: http://openbaton.org
.. _Apache v2 License: http://www.apache.org/licenses/LICENSE-2.0
.. _virtal environment: https://virtualenv.pypa.io/en/stable/
.. _openstack-python-vim-driver: https://github.com/openbaton/openstack-python-vim-driver
.. _here: http://github.org/openbaton
.. _Open Baton Website: http://openbaton.org
.. _openbaton: https://twitter.com/openbaton
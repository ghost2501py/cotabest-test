*************
CotaBest Test
*************

Test project for CotaBest job application

See online: <https://fast-lake-35340.herokuapp.com/api/v1/docs/>

Getting Started
===============

Prerequisites
-------------

* Python >= 3.6.0 <https://docs.python.org/3/index.html>
* Postgres >= 10.0 <https://www.postgresql.org/docs/>

Installing
----------

1. Create the database and the virtual environment. We recommend using
   `virtualenvwrapper <http://virtualenvwrapper.readthedocs.io/en/latest/index.html>`_.

2. Create an .env file and set variables. Examples can be found in :code:`.env.example`.

3. Setup the environment:

   .. code-block:: bash

      $ pip install -r requirements.txt
      $ python manage.py migrate

4. Load data:

   .. code-block:: bash

      $ python manage.py loaddata data.json

5. Start the server:

   .. code-block:: bash

      $ python manage.py runserver

The site will be available on <http://localhost:8000> or <http://127.0.0.1:8000>.

Deploy
======

TODO

API
===

API documentation can be found at <https://fast-lake-35340.herokuapp.com/api/v1/docs/> or <http://127.0.0.1:8000/api/v1/docs/>

Requirements
============

We use constraints for requirements.txt.

Add dependencies to requirements.txt:

   .. code-block:: text

      # requirements.txt
      -c constraints.txt
      Django
      anotherdependency

Then run:

   .. code-block:: bash

      $ pip install -r requirements.txt
      $ pip freeze > constraints.txt


Tests
=====

For postgres, the user must have permissions to create the database.
So in psql, you must do the following. See <https://stackoverflow.com/a/14186439>.

   .. code-block:: bash

      =# ALTER USER <yourdbuser> CREATEDB;

Basic commands
--------------

   .. code-block:: bash

      # Run tests
      $ python manage.py test

      # Update snapshots
      $ python manage.py test --snapshot-update

Coverage
--------

   .. code-block:: bash

      # Run coverage
      $ coverage run --source='.' manage.py test

      # Coverage report
      $ coverage report -m

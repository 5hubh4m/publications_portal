# Publications Portal

A web portal written in `Python3` with `Django` to store, retrieve and display the details of academic publications of the members of an institute.

## Features

These are described in the file `DBMS_requirements.pdf`

## Directory Structure

      publications_portal
      ├── accounts
      │   ├── __init__.py
      │   ├── apps.py
      │   ├── forms.py
      │   ├── managers.py
      │   ├── migrations
      │   │   ├── 0001_initial.py
      │   │   ├── 0002_auto_20161016_1628.py
      │   │   ├── 0003_auto_20161016_2039.py
      │   │   ├── 0004_auto_20161017_0204.py
      │   │   ├── 0005_auto_20161019_0903.py
      │   │   ├── 0006_auto_20161019_0906.py
      │   │   └── __init__.py
      │   ├── models.py
      │   ├── templates
      │   │   └── accounts
      │   │       ├── dashboard.html
      │   │       ├── email.html
      │   │       ├── email_subject.txt
      │   │       ├── login.html
      │   │       ├── password_reset.html
      │   │       ├── password_reset_complete.html
      │   │       ├── password_reset_confirm.html
      │   │       ├── password_reset_done.html
      │   │       ├── signup.html
      │   │       └── signup_successful.html
      │   ├── urls.py
      │   └── views.py
      ├── creator
      │   ├── __init__.py
      │   ├── apps.py
      │   ├── forms.py
      │   ├── migrations
      │   │   ├── __init__.py
      │   ├── templates
      │   │   └── creator
      │   │       ├── action_successful.html
      │   │       ├── add_field.html
      │   │       ├── add_form.html
      │   │       └── add_publication.html
      │   ├── urls.py
      │   └── views.py
      ├── DBMS_requirements.pdf
      ├── db_dump.sql
      ├── ERD.pdf
      ├── manage.py
      ├── portal
      │   ├── __init__.py
      │   ├── apps.py
      │   ├── forms.py
      │   ├── migrations
      │   ├── static
      │   │   └── portal
      │   │       ├── css
      │   │       │   └── style.css
      │   │       ├── images
      │   │       │   ├── google.png
      │   │       │   └── logo.png
      │   │       └── js
      │   ├── templates
      │   │   └── portal
      │   │       ├── 404.html
      │   │       ├── author.html
      │   │       ├── base.html
      │   │       ├── department.html
      │   │       ├── field.html
      │   │       ├── index.html
      │   │       ├── institute.html
      │   │       ├── publication.html
      │   │       ├── publication_list.html
      │   │       ├── publisher.html
      │   │       └── search.html
      │   ├── templatetags
      │   │   ├── __init__.py
      │   │   └── widget_type.py
      │   ├── urls.py
      │   └── views.py
      ├── pub_portal_schema_create.sql
      ├── publications_portal
      │    ├── __init__.py
      │    ├── settings.py
      │    ├── urls.py
      │    └── wsgi.py
      └── Schema.pdf
 
## Running the portal
 
The host computer must have `Django 1.10` and `python3` to run the portal. To simply run the portal for demonstration purposes, execute

> `python3 manage.py runserver`

In the `publications_portal` directory. This portal uses `MySQL` as it's database. The `SQL` script to setup the databse is given in `pub_portal_schema_create.sql` and the DB Dump is given in `db_dump.sql`.

To create the schema, run `mysql -uroot < pub_portal_schema_create.sql`.

To create DB from dump, run `mysql -uroot < db_dump.sql`.

The portal can be used with a production server such as `Apache` or `Nginx`.

## Django apps

The portal has been modularised into the following `Django apps`:
* `accounts`: For managing user accounts/profile creation and login features
* `creator`: For creating/adding new objects like Author, Publisher, Department, Institute, Publication, etc.
* `portal`: The main app, this is used to provide a view to all the auditing and browsing capabilities of the portal.

## UI/UX

The `UI`/`UX` of the portal is consistent and highly usable, with clean and clear visual cues and straightforward ways of performing tasks with complete and informative error messages which tell the user exactly what went wrong.

## Links

The important links in the portal are given below:
* `/`: Index
* `/login/`: Login
* `/signup/`: Signup
* `/dashboard/`: User dashboard
* `/add/*/`: Add an entity (Institute, Publication, etc.) to the portal
* `/*/id`: Display the detail of the entity (Institute, Publication, etc.) with the given `id`.

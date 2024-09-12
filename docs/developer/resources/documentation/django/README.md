# Django

## Description:

Django is a Python web framework that enables rapid development of secure and maintainable sites. It comes with read-to-use features like login system, database connection, Object Relational Mapping (ORM) to make it easier to work with databases, CRUD (Create Read Update Delete) operations and much more. This document will cover some helpful Django commands (runserver, makemigrations, etc.).


## Documentation:

For more details on the Django framework, please refer to the [official documentation](https://docs.djangoproject.com/en/5.0/).


## Commands:

* `runserver`: Used to spin up a Django server.

    * Example: `python manage.py runserver <host>:<port>`.

* `startapp`: Creates a new Django App.

    * Example: `python manage.py startapp <app_label>`.

* `makemigrations`: Creates migration files.       

    * Example:`python manage.py makemigrations`.
    * Note: You can create an empty migration for an app by running: `python manage.py makemigrations <app_label> --empty`. This is useful for creating a custom migration that, for example, may be used to populate a table with initial data.

* `migrate`: Applies migrations.

    * Example: `python manage.py migrate`.

* `squashmigrations`: Squashes the migration for a specified `app_label` up to and including the `migration_name`, if possible.

    * Example: `python manage.py squashmigrations <app_label> [start_migration_name] <migration_name>`. Note: `start_migration_name` is optional.

* `showmigrations`: Shows all migrations in the project.

    * Example: `python manage.py showmigrations`.
    * Note: This command's output shows all migrations grouped by `app_label` and will have an asterisk `*` enclosed in brackets `[]` for migrations that have been applied successfully.

* `dumpdata`: Outputs to STDOUT all data in the database associated with the named application(s). If no application name is provided, data for all installed applications will be dumped.

    * Example: `python manage.py dumpdata`.
    * Note: There is a conflict with `django_rq`, so when using this command be sure to use the `--exclude` option i.e.: `python manage.py dumpdata --exclude=django_rq`.

* `loaddata`: Searches for and loads the contents of a named `fixture` into the database.

    * Example: `python manage.py loaddata path/to/file/from/inside/the/api/container`


 
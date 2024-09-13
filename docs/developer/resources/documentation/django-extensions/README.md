# Django Extensions

## Description:

Django Extensions is a library that provides a collection of extensions for the Django framework. Some of these
extensions include admin extensions, model extensions and command extensions. This document focuses on covering
some useful command extensions and how to execute them in the terminal.

## Documentation:

For more details on the extensions provided by the library including examples, caveats, utilities, please
refer to the [official documentation](https://django-extensions.readthedocs.io/en/latest/).


## Command Extensions:

* `shell_plus`: Opens a Django shell with autoloading of the apps database models. Supports the following python
shells: IPython, bpython, ptpython and Python. You can set the configuration option `SHELL_PLUS` in the settings.py
file to explicitly specify the version you want. 

  * Note: If you wish to specify the shell you want to execute, you can do so by running: `docker compose exec api python manage.py shell_plus --{ipython|bpython|ptpython|plain}`.
  * Note: The default resolution order (if `SHELL_PLUS` has not been specified) is: `ptpython, bpython, ipython, python`.
  * Note: You can add command line arguments by using `--` example: `docker compose exec api python manage.py shell_plus --ipython -- --profile=test`. 
  * Note: IPython Notebook, which uses a web browser as its user interface, is also supported and can be executed by running:  `docker compose exec api python manage.py shell_plus --notebook`. The website will be hosted on: `http://{SERVER_HOST}:{NOTEBOOK_PORT}`. You will be asked to supply an API token to access the notebook, which appears in the container's STDOUT as the query param: token. Be sure to copy & paste the token's value into the notebook's password/token form field.

* `create_template_tags`: Creates a template tag directory structure within the specified application.

  * Example: `docker compose exec api python manage.py create_template_tags <app_name>`.

* `dumpscript`: Generates a Python script file that can be used to repopulate the database using objects.

  * Note: For this command, you need to provide the full path to file as shown here: `docker compose exec api python manage.py dumpscript <appname> > full/path/to/file`.

* `show_urls`: Displays the url routes that are defined in the project.

  * Example: `docker compose exec api python manage.py show_urls`.

* `runscript`: Lets you run a script within the Django context.

  * Note: This command uses a function named `run()` as the entry point for the script's execution.
  * Example: `docker compose exec api python manage.py <app_name.script_location.script_file>`. Note: When specifying the `script_file`, be sure not to include the `.py` extension.


* `export_emails`: Exports the email addresses for users stored in the User table.

    * Note: This command requires the following three setting keys to be defined in the `settings.py` file: `EXPORT_EMAILS_ORDER_BY`, `EXPORT_EMAILS_FIELDS` and `EXPORT_EMAILS_FULL_NAME_FUNC`. The only
    setting key not pre-defined in this codebase is `EXPORT_EMAILS_FULL_NAME_FUNC` which needs to have a Python function assigned to it. An example of one can be found here: https://github.com/django-extensions/django-extensions/blob/master/django_extensions/management/commands/export_emails.py#L23.
    * Example: `docker-compose exec api python manage.py export_emails > emails.txt`.

* `generate_password`: Generates a new password that may be used by a user.

    * Note: This command uses Django's core default password generator `make_random_password()`. Using the `--length` option allows you to specify the length of the password.
    * Example: `docker compose exec api python manage.py generate_password --length=<length>`.

* `graph_models`: Renders a graphical overview (Entity Relationship Diagram) of your project or specified apps.

    * Note: This command can generate either a GraphViz dot-file (.dot) or an image (.png). Be sure to view all options
    on the docs: https://django-extensions.readthedocs.io/en/latest/graph_models.html
    * Example: Creating a dot file: `docker compose exec api python manage.py graph_models -a > my_project.dot` 
    * Example: Creating a png file for the project with application grouping: `docker compose exec api python manage.py graph_models -a -g -o my_project_visualized.png`.

* `list_model_info`: List out all fields and methods for models in project apps.

    * Example: `docker compose exec api python manage.py list_model_info`.

* `managestate`: Saves `current` applied migrations to a file or applies migrations from a previous dump file.  
    
    * Example: Dumping current migrations: `docker compose exec api python manage.py dump master_backup`
    * Example: Rollback a database state using previous dump: `docker compose exec api python manage.py load master_backup`

* `print_settings`: Shows selected active Django settings or all if no arguments are passed.

    * Example: `docker compose exec api python manage.py print_settings`.

* `sqldiff`: Prints the `ALTER TABLE` statements for project apps.

    * Example: `docker compose exec api python manage.py sqldiff`.

* `sqldsn`: Prints the `Data Source Name` connection string for the databases.
    * Example: `docker compose exec api python manage.py sqldsn --all`.

* `validate_templates`: Checks template files for syntax and compile errors.

    * Note: This command does not catch invalid HTML errors, only errors in the Django template syntax used.
    * Note: There is a known issue where running this command returns back the error: `TemplateDoesNotExist` for a Jinja2 template. This
    is because the validate_templates command supports DjangoTemplates but not Jinja2Templates which are included in the `Templates` setting.
    This should not prevent you from writing Jinja2 templates, but be aware that running this command to validate them will return back that
    error.
    * Example: `docker compose exec api python manage.py validate_templates`.

* `admin_generator`: Generates the source code for Django Admin classes and outputs it to the container's STDOUT, by providing an app name. These classes are used to register an app's models with Django's admin site.
  
  * Example: `docker compose exec api python manage.py admin_generator <app_name>.`

* `clean_pyc`: Removes all the python bytecode compiled from the project.

  * Example: `docker compose exec api python manage.py clean_pyc`.

* `clear_cache`: Clears the Django cache.

  * Example: `docker compose exec api python manage.py clear_cache`.
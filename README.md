# myworkshop
A documentation generator for open hardware projects.

## Disclaimer
This project is at a very early stage of development: It can evolve dramatically at the next commits!

## Features
 * Generate beautiful documentation for open hardware projects!

## Getting started

### Requirements
 * python 3.6.9 or higher (package _python3_);
 * PostgreSQL 10.3 or higher;

### Install
Edit `myworkshop/settings/development.py` and complete your database settings in it.

Install all the required tools in a virtualenv:
```
$ make install
```

### Serve

#### Development environment
To run the application locally in a development environment:

```
$ make serve
```

#### Production environment
Create a new file named `production.py` in `myworkshop/settings` and write your production settings in it.

Edit `myworkshop/settings/__init__.py`:
```
from .production import *
```

## Tech/framework used

### Backend
* [Django 3.0](https://www.djangoproject.com/) : High-level Python Web framework.
* [Jinja2 2.11.1](https://jinja.palletsprojects.com/en/2.11.x/) : a modern and designer-friendly templating language for Python.
* [The “sites” framework](https://docs.djangoproject.com/en/2.2/ref/contrib/sites/) : Associating content with multiple sites
* [django-allauth 0.41.0](https://github.com/pennersr/django-allauth) : Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.
* [Modeltranslation 0.14.4](https://github.com/deschler/django-modeltranslation) : is used to translate dynamic content of existing Django models to an arbitrary number of languages without having to change the original model classes.
* [django-crispy-forms 1.9.0](https://github.com/django-crispy-forms/django-crispy-forms) : The best way to have DRY Django forms.
* [Django REST framework 3.11.0](https://github.com/encode/django-rest-framework) : A powerful and flexible toolkit for building Web APIs.

### Frontend
 * [Bootstrap 4.4.1](https://getbootstrap.com/) : A responsive web toolkit.
 * [Boostwatch 4.4.1](https://bootswatch.com/) : Free themes for Bootstrap.
 * [Font Awesome 5.12.1](https://fontawesome.com/) : Icon set and toolkit.
 * [jQuery 3.4.1](https://jquery.com/) : A feature-rich JavaScript library for dynamic web pages.

## Versioning
We use [SemVer](http://semver.org/) for versioning. See the [CHANGELOG.md](CHANGELOG.md) file for details.

## Technical details
To know more about the development guidelines of this project, see the [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) file.

## Contributing
If you'd like to contribute, please raise an issue or fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing
The code in this project is licensed under MIT license. See the [LICENSE](LICENSE) file for details.

## Contributors
 * **Julien Lebunetel** - [jlebunetel](https://github.com/jlebunetel)

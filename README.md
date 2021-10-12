# My Workshop
A documentation generator for open hardware projects.

**This project is currently unmaintained.**

## Features
 * Generate beautiful documentation for open hardware projects!

## Installation

### Requirements
- [Docker](https://docs.docker.com/get-docker/): we use _Docker_ to develop and run __My Workshop__. This is a strict requirement to use this project.
- [Docker Compose](https://docs.docker.com/compose/install/): we use _Docker Compose_ to simplify the orchestration of all __My Workshop__ application services, using configuration files for different environments (such as _dev_, _test_, _staging_ or _prod_).

Download this repository and unzip it on your computer. You should rename the folder `myworkshop-master` in `myworkshop`.

Or clone the repository directly on your computer:
```
$ git clone git@github.com:myworkshopproject/myworkshop.git
```

### Install and run a production environment
__My Workshop__ stores config in environment variables.
You must set these environment variables before running __My Workshop__, either directly or by providing the file `.env`.
To make things easier, we have prepared the `.env.example` template that you can adapt to your project.

Once the environment variables are set, you can build and start all the services of the __My Workshop__ application (via _Docker Compose_) using the following command:
``` bash
$ make prod
```

You can now access the application with your favorite internet browser at the address you set in the `$DOMAIN` environment variable.

When launching the application for the first time, you will need to create a super user to manage it.
You can do this using the following command:
``` bash
$ docker exec -it myworkshop_core_1 make createsuperuser
```

Finally, To stop all application services, use the following command:
``` bash
$ make stop
```

### Install and run a development environment
You can build and start a development environment (completely independent of the production one) with the following command:
``` bash
$ make dev
```

This previous command builds all the required services for development and starts them all except the _core_ web server and workers.

To start the _Django_ web server, please open a terminal in the container:
``` bash
$ docker exec -it myworkshop-dev_core_1 /bin/bash
```

Then run:
``` bash
$ make venv
$ make install
$ make migrate
$ make populate-db
$ make createsuperuser
$ make serve-dev
```

To start a _Celery_ worker, please run:
``` bash
$ docker exec -it myworkshop-dev_core_1 make worker
```

To start the frontend dev environment, please open a terminal in the container:
``` bash
$ docker exec -it myworkshop-dev_frontend_1 /bin/bash
```

Then run:
``` bash
$ npm install
$ npm run build
```

## Tech/framework used
- [NGINX](https://www.nginx.com/): a free and open-source web server used as a reverse proxy;
- [Django](https://www.djangoproject.com/): a Python-based free and open-source web framework;
- [PostgreSQL](https://www.postgresql.org/): a free and open-source relational database management system.

## Contributing
For the sake of simplicity, to ease interaction with the community, we use the [GitHub flow](https://guides.github.com/introduction/flow/index.html) for open-source projects. In a few words:
* The `master` branch is always stable and deployable;
* Tags from the `master` branch are considered as releases;
* Contributors have to fork or create a new feature-branch to work on (if they are allowed to in the original repository) and propose a pull request to merge their branch to `master`.

If you'd like to contribute, please raise an issue or fork the repository and use a feature branch. Pull requests are warmly welcome!

## Versioning
We use [SemVer](http://semver.org/) for versioning. See the [CHANGELOG.md](CHANGELOG.md) file for details.

## Licensing
The code in this project is licensed under MIT license. See the [LICENSE](LICENSE) file for details.

## Contributors
* **Julien Lebunetel** - [jlebunetel](https://github.com/jlebunetel).

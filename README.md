# chart_mysql

This is a web application based on flask-app builder. This application takes data from mysql and represent relevat chart in the browser

# Installation
## Install virtualenv
pip install virtualenv

### Create a virtualenv
virtualenv envs
### Activate virtualenv
$ . ./envs/bin/activate

## Install Flask-app builder
* (envs)$ pip install flask-appbuilder

* (envs)$ fabmanager create-app
* Your new app name: chart_maker
* Your engine type, SQLAlchemy or MongoEngine [SQLAlchemy]:
* Downloaded the skeleton app, good coding!
* (envs)$ cd chart_maker
* (envs)$ fabmanager create-admin
* Username [admin]:
* User first name [admin]:
* User last name [user]:
* Email [admin@fab.org]:
* Password:
* Repeat for confirmation:

## Run
(envs)chart_maker/app$ python views.py

# Reconcile

A web application to reconcile GSTR-2B and purchase register's B2B invoices. And then feed the
data to a google sheet via API.

## Development Setup

Python 3 and Linux recommended.

```bash
# Install pipenv globally.
$ pip install pipenv

# Create a virtual env.
$ pipenv --python 3

# Activate virtual env.
$ pipenv shell

# Install dependencies.
$ pipenv install --dev

# Run Django API server.
$ python manage.py runserver
```

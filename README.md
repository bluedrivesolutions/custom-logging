# Custom Logging
- [Introduction](#introduction)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)

## Introduction
Custom Logging is a simple library that logs changes to a model's fields. It is useful for tracking modifications to a model's fields and for logging authentication actions in a Django application.

## Installation
```bash
pip install git+https://github.com/bluedrivesolutions/custom-logging.git
```

## Setup
Add 'custom_logging.middleware.CustomLoggingMiddleware' to your MIDDLEWARE setting in settings.py file. This middleware gets the user whenever a model instance is saved.

```python
MIDDLEWARE = [
    ...
    'custom_logging.middleware.CustomLoggingMiddleware',
    ...
]
```

Add in LOGGING setting in settings.py file.

```python
LOGGING = {
    ...
    'loggers': {
        ...
        'custom_logging': {  
            'handlers': ['console'],
            'level': 'INFO',
        },
        ...
    },
    ...
}
```


## Usage
To log changes to a model's fields, you need to import ModelLogger and pass the model class and fields to log as arguments.
```python
# models.py
from custom_logging import ModelLogger

class DjangoModel:
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)

ModelLogger(model_class=DjangoModel, fields_to_log=['field1', 'field2'])

# Alternatively you can use __all__ to log all fields
ModelLogger(model_class=DjangoModel, fields_to_log='__all__')
```

To log authentication actions, you need to import the signals module to any of your apps.

```python
# apps.py

class MyAppConfig(AppConfig):
    name = 'my_app'

    def ready(self):
        from custom_logging import signals
```

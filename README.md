# Model Logger
- [Introduction](#introduction)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)

## Introduction
Model Logger is a simple library that logs changes to a model's fields. It is useful for tracking changes to a model's fields in a Django application.

## Installation
```bash
pip install git+ssh://git@github.com/bluedrivesolutions/model-logger.git
```

## Setup
Add 'model_logger.middleware.ModelLoggerMiddleware' to your MIDDLEWARE setting in settings.py file.

```python
MIDDLEWARE = [
    ...
    'model_logger.middleware.ModelLoggerMiddleware',
    ...
]
```

Add in LOGGING setting in settings.py file.

```python
LOGGING = {
    ...
    'loggers': {
        ...
        'model_logger': {  
            'handlers': ['console'],
            'level': 'INFO',
        },
        ...
    },
    ...
}
```


## Usage
```python
from model_logger import ModelLogger

class DjangoModel:
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)

ModelLogger(model_class=DjangoModel, fields_to_log=['field1', 'field2'])

# Alternatively you can use __all__ to log all fields
ModelLogger(model_class=DjangoModel, fields_to_log='__all__')
```
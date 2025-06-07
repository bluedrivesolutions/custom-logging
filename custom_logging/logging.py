import logging
import random
import string

from .middleware import get_current_user
from .utils import convert_string_to_numeric

logger = logging.getLogger(__name__)


class LoggingMixin:
    logging_fields = []

    def log_changes(self, old_instance):
        user = self.get_current_user()
        if user is None:
            return
        if user.pk is None:
            return

        object_name = self.__class__.__name__.capitalize()
        changes = []

        if isinstance(self.logging_fields, str):
            if self.logging_fields == "__all__":
                self.logging_fields = [field.name for field in self._meta.fields]
            else:
                raise ValueError(
                    "logging_fields must be a list of fields "
                    'to log or "__all__" to log all fields'
                )

        for field in self.logging_fields:
            old_value = getattr(old_instance, field)
            new_value = getattr(self, field)
            temp_old_value = convert_string_to_numeric(old_value)
            temp_new_value = convert_string_to_numeric(new_value)

            if temp_old_value == temp_new_value:
                continue
            if not temp_old_value and not temp_new_value:
                continue

            changes.append((field, old_value, new_value))

        if changes:
            for field, old_value, new_value in changes:
                logger.info(
                    f"{object_name} {self.pk} - {field} changed "
                    f"from `{old_value}` to `{new_value}` by {user}"
                )

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                self.log_changes(old_instance)
            except self.__class__.DoesNotExist:
                pass
        save_method = getattr(self, self.original_save_method_name)
        save_method(*args, **kwargs)

    def get_current_user(self):
        return get_current_user()


class ModelLogger:
    def __init__(self, model_class, fields_to_log=None):
        self.model_class = model_class
        self.fields_to_log = fields_to_log

        original_init = model_class.__init__

        original_save_method = model_class.save
        original_save_method_name = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        setattr(model_class, original_save_method_name, original_save_method)

        def __init__(self, *args, **kwargs):
            self.logging_fields = fields_to_log
            original_init(self, *args, **kwargs)

        if hasattr(model_class, "get_current_user"):
            logger.warning(
                f"get_current_user method is already defined in {model_class.__name__}"
            )

        if hasattr(model_class, "log_changes"):
            logger.warning(
                f"log_changes method is already defined in {model_class.__name__}"
            )

        if hasattr(model_class, "original_save_method_name"):
            logger.warning(
                f"original_save_method_name method is already defined in {model_class.__name__}"
            )
            raise ValueError(
                f"original_save_method_name method is already defined in {model_class.__name__}"
            )

        model_class.__init__ = __init__
        model_class.original_save_method_name = original_save_method_name
        model_class.save = LoggingMixin.save
        model_class.log_changes = LoggingMixin.log_changes
        model_class.get_current_user = LoggingMixin.get_current_user

# Ravestate property classes

from threading import Lock
import logging

class PropertyBase:
    """
    Base class for context properties. Controls read/write/push/pop/delete permissions,
    property name basic impls. for the property value, parent/child mechanism.
    """

    def __init__(
            self, *,
            name="",
            allow_read=True,
            allow_write=True,
            allow_push=True,
            allow_pop=True,
            allow_delete=True,
            default=None):

        self.name = name
        self.allow_read = allow_read
        self.allow_write = allow_write
        self.allow_push = allow_push
        self.allow_pop = allow_pop
        self.allow_delete = allow_delete
        self.value = default
        self._lock = Lock()
        self.module_name = ""

    def fullname(self):
        return f"{self.module_name}:{self.name}"

    def lock(self):
        self._lock.acquire()

    def unlock(self):
        self._lock.release()

    def read(self):
        """
        Read the current property value.
        """
        if not self.allow_read:
            logging.error(f"Unauthorized read access in property {self.name}!")
            return None
        return self.value

    def write(self, value):
        """
        Write a new value to the property.
        :param value: The new value.
        :return: True if the value has changed and :changed should be signaled, false otherwise.
        """
        if not self.allow_write:
            logging.error(f"Unauthorized write access in property {self.name}!")
            return False
        if self.value != value:
            self.value = value
            return True
        else:
            return False


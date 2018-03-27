from abc import ABCMeta, abstractmethod
from dbwrapper.base import Status 

class BasePlugin:
    __metaclass__ = ABCMeta

    status_list = [Status.UP, Status.DOWN]

    def __init__(self, service_id):
        self.service_id = service_id

    @abstractmethod
    def run(self):
        pass

from abc import ABCMeta, abstractmethod

class Status:
    UP = 'up'
    DOWN = 'down'    

class BaseDBWrapper:
    __metaclass__ = ABCMeta

    status_list = [Status.UP, Status.DOWN]

    @abstractmethod
    def get_service_status(self, service_id):
        pass

    @abstractmethod
    def set_service_status(self, service_id, status):
        pass





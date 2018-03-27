import time
from threading import Timer
from .exceptions import InvalidPlugin
from .plugin.base import BasePlugin
from dbwrapper.base import Status


class WatchDog:
    def __init__(self, services, dbwrapper):
        for service in services:
            if not isinstance(service, BasePlugin):
                raise InvalidPlugin
        self.services = services
        self.dbwrapper = dbwrapper

    def run(self):
        for service in self.services:
            last_status = self.dbwrapper.get_service_status(
                service.service_id,
            )
            status = service.run()
            print '#%s# #%s#'%(last_status, status)

            if last_status == status:
                print "signalll"
                pass # todo: send watch dog signal
            else:
                self.dbwrapper.set_service_status(
                    service.service_id,
                    status,
                )

    def start(self):
        while True:
            self.run()
            time.sleep(10)

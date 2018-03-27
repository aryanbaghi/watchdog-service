import os
from datetime import datetime
from .base import BaseDBWrapper, Status
from .exceptions import InvalidStatus


class FileWrapper(BaseDBWrapper):
    def __init__(self, path):
        self.path = path

    def get_service_status(self, service_id):
        for line in self._reverse_readline():
            _service_id, time_string, status = line.split('#')[1:]
            _service_id = _service_id.split(':')[1].strip()
            time_string = time_string.split(':')[1].strip()
            status = status.split(':')[1].strip()
            _service_id = service_id.strip().replace('\\n', '\n').replace('\@', '#')
            time_string = time_string.strip()
            status = status.strip()
            if service_id == _service_id:
                return status
        return Status.UP

    def set_service_status(self, service_id, status):
        if status not in self.status_list:
            raise InvalidStatus
        with open(self.path, 'a+') as db:
            db.write(
                '#service_id: %(service_id)s #time: %(time)s #status: %(status)s\n'%{
                    'service_id': str(service_id).replace('\n', '\\n').replace('#', '\@'),
                    'time': datetime.utcnow(),
                    'status': status
                }
            )

    def _reverse_readline(self, buf_size=8192):
        """a generator that returns the lines of a file in reverse order"""
        with open(self.path, 'r+') as fh:
            segment = None
            offset = 0
            fh.seek(0, os.SEEK_END)
            file_size = remaining_size = fh.tell()
            while remaining_size > 0:
                offset = min(file_size, offset + buf_size)
                fh.seek(file_size - offset)
                buffer = fh.read(min(remaining_size, buf_size))
                remaining_size -= buf_size
                lines = buffer.split('\n')
                # the first line of the buffer is probably not a complete line so
                # we'll save it and append it to the last line of the next buffer
                # we read
                if segment is not None:
                    # if the previous chunk starts right from the beginning of line
                    # do not concact the segment to the last line of new chunk
                    # instead, yield the segment first 
                    if buffer[-1] is not '\n':
                        lines[-1] += segment
                    else:
                        yield segment
                segment = lines[0]
                for index in range(len(lines) - 1, 0, -1):
                    if len(lines[index]):
                        yield lines[index]
            # Don't yield None if the file was empty
            if segment is not None:
                yield segment
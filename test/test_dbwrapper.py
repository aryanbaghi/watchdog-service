import os
import unittest
from dbwrapper import FileWrapper, Status


class TestFileWrapper(unittest.TestCase):
    PATH = 'test.db'
    SERVICE_ID = '#test_service\n'

    def setUp(self):
        self.filewrapper = FileWrapper(self.PATH)

    def tearDown(self):
        self.filewrapper = None
        # os.remove(self.PATH)

    def test_status(self):
        self.assertEqual(
            self.filewrapper.get_service_status(self.SERVICE_ID),
            Status.UP
        )
        self.filewrapper.set_service_status(self.SERVICE_ID, Status.DOWN)
        self.assertEqual(
            self.filewrapper.get_service_status(self.SERVICE_ID),
            Status.DOWN
        )

if __name__ == '__main__':
    unittest.main()
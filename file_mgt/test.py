"""Test Cases for Each of the Executing Commands"""
import unittest
from random import sample
from os import listdir
from string import ascii_lowercase
from executor import Executor
from settings import AUTHENTICATION_SUCCESSFUL, USER_DIR

EXECUTOR = Executor()
USER = ''
PASSWD = ''

class TestExecutor(unittest.TestCase):
    """Executor Tester"""
    def test_step1_object_creation(self):
        """Not a test, instead basic initialisaton"""
        global USER
        global PASSWD
        USER = ''.join(sample(ascii_lowercase, 10))
        PASSWD = ''.join(sample(ascii_lowercase, 10))
        while USER in listdir(USER_DIR):
            USER = ''.join(sample(ascii_lowercase, 10))


    def test_step2_register(self):
        """Registration test. Test for Directory Creation"""
        output = EXECUTOR.register('register', USER, PASSWD)

        self.assertEqual(AUTHENTICATION_SUCCESSFUL, output)
        self.assertTrue((USER_DIR / USER).is_dir())

    def test_step3_write_and_read_file(self):
        """Writing and Reading Test on a file"""
        file_name = ''.join(sample(ascii_lowercase, 5))
        content = ''.join(sample(ascii_lowercase, 20))
        EXECUTOR.write_file('write_file', file_name, content)
        content_in_file = (USER_DIR / USER / file_name).read_text()

        self.assertEqual(content_in_file, EXECUTOR.read_file('read_file', file_name))

    def test_step4_create_folder(self):
        """Folder Creation Test"""
        folder_name = ''.join(sample(ascii_lowercase, 4))
        EXECUTOR.create_folder('create_folder', folder_name)
        self.assertTrue((USER_DIR/USER/folder_name).is_dir())

    def test_step5_list(self):
        """Listing Contents Test"""
        output = EXECUTOR.ls('ls')
        actual_output = [x.name for x in (USER_DIR / USER).iterdir()]
        self.assertEqual(output, '\n'.join(actual_output))

if __name__ == '__main__':
    unittest.main()

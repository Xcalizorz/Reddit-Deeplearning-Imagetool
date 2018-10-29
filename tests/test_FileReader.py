# -*- coding: utf-8 -*-
import os
import unittest

from FileReader import FileReader


class TestFileReader(unittest.TestCase):
    """
    Unit-testing the FileReader
    """
    def test_read_file_FileNotFoundError(self):
        """
        Testing if FileNotFoundError is raised and handled correctly
        :return:
        """
        self.assertRaises(
            FileNotFoundError,
            FileReader.read_file("Wrongfile.xosda")
        )

    def test_read_file_ValueError(self):
        """
        Testing if ValueError is raised and handled correctly
        Trying to read with a wrong mode
        :return:
        """
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "make.bat"
        )
        self.assertRaises(
            ValueError,
            FileReader.read_file(file_path, "ysa")
        )


if __name__ == '__main__':
    unittest.main()

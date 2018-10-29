# -*- coding: utf-8 -*-
import unittest

from FileWriter import FileWriter


class TestFileWriter(unittest.TestCase):
    """
    Unit-testing the FileWriter
    """
    def test_write_file_FileNotFoundError(self):
        """
        Testing if FileNotFoundError is raised and handled correctly
        """
        self.assertRaises(
            FileNotFoundError,
            FileWriter.write_tex_file("SomeFile.txt", "a")
        )

    def test_read_file_ValueError(self):
        """
        Testing if ValueError is raised and handled correctly
        Trying to write with a wrong mode
        :return:
        """
        self.assertRaises(
            ValueError,
            FileWriter.write_tex_file("SomeFile.txt", "ysa")
        )


if __name__ == '__main__':
    unittest.main()

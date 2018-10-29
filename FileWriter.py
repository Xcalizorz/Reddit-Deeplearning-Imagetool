# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class FileWriter(ABC):
    """
        Abstract class which allows to read files using the read_file function

        Allowes to read, write, append or create files using its read_file() function
        """

    @staticmethod
    @abstractmethod
    def write_tex_file(file_paths, input_string, mode: str = "w+"):
        """
        Writes the given string to any given file.

        Examples:
        1)
            file_paths: A list of N files
            input_string: "A normal string."

            ->  Writes "A normal string." to all files in the list

        2)
            file_paths: A list of N files
            input_string: A list of N strings

            ->  Writes each string to each file_path, in input order

        3)
            file_paths: 1 file
            input_string: A list of N strings

            ->  Writes each string to that file_path, in input order
                A higher permission level (append) will be given

        4)
            file_paths: 1 file
            input_string: 1 string

            ->  Writes the string to that file_path.

        :param file_paths:
            Path to files, can be 1 or a list of many
            The list needs to be iterable.

            The extension must be provided in the file path
        :param input_string:
            String to be written to the file
        :type input_string:
            str
        :param mode:
            All modes available to pythons 'open()'-method
        :type mode:
            str, default is 'w+'
        :return:
            List of contents read from the csv files
        """
        if isinstance(file_paths, (list, tuple)):
            if isinstance(input_string, (list, tuple)):
                # n to n
                return FileWriter._write_tex_n_n(file_paths, input_string, mode)
            # n file-paths, 1 string
            return FileWriter._write_tex_n_1(file_paths, input_string, mode)

        if isinstance(input_string, (list, tuple)):
            # 1 file-path, n strings
            return FileWriter._write_tex_1_n(file_paths, input_string, mode)

        # 1 to 1
        return FileWriter._write_tex_1_1(file_paths, input_string, mode)

    @staticmethod
    def _write_tex_1_1(file_paths, input_string, mode):
        """
        1 file paths and 1 input strings
        :param file_paths:
        :param input_string:
        :param mode:
        :return:
        """
        return FileWriter._write_tex(file_paths, input_string, mode)

    @staticmethod
    def _write_tex_1_n(file_paths, input_strings, mode):
        """
        1 file paths and n input strings
        :param file_paths:
        :param input_strings:
        :param mode:
        :return:
        """
        return [FileWriter._write_tex(file_paths, input_string, mode) for input_string in input_strings]

    @staticmethod
    def _write_tex_n_1(file_paths, input_string, mode):
        """
        N file paths and 1 input strings
        :param file_paths:
        :param input_string:
        :param mode:
        :return:
        """
        return [FileWriter._write_tex(file_path, input_string, mode) for file_path in file_paths]

    @staticmethod
    def _write_tex_n_n(file_paths, input_strings, mode):
        """
        n file paths and n input strings
        :param file_paths:
        :param input_strings:
        :param mode:
        :return:
        """
        return [FileWriter._write_tex(file_path, input_string, mode)
                for file_path, input_string in zip(file_paths, input_strings)]

    @staticmethod
    def _write_tex(file_path, input_string: str, mode: str):
        """
        Internal function; writes string to any given file
        :param file_path:
            Path to your file
        :param input_string:
            String to be written to the file
        :type input_string:
            str
        :param mode:
            All modes available to pythons 'open()'-method
        :type mode:
            str, default is 'w+'
        :return:
            Returns the information from the .csv file as a pandas dataframe
            Returns None, if the .csv file is non existent
        """
        try:
            with open(file_path, mode) as f:
                f.write(input_string)
        except FileNotFoundError:
            print("Could not find the file!")
            return None
        except IOError:
            print("Could not read the file: {}".format(file_path))

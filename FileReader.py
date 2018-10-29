# -*- coding: utf-8 -*-
import os
from abc import ABC, abstractmethod
from xml.dom import minidom


class FileReader(ABC):
    """
    Abstract class which allows to read files using the read_file function

    Use the read_file function to read files.
    """

    @staticmethod
    @abstractmethod
    def read_file(path_to_file, mode: str = 'r'):
        """
        Reads a file and returns its content as a string
        :param path_to_file:
            The path to the file to be read
        :param mode:
            Level of permission to use
            r:  read
            w:  write
            a:  append
            r+: read & write
            w+: read & write, create if non existent
            a+: append, create if non existent
        :return:
            Content of file as string
        """
        try:
            with open(path_to_file, mode) as f:
                return FileReader._read_file_try_catch_helper(f)
        except FileNotFoundError:
            print("Could not find a file at {}".format(path_to_file))
        except ValueError:
            print("Only specific values for mode are allowed.\n"
                  "Check the doc for further information.")
        except IOError:
            print("Could not read the file: {}".format(path_to_file))

    @staticmethod
    def _read_file_try_catch_helper(file):
        """
        Allows to observe rules regarding indentation levels
        in the read_file method
        :param file:
            Opened file object to be read
        :return:
            Contents of the file
        """
        try:
            return file.read()
        except FileNotFoundError:
            print("The file was deleted by another process during the creation.")
            return None

    @staticmethod
    @abstractmethod
    def read_xml_files(xml_file_paths):
        """
        Checking csv_file_paths and reading the csv files
        The csv file paths will be read in input order

        WARNING: The xml.dom.minidom module is not secure against maliciously constructed data.
        If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
            https://docs.python.org/3.7/library/xml.html#xml-vulnerabilities

        :param xml_file_paths:
            Path to xml-files, can be 1 or a list of many.
            Can be a directory as well
        :return:
            List of contents read from the csv files
        """
        if os.path.isdir(xml_file_paths):
            xml_file_paths = [os.path.join(xml_file_paths, xml_file_path)
                              for xml_file_path in os.listdir(xml_file_paths)
                              if xml_file_path.endswith('.xml')]

        return [FileReader._read_xml(xml_file_path) for xml_file_path in xml_file_paths
                if xml_file_path.endswith('.xml')]

    @staticmethod
    def _read_xml(xml_file_path):
        """
        Internal function; reads xml files
        :param xml_file_path:
            Path to .xml file
        :return:
            Returns the information from the .csv file as a pandas dataframe
            Returns None, if the .xml file is non existent or unreadable
        """
        try:
            return minidom.parse(xml_file_path)
        except FileNotFoundError:
            print("Could not find the .xml-file!")
            return None
        except IOError:
            print("Could not read the file: {}".format(xml_file_path))
            return None

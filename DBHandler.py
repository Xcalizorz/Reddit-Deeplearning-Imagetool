"""An abstract class, combining different DB handlers
Combines different DB types and can be used by other tools.

For now, the following DB types are available:
    - SQLite3
"""
import sqlite3


class DBHandler():

    def __init__(self):
        self.db_types = {
            'sqlite3': sqlite3.connect('db.sqlite3'),
        }

    @property
    def connection(self, db_type):
        """Create a connection to a given database type
        The database type given is not case sensitive

        :param db_type:
            database type:
            E.g.: ('sqlite3')
        :type db_type: str
        :return: Database connection object
        :raises sqlite3.Error:
            Raises exception if it cant connect to the SQLite3 database
        """

        try:
            return self.db_types[db_type.lower()]
        except sqlite3.Error as error:
            raise f"An SQLite3 Error occured: {error}"

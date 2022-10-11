import mysql.connector
import mysql
import traceback

from api.utils.logger.logger import Logger

from api.utils.config.config import Config

config = Config()
logger = Logger()


class Interface:
    def __init__(self):
        self.host_name = config.db_server
        self.host_port = config.db_port
        self.user_name = config.db_user
        self.user_password = config.db_password
        self.database_name = config.db_table
        self.connection = None
        self.cursor = None
        self.__create_connection__()

    def __create_connection__(self):
        """
        Establishes the connection between the database and the api_old
        :return:
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                port=self.host_port,
                user=self.user_name,
                passwd=self.user_password,
                database=self.database_name
            )
        except mysql.connector.errors.Error:
            logger.error(f"An error has occurred while connecting to the database!")
            traceback.print_exc()

        return self.connection

    def execute(self, query, variables=None):
        """
        Executes a query
        :param query: The query to execute
        :param variables: The variables to prevent sql injection
        :return: The result of the query. Returns an empty list if there is no return value (for example in an 'insert into' query)
        """

        if variables is None:
            variables = {}
        self.cursor = self.connection.cursor()
        self.cursor.execute(query, variables)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def close(self):
        """
        Commits the actions taken and closes the connection
        :return:
        """
        self.connection.commit()
        self.connection.close()

import psycopg2


class Database:
    def create(self):
        self.__connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
        )

        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor()

        sql = """
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE SCHEMA IF NOT EXISTS vector_db;

        CREATE TABLE IF NOT EXISTS vector_db.articles (
            id bigserial PRIMARY KEY,
            filename VARCHAR(50),
            embedding vector(100)
        );
        """

        self.__cursor.execute(sql)
        self.__connection.commit()
        self.__cursor.close()
        self.__connection.close()

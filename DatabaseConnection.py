from pgvector.psycopg2 import register_vector
import psycopg2
import numpy as np


class DatabaseConnection:
    def __init__(self) -> None:
        self.__connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
        )
        register_vector(self.__connection)
        self.__cursor = self.__connection.cursor()

    def insert_embedding(self, filename: str, embedding: np.ndarray):
        self.__cursor.execute(f"INSERT INTO vector_db.articles (filename, embedding) VALUES ('{filename}', %s)", (embedding,))
        self.__connection.commit()
        return self
    
    def get_similar_article(self, embedding: np.ndarray):
        self.__cursor.execute(f"SELECT * FROM vector_db.articles ORDER BY embedding <=> %s LIMIT 5;", (embedding,))
        result = self.__cursor.fetchall()
        return result
        
    def finalize(self):
        self.__cursor.close()
        self.__connection.close()

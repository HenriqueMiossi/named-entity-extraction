from Article import Article
from ArticleCollection import ArticleCollection
from Database import Database
from DatabaseConnection import DatabaseConnection

def store_collection():
    ac = ArticleCollection()
    ac.get_articles_from_path("./dataset")

def get_similar():
    dbc = DatabaseConnection()
    ac = ArticleCollection()
    
    ac.get_articles_from_path("./dataset-test")
    dbc.get_similar_article(ac.items[0].article_embedding)

    dbc.finalize()

if __name__ == "__main__":
    Database().create()
    # store_collection()
    get_similar()
    
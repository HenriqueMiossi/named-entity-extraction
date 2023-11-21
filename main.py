from ArticleCollection import ArticleCollection
from DatabaseConnection import DatabaseConnection
from Database import Database


if __name__ == "__main__":
    Database().create()

    ac = ArticleCollection()
    ac.get_articles_from_path("./dataset")

    dbc = DatabaseConnection()
    
    # for article in ac.items:
    #     dbc.insert_embedding(article.filename, article.article_embedding)

    print(dbc.get_similar_article(ac.items[0].article_embedding))
    
    dbc.finalize()

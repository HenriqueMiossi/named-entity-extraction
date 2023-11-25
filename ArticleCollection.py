from os import listdir
from os.path import isfile, join

from Article import Article
from DatabaseConnection import DatabaseConnection
from Method import Method


class ArticleCollection:
    def get_articles_from_path(self, path: str):
        file_paths_from_directory = [
            join(path, f) for f in listdir(path) if isfile(join(path, f))
        ]
        self.items = []
        for article in file_paths_from_directory:
            try:
                print(f"Processing {article}")
                dbc = DatabaseConnection()
                new_article = (
                    Article(article)
                    .apply_ner()
                    .get_dbpedia_uris(method=Method.RDF2VEC)
                    .get_uri_embeddings()
                    .get_article_embedding()
                )

                self.items.append(new_article)
                # dbc.insert_embedding(new_article.filename, new_article.article_embedding)
                # print(f"{article} was saved to the db")
                dbc.finalize()
            except Exception as e:
                print(f"Error with article {article}: {e}")

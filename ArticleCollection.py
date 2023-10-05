from os import listdir
from os.path import isfile, join

from Article import Article
from Method import Method


class ArticleCollection:
    def get_articles_from_path(self, path: str):
        file_paths_from_directory = [
            join(path, f) for f in listdir(path) if isfile(join(path, f))
        ]
        self.items = [
            Article(article).apply_ner().get_dbpedia_uri(method=Method.RDF2VEC)
            for article in file_paths_from_directory
        ]
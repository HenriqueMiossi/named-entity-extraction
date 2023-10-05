from typing_extensions import Self
from contextlib import closing
from multiprocessing import Pool
import spacy
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF

from DbpediaInterface import DbpediaInterface
from EntityType import EntityType
from Method import Method
from RDF2Vec import RDF2Vec


class Article:
    __nlp = spacy.load("pt_core_news_lg")

    def __init__(self, path: str) -> None:
        with open(file=path, mode="r", encoding="windows-1252") as file:
            self.content = file.read()

    def apply_ner(self) -> Self:
        self.entities = self.__nlp(self.content).ents
        return self

    def get_dbpedia_uri(self, method: Method) -> Self:
        dbpedia = DbpediaInterface()

        # if method == Method.WORD2VEC:
        #     self.content

        if method == Method.RDF2VEC:
            uri_list = []

            for entity in self.entities:
                entity_type = EntityType[entity.label_]
                uris = dbpedia.get_possible_dbpedia_uris(entity.text, entity_type)

                # Disambiguate uris
                if uris == None or len(uris) == 0:
                    continue
                elif len(uris) == 1:
                    uri = uris[0]
                else:
                    # Disambiguate uris
                    doc = self.__nlp(self.content)
                    candidates_similarity = [
                        self.__calculate_similarity(doc, candidate)
                        for candidate in uris
                    ]
                    uri_list.append(
                        max(candidates_similarity, key=lambda d: d["similarity"])
                    )

            # Create embedding list from uri_list with pyRDF2Vec
            # Create single embedding for the article with an embedding aggregation technique
            uri_string_list = [
                item["uri"][list(item["uri"].keys())[0]]["value"]
                for item in uri_list
            ]

            embedder = RDF2Vec()
            embeddings = embedder.get_embeddings(uri_string_list)

    def __calculate_similarity(
        self, original_document: spacy.tokens.Doc, uri: dict
    ) -> tuple[str, float]:
        abstract_doc = self.__nlp(uri["abstract"]["value"])
        return {"uri": uri, "similarity": original_document.similarity(abstract_doc)}

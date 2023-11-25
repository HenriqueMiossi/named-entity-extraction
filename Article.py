from typing_extensions import Self
import spacy
import numpy as np

from DbpediaInterface import DbpediaInterface
from EntityType import EntityType
from Method import Method
from RDF2Vec import RDF2Vec


class Article:
    __nlp = spacy.load("pt_core_news_lg")

    def __init__(self, path: str) -> None:
        with open(file=path, mode="r", encoding="windows-1252") as file:
            self.filename = file.name
            self.content = file.read()

    def apply_ner(self) -> Self:
        self.entities = self.__nlp(self.content).ents
        return self

    def get_dbpedia_uris(self, method: Method) -> Self:
        dbpedia = DbpediaInterface()

        if method == Method.RDF2VEC:
            self.__uri_list = []

            for entity in self.entities:
                entity_type = EntityType[entity.label_]
                if (entity_type.name == 'MISC'):
                    continue

                uris = dbpedia.get_possible_dbpedia_uris(entity.text, entity_type)

                if uris == None or len(uris) == 0:
                    continue
                elif len(uris) == 1:
                    doc = self.__nlp(self.content)
                    item = self.__calculate_similarity(doc, uris[0])
                    self.__uri_list.append(item)
                else:
                    # Disambiguate URIs
                    doc = self.__nlp(self.content)
                    candidates_similarity = [
                        self.__calculate_similarity(doc, candidate)
                        for candidate in uris
                    ]
                    self.__uri_list.append(
                        max(candidates_similarity, key=lambda d: d["similarity"])
                    )
        return self

    def get_uri_embeddings(self) -> Self:
        # Create embedding list from uri_list with pyRDF2Vec
        if (len(self.__uri_list) == 0):
            raise Exception('No URIs were found at DBpedia')
        
        for item in self.__uri_list:
            uri_string_list = [item["uri"][list(item["uri"].keys())[0]]["value"]]

        embedder = RDF2Vec()
        self.embeddings = embedder.get_embeddings(uri_string_list)
        return self

    def get_article_embedding(self) -> Self:
        # If there are no entities, return a vector of zeros as article embedding
        if len(self.embeddings) == 0:
            self.article_embedding = np.zeros(self.embeddings.shape[1])
            return self

        # Aggregate the embeddings of article entities by calculating the average
        aggregated_embedding = np.mean(self.embeddings, axis=0)

        # Store the aggregate article embedding
        self.article_embedding = aggregated_embedding

        return self

    def __calculate_similarity(
        self, original_document: spacy.tokens.Doc, uri: dict
    ) -> tuple[str, float]:
        abstract_doc = self.__nlp(uri["abstract"]["value"])
        return {"uri": uri, "similarity": original_document.similarity(abstract_doc)}

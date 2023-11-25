from pyrdf2vec import RDF2VecTransformer
from pyrdf2vec.graphs import KG
from pyrdf2vec.walkers import RandomWalker
from pyrdf2vec.embedders import Word2Vec
import numpy as np


class RDF2Vec:
    def __init__(self) -> None:
        self.kg = KG(
            "https://dbpedia.org/sparql",
            skip_predicates={"www.w3.org/1999/02/22-rdf-syntax-ns#type"},
            literals=[
                [
                    "http://dbpedia.org/ontology/wikiPageWikiLink",
                    "http://www.w3.org/2004/02/skos/core#prefLabel",
                ],
            ],
        )

    def get_embeddings(self, uris: list[str]) -> np.ndarray:
        if len(uris) == 0: return np.zeros(100)

        uris = list(set(uris))

        transformer = RDF2VecTransformer(
            Word2Vec(epochs=10),
            walkers=[RandomWalker(4, 10, with_reverse=False, n_jobs=4)],
            verbose=1,
        )

        try:
            embeddings, _ = transformer.fit_transform(self.kg, uris)
        except Exception as e:
            print(f'Error: {e}')
            raise e

        return np.array(embeddings)

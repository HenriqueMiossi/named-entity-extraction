from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE

from EntityType import EntityType
from Method import Method


class DbpediaInterface:
    wrapper = SPARQLWrapper("https://dbpedia.org/sparql")

    def __init__(self) -> None:
        self.wrapper.setReturnFormat(JSON)

    def get_possible_dbpedia_uris(self, entity: str, type: EntityType):
        try:
            if type == EntityType.PER:
                self.wrapper.setQuery(
                    f"""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?person ?abstract
                    WHERE {{
                        ?person rdf:type dbo:Person .
                        ?person rdfs:label ?label .
                        ?person dbo:abstract ?abstract .

                        FILTER (str(?label) = "{entity}")
                        FILTER langMatches(lang(?abstract),'en')
                    }}
                    """
                )
            elif type == EntityType.LOC:
                self.wrapper.setQuery(
                    f"""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?place ?abstract
                    WHERE {{
                        ?place rdf:type dbo:Place .
                        ?place rdfs:label ?label .
                        ?place dbo:abstract ?abstract .

                        FILTER (str(?label) = "{entity}")
                        FILTER langMatches(lang(?abstract), "en")
                    }}
                    """
                )
            elif type == EntityType.ORG:
                self.wrapper.setQuery(
                    f"""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                    SELECT DISTINCT ?organization ?abstract
                    WHERE {{
                        ?organization rdf:type ?range .
                        ?organization rdfs:label ?label .
                        ?organization dbo:abstract ?abstract .

                        FILTER (str(?label) = "{entity}")
                        FILTER langMatches(lang(?abstract),'en')
                        FILTER (?range = dbo:Organization || ?range = dbo:Company || ?range = dbo:Group || ?range = dbo:Institution)
                    }}
                    """
                )
            else:
                pass

            return self.wrapper.query().convert()["results"]["bindings"]
        except Exception as e:
            print(f'Error with entity: {repr(entity)}')

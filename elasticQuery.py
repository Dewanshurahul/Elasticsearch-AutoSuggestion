try:
    from flask import app,Flask
    from flask_restful import Resource, Api, reqparse
    from elasticsearch import Elasticsearch
except Exception as e:
    print("Modules Missing {}".format(e))

# Flask App
app = Flask(__name__)
# API the main entry point of the Application
# should be initialized with a flask application
api = Api(app)

# index name Elasticsearch
name = 'a'

# Getting Elasticsearch Connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


class ElasticSearch(Resource):

    # To auto_query for every input (Use of Constructor)
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.main_query ={
            "_source": [],
            "size": 0,
            "min_score": 0.5,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "title": {
                                    "query": "{}".format(self.query)
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

    def get(self):
        res = es.search(index=name, size=0, body=self.main_query)
        return res

parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True)

api.add_resource(ElasticSearch, '/autocomplete')

# Run the App
if __name__ == '__main__':
    app.run(debug=True, port=4000)

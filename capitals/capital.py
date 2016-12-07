from datetime import datetime
from google.cloud import datastore
import utility


class Capital:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "Capitals"

    def to_dto(self, capital):
        json_capital = {}
        json_capital['id'] = capital.key.id
        json_capital['name'] = capital['name']
        json_capital['countryCode'] = capital['countryCode']
        json_capital['country'] = capital['country']
        json_capital['location'] = {}
        json_capital['location']['latitude'] = capital['latitude']
        json_capital['location']['longitude'] = capital['longitude']
        json_capital['continent'] = capital['continent']
        return json_capital

    def store(self, capital):

        print capital
        key = self.ds.key(self.kind, capital['id'])

        print key
        entity = datastore.Entity(key)
 
        entity['name'] = capital['name']
        entity['countryCode'] = capital['countryCode']
        entity['country'] = capital['country']
        entity['latitude'] = capital['location']['latitude']
        entity['longitude'] = capital['location']['longitude']
        entity['continent'] = capital['continent']

        return self.ds.put(entity)

    def fetch(self):
        query = self.ds.query(kind=self.kind)
        #query.order = ['-timestamp']
        return self.get_query_results(query)

    def delete(self, capital_id):
        key = self.ds.key(self.kind, int(capital_id))
        capital = self.ds.delete(key)

    def get(self, capital_id):
        key = self.ds.key(self.kind, int(capital_id))
        capital = self.ds.get(key)
        if not capital:
            return None
        capital['id'] = capital_id
        return self.to_dto(capital)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(self.to_dto(entity))
        return results


def parse_note_time(note):
    """converts a greeting to an object"""
    return {
        'text': note['text'],
        'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    }

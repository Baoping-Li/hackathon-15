from datetime import datetime
from google.cloud import datastore
from google.cloud import storage, exceptions
from google.cloud.storage import Blob
from google.cloud import pubsub
import json
import utility

class Capital:

    def __init__(self):
        self.project_id = project=utility.project_id()
        self.ds = datastore.Client(self.project_id)
        self.kind = "Capitals"
        self.gcs = storage.Client(self.project_id)

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

    def store(self, capital, capital_id):

        capital['id'] = int(capital_id)
        key = self.ds.key(self.kind, capital['id'])
        entity = datastore.Entity(key)
        entity['name'] = capital['name']
        entity['countryCode'] = capital['countryCode']
        entity['country'] = capital['country']
        entity['latitude'] = capital['location']['latitude']
        entity['longitude'] = capital['location']['longitude']
        entity['continent'] = capital['continent']

        return self.ds.put(entity)

    def fetch(self, limit=None, property=None, value=None, distinct=None):
        query = self.ds.query(kind=self.kind)
        if property:
            query.add_filter(property, "=", value)
        if distinct:
            query.distinct_on = ['country']
            query.order = ['country']
        results = list()
        for entity in list(query.fetch(limit)):
            results.append(self.to_dto(entity))
        return results

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

    def cloud_store(self, bucket_name, capital_data):
        bucket = self.gcs.get_bucket(bucket_name)
        blob = Blob(capital_data['id'], bucket)
        blob.upload_from_string(json.dumps(capital_data), content_type='application/json')

    def publish(self, topic_name, capital_data):
        topic_items = topic_name.split('/')
        if len(query_items) != 2:
            return None

        project = topic_items[1]
        topic_id = topic_items[3]
        pubsub_client = pubsub.Client(project)
        topic = pubsub_client.topic(topic_id)
        data = json.dumps(capital_data).encode('utf-8')
        message_id = topic.publish(data)
        return message_id
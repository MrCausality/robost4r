import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')


# Helper class to convert a DynamoDB item to JSON.
class Decimal_Encoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(Decimal_Encoder, self).default(o)


class DynamoDB:

    def __init__(self, user_id):
        self.user_id = user_id

        self.last_table = ''
        self.last_keys = None
        self.last_item = None

    def get_value(self, table, keys, attribute=''):

        if self.last_item is None or self.last_table != table or self.last_keys != keys:

            self.last_table = table
            self.last_keys = keys

            try:
                self.last_item = dynamodb.Table(table).get_item(Key=keys)

                if 'Item' in self.last_item:
                    self.last_item = self.last_item['Item']
                else:
                    self.last_item = None
                    attribute = ''

            except ClientError as e:
                print(e.response['Error']['Message'])

        if attribute == '':
            return self.last_item
        else:
            return self.last_item[attribute]

    def put_value(self, table, item):

        try:
            dynamodb.Table(table).put_item(Item=item)

        except ClientError as e:
            print(e.response['Error']['Message'])

        return True

    def get_token(self):
        return self.get_value('Channels', {'Channel_ID': self.user_id}, 'oauth_Token')

    def get_secret(self):
        return self.get_value('Channels', {'Channel_ID': self.user_id}, 'oauth_Secret')

    def get_fact(self, number):
        return self.get_value('Facts', {'User_ID': self.user_id, 'number': int(number)}, 'text')

    def put_fact(self, number, text):
        return self.put_value('Facts', {'User_ID': self.user_id, 'number': int(number), 'text' : text})
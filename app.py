import json
import base64
import boto3
from flask import Flask, jsonify

app = Flask(__name__)

def get_response(lambda_response):
    response_decoded = lambda_response['Payload'].read().decode('utf-8')
    json_decoded = json.loads(response_decoded)
    json_decoded64 = base64.b64decode(json_decoded['body'])
    return json.loads(json_decoded64)


@app.route('/')
def index():
    session = boto3.Session(region_name='eu-west-1')
    client = session.client('lambda')
    response = client.invoke(
        FunctionName='privatedancer-dev',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            'body': '{}',
            'httpMethod': 'GET',
            'category': 'internal-routing',
            'path': '/',
            'headers': {
                'User-Agent': 'Dancer',
                'Content-Type': 'application/json'
            },
            'queryStringParameters': {},
            'pathParameters': {},
            'stageVariables': None,
            'requestContext': {}
        })
    )

    json_body = get_response(response)

    return jsonify(json_body)

if __name__ == '__main__':
    app.run()

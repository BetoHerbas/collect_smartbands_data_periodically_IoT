import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    iot_data_client = boto3.client('iot-data', region_name='us-east-1')
    
    table_name = 'smartbands_user_thing'
    
    response = dynamodb.scan(TableName=table_name)
    
    devices = [
        f"smartband_{item['serial_number']['S']}"
        for item in response['Items']
    ]
    
    message = {
        "state": {
            "desired": {
                "data_requested": 1 
            }
        }
    }
    
    for device in devices:
        topic = f"$aws/things/{device}/shadow/update"
        iot_data_client.publish(
            topic=topic,
            qos=1,
            payload=json.dumps(message)
        )
    
    return {"status": "Messages sent", "devices": devices}

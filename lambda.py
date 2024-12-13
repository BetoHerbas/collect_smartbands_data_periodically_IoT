import json
import boto3

iot_client = boto3.client('iot-data')

def lambda_handler(event, context):
    """
    Lambda function to update the shadow state of an IoT thing 
    based on the heart rate state received in the event.
    """
    try:
        thing_name = event.get('thing_name', None)
        heart_rate_state = event.get('heart_rate_state', None)
        
        if not thing_name or heart_rate_state is None:
            raise ValueError("Missing required fields: 'thing_name' or 'heart_rate_state'")

        heart_rate_messages = {
            0: "Pulso demasiado bajo",
            1: "Pulso normal",
            2: "Pulso demasiado alto"
        }

        message_text = heart_rate_messages.get(heart_rate_state)
        if message_text is None:
            print(f"Unknown pulse status: {heart_rate_state}")
            return

        shadow_payload = {
            "state": {
                "desired": {
                    "message": message_text
                }
            }
        }

        output_topic = f"$aws/things/{thing_name}/shadow/update"
        response = iot_client.publish(
            topic=output_topic,
            qos=1,
            payload=json.dumps(shadow_payload)
        )

        print(f"Message successfully posted: {message_text}")
        return response

    except Exception as e:
        print(f"Error processing event: {e}")
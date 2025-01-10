# src/services/rabbitmq_publisher.py
import aiormq
import json
from src.core.exceptions.base import BadRequestException

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"
QUEUE_NAME = "quiz_completed_queue"

class RMQEventPublisher:
    def __init__(self, conn_url: str = RABBITMQ_URL, queue_name: str = QUEUE_NAME):
        self.conn_url = conn_url
        self.queue_name = queue_name

    async def publish_event(self, event_payload: dict):
        connection = await aiormq.connect(self.conn_url)
        channel = await connection.channel()

        message_body = json.dumps(event_payload).encode()
        
        await channel.basic_publish(
            routing_key=self.queue_name,
            body=message_body
        )
        print("SUCCESS")
        await connection.close()

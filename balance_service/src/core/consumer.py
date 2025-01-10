import json
from uuid import UUID

import aiormq

from src.core.enums import EventType
from src.services.balance_service import BalanceService


class Consumer:

    def __init__(self, balance_service: BalanceService):
        self.balance_service = balance_service
        self.connection = None
        self.channel = None

    async def on_message(self, message: aiormq.abc.DeliveredMessage):
        await message.channel.basic_ack(message.delivery.delivery_tag)

    async def connect_to_rabbit_mq(self):
        self.connection = await aiormq.connect("amqp://guest:guest@rabbitmq/")
        self.channel = await self.connection.channel(1)
        await self.channel.queue_declare(queue="quiz_completed_queue",durable=True)
        await self.channel.basic_consume(
            queue="quiz_completed_queue", consumer_callback=self.handle_msg
        )

    async def handle_msg(self, message: aiormq.abc.DeliveredMessage):
        try:
            msg_json = json.loads(message.body.decode("utf-8"))
            if msg_json.get("event_type") == EventType.QUIZ_COMPLETED.value:
                print(f"Received response from QUIZ SERVICE: {msg_json}")
                await self.balance_service.process_quiz_completion(
                    user_id=UUID(msg_json.get("user_id")),
                    correct_count=msg_json.get("new_correct_answers"),
                    current_streak=msg_json.get("current_streak")
                    
                )
                await message.channel.basic_ack(message.delivery.delivery_tag)
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    async def close(self):
        if self.channel:
            await self.channel.close()
            print("Channel closed.")

        if self.connection:
            await self.connection.close()
            print("Connection closed.")

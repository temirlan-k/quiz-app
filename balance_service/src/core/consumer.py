import json
from uuid import UUID
import aiormq
from src.core.enums import EventType
from src.services.balance_service import BalanceService
from src.core.uow import UnitOfWork
from src.core.db import async_session_factory

class Consumer:

    def __init__(self):
        self.balance_service = BalanceService(uow=UnitOfWork(async_session_factory))
    
    async def on_message(self,message: aiormq.abc.DeliveredMessage):
        print(f"[x] {message.body!r}")

        await message.channel.basic_ack(
            message.delivery.delivery_tag
        )

    async def connect_to_rabbitmq(self):
        connection = await aiormq.connect("amqp://guest:guest@rabbitmq/")
        channel = await connection.channel(1)
        print("-------------Connected to RabbitMQ from Balance--------------")
        
        queue = await channel.queue_declare(queue="quiz_completed_queue", passive=True)
        print("Consume",queue)
        await channel.basic_consume(queue="quiz_completed_queue", consumer_callback=self.handle_msg)

    async def handle_msg(self,message: aiormq.abc.DeliveredMessage):
        try:
            msg_json = json.loads(message.body.decode('utf-8'))
            if msg_json.get("event_type") == EventType.QUIZ_COMPLETED.value:
                print(f"Received response from QUIZ SERVICE: {msg_json}")
                await self.balance_service.process_quiz_completion(
                    user_id=UUID(msg_json.get('user_id')),
                    correct_count=msg_json.get('new_correct_answers')
                )
                await message.channel.basic_ack(message.delivery.delivery_tag)
        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON: {e}")
import logging
import json
from uuid import UUID

import aiormq
from aiormq.abc import AbstractChannel, AbstractConnection, DeliveredMessage

from src.core.enums import EventType
from src.core.exceptions import BadRequestException
from src.services.balance_service import BalanceService

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, balance_service: BalanceService):
        self.balance_service = balance_service
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect_to_rabbit_mq(self) -> None:
        try:
            logger.info("Connecting to RabbitMQ at %s", "amqp://guest:guest@rabbitmq/")
            self.connection = await aiormq.connect("amqp://guest:guest@rabbitmq/")
            self.channel = await self.connection.channel(1)
            await self.channel.queue_declare(queue="quiz_completed_queue", durable=True)
            await self.channel.basic_consume(
                queue="quiz_completed_queue", consumer_callback=self.handle_msg
            )
            logger.info("Connected to RabbitMQ and started consuming messages.")
        except Exception as e:
            logger.exception("Failed to connect to RabbitMQ: %s", e)
            raise

    async def handle_msg(self, message: DeliveredMessage) -> None:
        try:
            logger.debug("Received message: %s", message.body)
            msg_json = json.loads(message.body.decode("utf-8"))
            event_type = msg_json.get("event_type")
            logger.debug("Parsed event_type: %s", event_type)

            if event_type == EventType.QUIZ_COMPLETED.value:
                logger.info("Processing QUIZ_COMPLETED event: %s", msg_json)
                user_id_str = msg_json.get("user_id")
                new_correct_answers = msg_json.get("new_correct_answers")
                current_streak = msg_json.get("current_streak")
                await self.balance_service.process_quiz_completion(
                    user_id=UUID(user_id_str),
                    correct_count=new_correct_answers,
                    current_streak=current_streak,
                )
                await self.channel.basic_ack(message.delivery.delivery_tag)
                logger.info(
                    "Successfully processed and acknowledged message: %s",
                    message.delivery.delivery_tag,
                )
            else:
                logger.warning("Received unknown event_type: %s", event_type)
                await self.channel.basic_ack(message.delivery.delivery_tag)
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
            await self.channel.basic_ack(message.delivery.delivery_tag)
        except Exception as e:
            logger.exception("Error handling message: %s", e)
            await self.channel.basic_nack(message.delivery.delivery_tag, requeue=False)

    async def close(self) -> None:
        try:
            if self.channel:
                await self.channel.close()
                logger.info("RabbitMQ channel closed.")
            if self.connection:
                await self.connection.close()
                logger.info("RabbitMQ connection closed.")
        except Exception as e:
            logger.exception("Error closing RabbitMQ connection/channel: %s", e)
            raise

from dependency_injector import containers, providers

from src.core.db import async_session_factory
from src.core.uow import UnitOfWork
from src.services.question import QuestionService
from src.services.quiz import QuizService
from src.services.rabbit_mq import RMQEventPublisher
from src.services.user_answer import AnswerService
from src.services.user_quiz_session import UserQuizSessionService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.api.v1"])

    db_session_factory = providers.Object(async_session_factory)

    uow = providers.Factory(UnitOfWork, session_factory=db_session_factory)

    rmq_publisher = providers.Singleton(RMQEventPublisher)

    quiz_service = providers.Factory(QuizService, uow=uow)
    question_service = providers.Factory(QuestionService, uow=uow)
    quiz_session_service = providers.Factory(
        UserQuizSessionService, uow=uow, publisher=rmq_publisher
    )
    answer_service = providers.Factory(AnswerService, uow=uow)

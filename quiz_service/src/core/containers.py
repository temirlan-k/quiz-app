from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import async_session_factory
from src.repositories.quiz import QuizRepository
from src.services.quiz import QuizService
from src.services.question import QuestionService
from src.core.uow import UnitOfWork


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["src.api.v1"]
    )
    
    db_session_factory = providers.Object(async_session_factory)
    
    uow = providers.Factory(
        UnitOfWork,
        session_factory=db_session_factory
    )
    
    
    quiz_service = providers.Factory(
        QuizService,
        uow=uow
    )
    question_service = providers.Factory(
        QuestionService,
        uow=uow
    )
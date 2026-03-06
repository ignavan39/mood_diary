from dependency_injector import containers, providers

from application.use_cases import (
    GetUserWeeklyStatsUseCase,
    RecordMoodUseCase,
    RegisterUserUseCase,
)
from infrastructure.ioc.container.infrastructure import InfrastructureContainer


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure: providers.Container[InfrastructureContainer] = providers.Container(
        InfrastructureContainer
    )

    register_user_use_case: providers.Factory[RegisterUserUseCase] = providers.Factory(
        RegisterUserUseCase, user_repo=infrastructure.user_repository.provided
    )

    get_user_weekly_stats_use_case: providers.Factory[GetUserWeeklyStatsUseCase] = (
        providers.Factory(
            GetUserWeeklyStatsUseCase,
            diary_repo=infrastructure.diary_repository.provided,
            user_repo=infrastructure.user_repository.provided,
        )
    )

    record_mood_use_case: providers.Factory[RecordMoodUseCase] = providers.Factory(
        RecordMoodUseCase,
        diary_repo=infrastructure.diary_repository.provided,
        user_repo=infrastructure.user_repository.provided,
    )

from dependency_injector import containers, providers

from application.use_cases import (
    EnsureUserUseCase,
    GetUserStatsUseCase,
    RecordMoodUseCase,
)
from application.use_cases.generate_mood_infographic import (
    GenerateMoodInfographicUseCase,
)
from application.use_cases.update_mood import UpdateMoodUseCase


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    get_user_stats_use_case: providers.Factory[GetUserStatsUseCase] = providers.Factory(
        GetUserStatsUseCase,
        diary_repo=infrastructure.diary_repository.provided,
        user_repo=infrastructure.user_repository.provided,
    )
    record_mood_use_case: providers.Factory[RecordMoodUseCase] = providers.Factory(
        RecordMoodUseCase,
        diary_repo=infrastructure.diary_repository.provided,
        user_repo=infrastructure.user_repository.provided,
    )

    update_mood_use_case: providers.Factory[UpdateMoodUseCase] = providers.Factory(
        UpdateMoodUseCase,
        diary_repo=infrastructure.diary_repository.provided,
    )

    generate_mood_infographic_use_case: providers.Factory[
        GenerateMoodInfographicUseCase
    ] = providers.Factory(
        GenerateMoodInfographicUseCase,
        diary_repo=infrastructure.diary_repository.provided,
        user_repo=infrastructure.user_repository.provided,
        chart_generator=infrastructure.chart_generator.provided,
    )

    ensure_user_use_case: providers.Factory[EnsureUserUseCase] = providers.Factory(
        EnsureUserUseCase,
        user_repo=infrastructure.user_repository.provided,
    )

from infrastructure.db_helper import db_helper
from infrastructure.orm.metadata_providers.positionsMetadataProvider import PositionsMetadataProvider
from infrastructure.orm.metadata_providers.providerManagerMetadataProvider import ProviderManagerMetadataProvider
from infrastructure.orm.metadata_providers.providersMetadataProvider import ProviderMetadataProvider
from use_cases.position import PositionsUseCases
from use_cases.providers import ProviderUseCases
from use_cases.provider_managers import ProviderManagerUseCases


def get_provider_provider() -> ProviderMetadataProvider:
    return ProviderMetadataProvider(db=db_helper)


def get_manager_provider() -> ProviderManagerMetadataProvider:
    return ProviderManagerMetadataProvider(db=db_helper)


def get_provider_use_cases() -> ProviderUseCases:
    return ProviderUseCases(
        providers=get_provider_provider(),
        managers=get_manager_provider(),
    )


def get_manager_use_cases() -> ProviderManagerUseCases:
    return ProviderManagerUseCases(managers=get_manager_provider())
def get_positions_provider() -> PositionsMetadataProvider:
    return PositionsMetadataProvider(db=db_helper)


def get_positions_use_cases() -> PositionsUseCases:
    return PositionsUseCases(positions=get_positions_provider())
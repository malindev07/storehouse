from infrastructure.db_helper import db_helper
from infrastructure.orm.metadata_providers.positionsMetadataProvider import (
    PositionsMetadataProvider,
)
from infrastructure.orm.metadata_providers.providerManagerMetadataProvider import (
    ProviderManagerMetadataProvider,
)
from infrastructure.orm.metadata_providers.providersMetadataProvider import (
    ProviderMetadataProvider,
)
from infrastructure.orm.metadata_providers.warehouseMetadataProvider import (
    WarehouseMetadataProvider,
)
from use_cases.position import PositionsUseCases
from use_cases.positions_markup import UpdatePositionsMarkupUseCase
from use_cases.providers import ProviderUseCases
from use_cases.provider_managers import ProviderManagerUseCases
from use_cases.warehouse import WarehousesUseCases


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


def get_warehouses_provider() -> WarehouseMetadataProvider:
    return WarehouseMetadataProvider(db=db_helper)


def get_warehouses_usecases() -> WarehousesUseCases:
    return WarehousesUseCases(warehouses=get_warehouses_provider())


def get_positions_provider() -> PositionsMetadataProvider:
    return PositionsMetadataProvider(db=db_helper)


def get_update_positions_markup_uc() -> UpdatePositionsMarkupUseCase:
    return UpdatePositionsMarkupUseCase(positions=get_positions_provider())

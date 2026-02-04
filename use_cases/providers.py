from __future__ import annotations

from uuid import UUID
from sqlalchemy.exc import IntegrityError

from infrastructure.orm.metadata_providers.providerManagerMetadataProvider import ProviderManagerMetadataProvider
from infrastructure.orm.metadata_providers.providersMetadataProvider import ProviderMetadataProvider


class ProviderUseCases:
    def __init__(
        self,
        providers: ProviderMetadataProvider,
        managers: ProviderManagerMetadataProvider,
    ):
        self.providers = providers
        self.managers = managers

    async def list_providers(self):
        return await self.providers.get_all()

    async def get_provider(self, provider_id: UUID):
        return await self.providers.get_by_id(provider_id)

    async def create_provider(self, data: dict):
        try:
            return await self.providers.insert(data=data, refresh=True)
        except IntegrityError as e:
            # например unique constraint (если будет)
            raise e

    async def update_provider(self, provider_id: UUID, patch: dict):
        return await self.providers.update_by_id(provider_id, patch, refresh=True)

    async def delete_provider(self, provider_id: UUID) -> bool:
        return await self.providers.delete_by_id(provider_id)

    async def create_provider_with_manager(self, provider_data: dict, manager_data: dict):
        """
        Бизнес-правило: у поставщика всегда есть карточка менеджера.
        Создаём provider, потом manager в одной транзакции (если у тебя есть такой метод).
        Если нет — можно сделать последовательно, но лучше одной транзакцией в ProviderMetadataProvider.
        """
        return await self.providers.create_with_manager(provider_data, manager_data)

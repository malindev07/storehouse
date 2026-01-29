from __future__ import annotations

from uuid import UUID

from infrastructure.orm.metadata_providers.providerManagerMetadataProvider import ProviderManagerMetadataProvider


class ProviderManagerUseCases:
    def __init__(self, managers: ProviderManagerMetadataProvider):
        self.managers = managers

    async def list_managers(self):
        return await self.managers.get_all()

    async def get_manager(self, manager_id: UUID):
        return await self.managers.get_by_id(manager_id)

    async def list_by_provider(self, provider_id: UUID):
        return await self.managers.get_by_provider_id(provider_id)

    async def create_manager(self, data: dict):
        return await self.managers.insert(data=data, refresh=True)

    async def update_manager(self, manager_id: UUID, patch: dict):
        return await self.managers.update_by_id(manager_id, patch, refresh=True)

    async def delete_manager(self, manager_id: UUID) -> bool:
        return await self.managers.delete_by_id(manager_id)

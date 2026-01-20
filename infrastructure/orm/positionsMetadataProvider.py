from dataclasses import dataclass


@dataclass
class PositionsMetadataProvider:

    def get_many(self):
        pass

    def get_by_id(self):
        pass

    def insert_many(self):
        pass

    def insert(self):
        pass

    def delete_many(self):
        pass

    def delete(self):
        pass

    def update_many(self):
        pass

    def update(self):
        pass


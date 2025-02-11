class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def add(self, *args, **kwargs):
        return self.repository.create(*args, **kwargs)

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, entity_id):
        return self.repository.get_by_id(entity_id)

    def update(self, entity_id, *args, **kwargs):
        return self.repository.update(entity_id, *args, **kwargs)

    def delete(self, entity_id):
        return self.repository.soft_delete(entity_id)

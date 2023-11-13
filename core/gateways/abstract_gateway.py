from sqlalchemy.orm import Session
from core.models import Base

from abc import ABC, abstractmethod


class AbstractGateway(ABC):
    model = None
    
    def get(self, **kwargs):
        raise NotImplementedError

    def create(self, **kwargs):
        raise NotImplementedError

    def update(self, model_id: int, model):
        raise NotImplementedError

    def delete(self, model_id: int):
        raise NotImplementedError

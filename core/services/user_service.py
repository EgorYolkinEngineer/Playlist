from dataclasses import asdict

from core.gateways.abstract_gateway import AbstractGateway
from core.gateways.user_gateway import (UserGateway, 
                                        user_gateway)


from core.models import User
from core.schemas import UserScheme


class UserService:
    model: User = User
    
    def __init__(self, 
                 gateway: UserGateway
                 ) -> None:
        self.gateway = gateway
        
    def create_user(self, 
                    user: UserScheme
                    ) -> None:
        model = self.model(**asdict(user))
        self.gateway.create(model)
        

user_service = UserService(gateway=user_gateway)
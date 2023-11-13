from core.gateways.abstract_gateway import AbstractGateway
from core.models import User

from core.conf.database import session, Session


class UserGateway(AbstractGateway):
    def __init__(self, 
                 session: Session):
        self.session = session

    def get(self, pk: int) -> User:
        return self.session.query(User).get(pk)

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()

    def update(self, pk: int, user: User):
        self.session.query(User).filter(User.pk == pk).update(user)
        self.session.commit()

    def delete(self, pk):
        self.session.query(User).filter(User.pk == pk).delete()
        self.session.commit()


user_gateway = UserGateway(session=session)
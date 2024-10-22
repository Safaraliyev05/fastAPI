import bcrypt
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import String, Boolean, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField
from starlette.authentication import BaseUser

from apps.models.database import BaseModel, db
from config import storage


class User(BaseModel, BaseUser):
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default="False")
    products: Mapped[list['Product']] = relationship('Product', back_populates='owner')
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('users/%Y/%m/%d')), nullable=True)

    def __str__(self):
        return super().__str__() + f" - {self.username}"

    @classmethod
    async def get_user_by_username(cls, username):
        query = select(cls).where(cls.username == username)
        return (await db.execute(query)).scalar()

    async def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    @classmethod
    async def generate(cls, count: int = 1):
        f = await super().generate(count)
        for _ in range(count):
            await cls.create(
                first_name=f.first_name(),
                last_name=f.last_name(),
                username=f.user_name(),
                password=f.password()
            )

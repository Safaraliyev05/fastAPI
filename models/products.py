from html import unescape

from config import storage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import BigInteger, VARCHAR, ForeignKey, select
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from models.db import CreatedModel, db


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage))
    price: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', back_populates='products')

    @property
    def get_photo(self):  # TODO check it
        html_code = f"""<img src="{self.photo}" alt="">"""
        return unescape(html_code)

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()

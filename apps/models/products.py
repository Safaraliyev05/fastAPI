from fastapi_storages.integrations.sqlalchemy import FileType
from slugify import slugify
from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, select, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import CreatedBaseModel, db
from config import storage


class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category', lazy='selectin')

    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    parent: Mapped['Category'] = relationship('Category', lazy='selectin', remote_side='Category.id',
                                              back_populates='subcategories')
    subcategories: Mapped[list['Category']] = relationship('Category', back_populates='parent', lazy='selectin')

    def __str__(self):
        _name = ''
        if self.parent is None:
            return self.name
        return f"{self.parent} -> {self.name}"


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(BigInteger, nullable=False)
    discount_price: Mapped[float] = mapped_column(BigInteger, nullable=True)

    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', lazy='selectin', back_populates='products')

    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    owner: Mapped['User'] = relationship('User', lazy='selectin', back_populates='products')

    images: Mapped[list['ProductImage']] = relationship('ProductImage', back_populates='products', lazy='selectin')

    __table_args__ = (
        CheckConstraint('discount_price <= price', name='check_discount_price'),
    )

    @classmethod
    async def get_by_slug(cls, slug: str):
        query = select(cls).where(cls.slug == slug)
        return (await db.execute(query)).scalar()


class ProductImage(CreatedBaseModel):
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('products/%Y/%m/%d')))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Product.id, ondelete='CASCADE'))
    products: Mapped['Product'] = relationship('Product', lazy='selectin', back_populates='images')

from fastapi_storages.integrations.sqlalchemy import FileType
from slugify import slugify
from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, select, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import CreatedBaseModel, db
from config import storage


class Category(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __str__(self):
        return super().__str__() + f" - {self.name}"


class Product(CreatedBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
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
    async def create(cls, **kwargs):
        _slug = slugify(kwargs['name'])
        while await cls.get_by_slug(_slug) is not None:
            _slug = slugify(kwargs['name'] + '-1')
        kwargs['slug'] = _slug

        if 'discount_price' in kwargs and kwargs['discount_price']:
            if kwargs['discount_price'] > kwargs['price']:
                raise ValueError("Discount price cannot be higher than price")

        return await super().create(**kwargs)

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()

    @classmethod
    async def get_by_slug(cls, slug: str):
        query = select(cls).where(cls.slug == slug)
        return (await db.execute(query)).scalar()


class ProductImage(CreatedBaseModel):
    photo: Mapped[ImageField] = mapped_column(FileType(storage=storage('products/%Y/%m/%d')))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Product.id, ondelete='CASCADE'))
    products: Mapped['Product'] = relationship('Product', lazy='selectin', back_populates='images')

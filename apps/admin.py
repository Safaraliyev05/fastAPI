from typing import Any

from slugify import slugify
from sqladmin import ModelView
from starlette.requests import Request

from apps.models import ProductImage, User, Product, Category


class UserAdmin(ModelView, model=User):
    column_list = ['id', 'username']


class ProductImageAdmin(ModelView, model=ProductImage):
    column_list = ['id', 'photo', 'product']


class ProductAdmin(ModelView, model=Product):
    column_list = ['id', 'name']
    form_excluded_columns = ['created_at', 'updated_at', 'slug']
    name_plural = 'Mahsulotlar'
    name = 'Mahsulot'

    async def insert_model(self, request: Request, data: dict) -> Any:
        data['slug'] = slugify(data['name'])
        return await super().insert_model(request, data)


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name', 'parent_id']
    name_plural = 'Kategoriyalar'
    name = 'Kategoriya'
    form_rules = [
        "name",
        "parent"
    ]
    can_export = False

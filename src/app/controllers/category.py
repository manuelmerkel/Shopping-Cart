from pprint import pprint

from pydantic import TypeAdapter
from sqlalchemy import select

from models.category import Category as CategoryModel
from schemas.category import Category as CategorySchema
from models.product import Product as ProductModel

from .base import Controller


class CategoryController(Controller[CategoryModel]):

    def get_categories(self) -> list[CategorySchema]:
        stmt = select(CategoryModel)
        categories = self.session.scalars(stmt).fetchall()
        return TypeAdapter(list[CategorySchema]).validate_python(categories)

    def get_category_with_product_info(self, category_id: int) -> list:#
        # TODO hier kann man das noch schöner machen
        stmt = select(CategoryModel, ProductModel)\
            .join(ProductModel, CategoryModel.category_id == ProductModel.category_id)\
            .where(CategoryModel.category_id == category_id)
        category_with_product_info = self.session.execute(stmt).fetchall()
        category_with_product_info = TypeAdapter(list).validate_python(category_with_product_info)
        combined_results = []
        for category, product in category_with_product_info:
            combined_result = {
                'category_id': category.category_id,
                'category_name': category.category_name,
                'product_id': product.product_id,
                'product_name': product.product_name,
                'description': product.description,
                'image': product.image,
                'price': product.price,
                'stock': product.stock
            }
            combined_results.append(combined_result)

        return combined_results

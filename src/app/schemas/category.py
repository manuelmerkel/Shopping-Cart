from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    category_name: str


class Category(CategoryCreate):
    category_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class CategoryUpdate(CategoryCreate):
    pass

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class CategoryRequest(BaseModel):
    name: str
    description: str

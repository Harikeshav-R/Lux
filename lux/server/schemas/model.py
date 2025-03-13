from pydantic import BaseModel


class ModelBase(BaseModel):
    model_name: str
    base_provider: str
    is_provider: bool
    supports_image_generation: bool


class ModelInDBBase(ModelBase):
    id: int

    class Config:
        orm_mode = True


class Model(ModelInDBBase):
    pass

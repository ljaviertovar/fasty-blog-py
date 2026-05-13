from pydantic import BaseModel, Field, ConfigDict

class PostBase(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=2, max_length=50)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    date_posted: str

    model_config = ConfigDict(from_attributes=True)
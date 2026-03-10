from pydantic import BaseModel


class PostFormat(BaseModel):
    title:str
    content:str
import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    openai_api_key: str


config = Config(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

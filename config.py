import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class OpenSearchConfig(BaseModel):
    hosts: list[str]
    port: int
    user: str
    password: str


class Config(BaseModel):
    openai_api_key: str

    opensearch: OpenSearchConfig


config = Config(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    opensearch=OpenSearchConfig(
        hosts=["localhost"],
        port=9200,
        user=os.getenv("OPENSEARCH_USER"),
        password=os.getenv("OPENSEARCH_PASSWORD"),
    ),
)

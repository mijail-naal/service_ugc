from pydantic import BaseModel, Field

from src.core.config import defaul_topic


class CreateTopic(BaseModel):
    name: str
    partition: int = Field(default=defaul_topic.partition)
    replication: int = Field(default=defaul_topic.replication)
    min_replicas: int = Field(default=defaul_topic.min_insync)
    retention: int = Field(default=defaul_topic.retention)

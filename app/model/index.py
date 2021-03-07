from pydantic import BaseModel
from enum import Enum

class Project(BaseModel):
    key: str
    name: str
    projectTypeKey: str
    projectTemplateKey: str
    description: str
    lead: str

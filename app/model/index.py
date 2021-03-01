from pydantic import BaseModel

class Project(BaseModel):
    key: str
    name: str
    projectTypeKey: str
    projectTemplateKey: str
    description: str
    lead: str
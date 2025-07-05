from pydantic import BaseModel, Field
from typing import List

class UserStory(BaseModel):
    as_a: str = Field(..., description="The type of user performing the action (e.g., Product Owner, User, Admin)")
    i_want_to: str = Field(..., description="The action the user wants to perform")
    so_that: str = Field(..., description="The benefit or value the user gains from the action")
    priority: str = Field("Medium", description="Priority of the user story (e.g., High, Medium, Low)")

class Epic(BaseModel):
    name: str = Field(..., description="The name of the epic")
    description: str = Field(..., description="A brief description of what the epic entails")

class Requirement(BaseModel):
    id: str = Field(..., description="Unique identifier for the functional requirement (e.g., FR001)")
    description: str = Field(..., description="Detailed description of the functional requirement")
    priority: str = Field("Medium", description="Priority of the requirement (e.g., High, Medium, Low)")

class RequirementsList(BaseModel):
    requirements: List[Requirement] = Field(..., description="A list of functional requirements for the product based on provided user stories.")

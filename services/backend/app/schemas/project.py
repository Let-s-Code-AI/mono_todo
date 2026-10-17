"""Pydantic schemas for project API requests and responses."""

from pydantic import BaseModel, Field

from app.db.models import ProjectRole


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(max_length=100, description="Project name")


class ProjectResponse(BaseModel):
    """Schema for project API responses."""

    id: int
    name: str
    owner_id: int

    model_config = {"from_attributes": True}


class MemberAdd(BaseModel):
    """Schema for adding a user to a project by email."""

    email: str = Field(max_length=255, description="Email of an existing user")


class MemberResponse(BaseModel):
    """Schema for project member API responses."""

    user_id: int
    email: str
    role: ProjectRole

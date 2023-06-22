from typing import List
from models.projects import Project
from schemas.projects import ProjectInitializeSchema, ProjectRetrieveSchema, ProjectSchema
from services.base import BaseService


class ProjectService(BaseService):
  def get_projects(self) -> List[ProjectRetrieveSchema]:
    """Get all projects."""

    locations = self.session.query(Project).all()
    return [ProjectRetrieveSchema(**location.to_dict()) for location in locations]

  def get_project(self, location_id: int) -> ProjectRetrieveSchema:
    """Get project by ID."""

    location = self.session.query(Project).get(location_id)

    if location:
      return ProjectRetrieveSchema(**location.to_dict())
    return None

  def create_project(self, project: ProjectInitializeSchema) -> ProjectSchema:
    """Create project."""

    new_project = Project(**project.dict())
    self.session.add(new_project)
    self.session.commit()

    return ProjectSchema(**new_project.to_dict())

from math import ceil
from typing import List
from models import Location, User
from models.projects import Project
from schemas.projects import ProjectInitializeSchema, ProjectListResponseSchema, ProjectRetrieveSchema, ProjectUpdateSchema
from services.base import BaseService
from sqlalchemy import func, desc, or_


class ProjectService(BaseService):

  def get_projects(self, page: int, size: int, filter_param: str = None) -> ProjectListResponseSchema:
    """Get paginated projects with total pages and combined filter."""

    offset = (page - 1) * size
    query = self.session.query(Project).\
        outerjoin(Project.user).\
        outerjoin(Project.location).\
        order_by(desc(Project.updated_at))

    if filter_param:
      search_term = filter_param.lower()  # Convert the filter to lowercase
      query = query.filter(
          or_(
              func.lower(Project.name).like(f"%{search_term}%"),
              func.lower(Location.place).like(f"%{search_term}%"),
              func.lower(User.first_name).like(f"%{search_term}%"),
              func.lower(User.last_name).like(f"%{search_term}%"),
          )
      )

    count = query.count()
    projects = query.offset(offset).limit(size).all()
    total_pages = ceil(count / size)

    return ProjectListResponseSchema(page=page, total=total_pages, projects=projects, page_size=size)

  def get_project(self, project_id: int) -> ProjectRetrieveSchema:
    """Get project by ID."""

    project = self.session.query(Project).get(project_id)

    if project:
      return ProjectRetrieveSchema.from_orm(project)
    return None

  def create_project(self, project: ProjectInitializeSchema) -> ProjectRetrieveSchema:
    """Create project."""

    new_project = Project(**project.dict())
    self.session.add(new_project)
    self.session.commit()

    return ProjectRetrieveSchema.from_orm(new_project)

  def update_project(self, id: int, project: ProjectUpdateSchema) -> ProjectRetrieveSchema:
    """Update project."""
    project_to_update = self.session.query(Project).get(id)

    if project_to_update:
      for attr, value in project.dict(exclude_unset=True, exclude_defaults=True).items():
        setattr(project_to_update, attr, value)
      self.session.commit()

      return ProjectRetrieveSchema.from_orm(project_to_update)

    return None

  def delete_project(self, id: int) -> bool:
    """Delete project."""

    project_to_delete = self.session.query(Project).get(id)

    if project_to_delete:
      self.session.delete(project_to_delete)
      self.session.commit()
      return True

    return False

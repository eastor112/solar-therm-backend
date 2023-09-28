from typing import List, Optional
from models.pipeline import Pipeline
from schemas.pipelines import PipelineCreateSchema, PipelineUpdateSchema, PipelineRetrieveSchema
from services.base import BaseService


class PipelineService(BaseService):
  def create_pipeline(self, pipeline_data: PipelineCreateSchema) -> PipelineRetrieveSchema:
    """Create a new pipeline."""

    pipeline = Pipeline(**pipeline_data.dict())
    self.session.add(pipeline)
    self.session.commit()
    return PipelineRetrieveSchema(**pipeline.to_dict())

  def get_pipelines(self) -> List[PipelineRetrieveSchema]:
    """Get all pipelines."""

    pipelines = self.session.query(Pipeline).order_by(Pipeline.id).all()
    return [PipelineRetrieveSchema(**pipeline.to_dict()) for pipeline in pipelines]

  def get_pipeline(self, pipeline_id: int) -> Optional[PipelineRetrieveSchema]:
    """Get a pipeline by ID."""

    pipeline = self.session.query(Pipeline).get(pipeline_id)
    if pipeline:
      return PipelineRetrieveSchema(**pipeline.to_dict())
    return None

  def update_pipeline(self, pipeline_id: int, pipeline_data: PipelineUpdateSchema) -> Optional[PipelineRetrieveSchema]:
    """Update a pipeline by ID."""

    pipeline = self.session.query(Pipeline).get(pipeline_id)
    if pipeline:
      for attr, value in pipeline_data.dict(exclude_unset=True, exclude_defaults=True).items():
        setattr(pipeline, attr, value)
      self.session.commit()
      return PipelineRetrieveSchema(**pipeline.to_dict())
    return None

  def delete_pipeline(self, pipeline_id: int) -> bool:
    """Delete a pipeline by ID."""

    pipeline = self.session.query(Pipeline).get(pipeline_id)
    if pipeline:
      self.session.delete(pipeline)
      self.session.commit()
      return True
    return False

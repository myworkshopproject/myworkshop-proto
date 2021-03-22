from core.models import BaseModel as CoreBaseModel


class BaseModel(CoreBaseModel):
    class Meta(CoreBaseModel.Meta):
        abstract = True

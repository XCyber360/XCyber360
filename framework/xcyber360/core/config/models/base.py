from pydantic import BaseModel, ConfigDict


class Xcyber360ConfigBaseModel(BaseModel):
    """Main model for the configuration sections."""
    model_config = ConfigDict(use_enum_values=True)

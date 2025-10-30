from pydantic import BaseModel, ConfigDict


class SavedRecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipe_id: int
    user_id: int


class SaveRecipeRequest(BaseModel):
    recipe_id: int

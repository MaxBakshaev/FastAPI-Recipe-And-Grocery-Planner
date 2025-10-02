from core.models import Recipe
from core.schemas.recipe import ProductInRecipe, RecipeResponse


def map_recipe_to_response(recipe: Recipe) -> RecipeResponse:
    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        body=recipe.body,
        user_id=recipe.user_id,
        products=[
            ProductInRecipe(
                product_id=assoc.product_id,
                quantity=assoc.quantity,
                calories_per_unit=assoc.calories_per_unit,
            )
            for assoc in recipe.product_associations
        ],
    )

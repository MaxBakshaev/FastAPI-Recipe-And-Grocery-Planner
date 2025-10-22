from core.models import Recipe
from core.schemas import ProductInRecipe, RecipeResponse


def map_recipe_to_response(recipe: Recipe) -> RecipeResponse:
    """Преобразует объект модели Recipe в RecipeResponse"""
    return RecipeResponse(
        id=recipe.id,
        title=recipe.title,
        body=recipe.body,
        user_id=recipe.user_id,
        image_url=recipe.image_url,
        products=[
            ProductInRecipe(
                product_id=assoc.product_id,
                quantity=assoc.quantity,
                calories_per_gram=assoc.calories_per_gram,
            )
            for assoc in recipe.product_associations
        ],
        total_calories=recipe.total_calories,
        total_quantity=recipe.total_quantity,
    )

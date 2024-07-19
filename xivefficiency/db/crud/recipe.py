

from xivefficiency.db.models_generated.Item import Item
from xivefficiency.db.models_generated.Recipe import Recipe


def recipe_get_ingredients(recipe: Recipe) -> list[tuple[Item, int]]:
    ret = []
    if (recipe.amount_ingredient0 > 0):
        ret.append((recipe.item_ingredient0, recipe.amount_ingredient0))
    if (recipe.amount_ingredient1 > 0):
        ret.append((recipe.item_ingredient1, recipe.amount_ingredient1))
    if (recipe.amount_ingredient2 > 0):
        ret.append((recipe.item_ingredient2, recipe.amount_ingredient2))
    if (recipe.amount_ingredient3 > 0):
        ret.append((recipe.item_ingredient3, recipe.amount_ingredient3))
    if (recipe.amount_ingredient4 > 0):
        ret.append((recipe.item_ingredient4, recipe.amount_ingredient4))
    if (recipe.amount_ingredient5 > 0):
        ret.append((recipe.item_ingredient5, recipe.amount_ingredient5))
    if (recipe.amount_ingredient6 > 0):
        ret.append((recipe.item_ingredient6, recipe.amount_ingredient6))
    if (recipe.amount_ingredient7 > 0):
        ret.append((recipe.item_ingredient7, recipe.amount_ingredient7))
    return ret

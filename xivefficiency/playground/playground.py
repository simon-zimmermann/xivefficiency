

from sqlmodel import Session, select
from xivefficiency.db import crud
from xivefficiency.db.models_generated.Item import Item
from xivefficiency.db.models_generated.Recipe import Recipe


def playground(engine):
    with Session(engine) as session:
        item = session.get(Item, 43316)
        recipe_overview(session, item)


def recipe_overview(session: Session, item: Item):
    print(item.name)
    statement = select(Recipe).where(Recipe.item_result == item)
    recipes = session.exec(statement)
    for recipe in recipes:
        ingredients = crud.recipe_get_ingredients(recipe)
        print(f"printing recipe for {item.name}")
        for ingredient in ingredients:
            print(f"\tItem: {ingredient[0].name}, Amount: {ingredient[1]}")


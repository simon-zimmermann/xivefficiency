from sqlmodel import Session, select
from statistics import median

from webapp.db.models.UniversalisEntry import UniversalisEntry
from webapp.db.models_generated.Item import Item
from webapp.db.crud import gathering
from webapp.db import engine


def get_by_item(item_id: int) -> list[UniversalisEntry]:
    with Session(engine) as session:
        statement = select(UniversalisEntry).filter(UniversalisEntry.item_id == item_id)
        return session.exec(statement).all()


def get_minimum(item_id: int):
    data = get_by_item(item_id)
    if len(data) == 0:
        return 0
    else:
        return min([entry.single_price for entry in data])


def get_arithmethic_avg(item_id: int):
    data = get_by_item(item_id)
    listing_count = len(data)
    listing_sum = sum([entry.single_price for entry in data])
    if listing_count == 0:
        arithmethic_avg = 0
    else:
        arithmethic_avg = listing_sum / listing_count
    return arithmethic_avg


def get_median(item_id: int):
    data = get_by_item(item_id)
    if len(data) == 0:
        return 0
    else:
        return median([entry.single_price for entry in data])


def get_realistic_avg(item_id: int, buy_count: int = 99):
    data = get_by_item(item_id)
    # special average
    rolling_sum = 0
    rolling_count = 0
    current_weight = 1
    min_weight = 1 / 4
    buy_count_remaining = buy_count
    it = iter(data)
    try:
        curr_price = 0
        curr_count = 0
        while True:
            # weight has been reduced low enough -> calculation is complete
            if current_weight < min_weight:
                break
            # current listing is exhausted -> get next listing
            elif curr_count == 0:
                curr_listing = next(it)
                curr_price = curr_listing.single_price
                curr_count = curr_listing.quantity
            # current weight is exhausted -> reduce weight and reset buy_count_remaining
            elif buy_count_remaining == 0:
                buy_count_remaining = buy_count
                current_weight /= 2
            # we can buy all items from this listing -> do so
            elif buy_count_remaining >= curr_count:
                buy_count_remaining -= curr_count
                rolling_sum += curr_price * curr_count * current_weight
                rolling_count += curr_count * current_weight
                curr_count = 0
            # we cant buy all items from this listing with the current weight -> buy as many as we can
            else:
                curr_count -= buy_count_remaining
                rolling_sum += curr_price * buy_count_remaining * current_weight
                rolling_count += buy_count_remaining * current_weight
                buy_count_remaining = 0

    except StopIteration:
        pass

    if rolling_count == 0:
        special_avg = 0
    else:
        special_avg = rolling_sum / rolling_count
    return special_avg


def get_all(items: list[Item]):
    ret = []
    for item in items:
        data = {
            "item": item,
            "item_id": item.id,
            "item_name": item.name,
            "arithmethic_avg": get_arithmethic_avg(item.id),
            "median": get_median(item.id),
            "minimum": get_minimum(item.id),
            "realistic_avg": get_realistic_avg(item.id)
        }
        ret.append(data)
    return ret


def test_average_calc() -> list[dict]:
    itemlist = gathering.get_gatherable_all()
    prices = get_all(itemlist)
    sorted_prices = sorted(prices, key=lambda x: x["minimum"], reverse=True)
    sorted_prices = sorted_prices[:3]
    for entry in sorted_prices:
        entry.pop("item")
    return sorted_prices

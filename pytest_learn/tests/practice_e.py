from collections import Counter

def unique_tags(raws: list[str]) -> list[str]:
   lower_list = [r.lower() for r in raws]
   final_list = set(lower_list)
   return sorted(final_list)

some_list = ['Py','api','py','API']



def unique_tags_short(raws: list[str]) -> list[str]:
   return sorted({r.lower() for r in raws})


some_dict = [{"name": "Alice", "status": "active" }, {"name": "Bob", "status": "active" }, {"name": "James", "status": "anavalible" }]

def most_common_status(tickets: list[dict]) -> str:
   return Counter(s['status'] for s in tickets).most_common(1)[0][0]
   

paid_orders = [{"status": "refused", "item": "scooter"}, {"status": "paid", "item": "scooter"}, {"status": "paid", "item": "scooter"}, {"status": "paid", "item": "scooter"},]

def all_paid(orders: list[dict]) -> bool:
    return all(o['status'] == 'paid' for o in orders)

def any_refunded(orders: list[dict]) -> bool:
    return any(o['status'] == 'refused' for o in orders)

paid_customer = [{"name": "Bob", "amount": 700},{"name": "Alice", "amount": 900},{"name": "Jon", "amount": 670}]
def richest(orders: list[dict]) -> str:
   return max(orders, key= lambda x: x['amount'])['name']


# 5. `numbered(titles: list[str]) -> list[str]`
#    `['a','b']` -> `['1. a', '2. b']`.
#    Инструмент: **enumerate(start=1)** + f-string.

# 6. `names_to_scores(names: list[str], scores: list[int]) -> dict[str,int]`
#    `['a','b'], [10,20]` -> `{'a':10,'b':20}`.
#    Инструмент: **zip** + **dict-comprehension**.


def numbered_titles(title_sist: list[str]) -> list[str]:
   return [f"{i}. {t}" for i, t in enumerate(title_sist, start=1)]


def names_to_scores(names: list[str], scores: list[int]) -> dict[str,int]:
   return {k: v for k, v in zip(names, scores)}


def running_total(nums: list[int]) -> int:
    total = 0
    for num in nums:
       total += num
       yield total


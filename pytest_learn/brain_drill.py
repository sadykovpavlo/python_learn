from collections import Counter, defaultdict
# ═══════════════════════════════════════════════════════════════════
# BRAIN PYTHON — выжимаем данные из структур (как из response.json())
# Делай ПО ОДНОЙ. Пиши функцию, раскомментируй print, запусти:
#   .venv/bin/python brain_drill.py
# Зови на ревью после каждой (или пачкой — как удобнее).
# ═══════════════════════════════════════════════════════════════════


# ── 1. Фильтр + агрегация (grouping + условие) ─────────────────────
# Верни СПИСОК имён клиентов, которые в сумме потратили СТРОГО больше 100.
# Порядок неважен. Инструмент: словарь-аккумулятор -> потом фильтр.
orders = [
    {"customer": "a", "amount": 80},
    {"customer": "b", "amount": 80},
    {"customer": "a", "amount": 300},   # a: 80+300 = 380
    {"customer": "c", "amount": 45},    # c: 45
    {"customer": "b", "amount": 30},    # b: 80+30 = 110
]

def big_spenders(orders: list[dict]) -> list[str]:
    amount_spended = defaultdict(int)
    for order in orders:
        amount_spended[order["customer"]] += order["amount"]
    top_pairs = [s for s, m in amount_spended.items() if m > 100]
    return top_pairs


# def big_spenders(orders: list[dict]) -> list[str]:
#     ...
# ожидаем (в любом порядке): ['a', 'b']
# print(big_spenders(orders))


# ── 2. Вложенность (dict внутри dict) ──────────────────────────────
# Ответ API с профилями. Верни список email'ов ТОЛЬКО активных юзеров.
# Инструмент: u['profile']['email'] + фильтр по u['active'].
users = [
    {"id": 1, "active": True,  "profile": {"email": "a@x.com", "city": "Kyiv"}},
    {"id": 2, "active": False, "profile": {"email": "b@x.com", "city": "Lviv"}},
    {"id": 3, "active": True,  "profile": {"email": "c@x.com", "city": "Kyiv"}},
]

def active_emails(users: list[dict]) -> list[str]:
    return [u["profile"]["email"] for u in users if u["active"]]
    # for user in users:
    #     if user["active"] == True:
    #         active_user.append(user["profile"]["email"])
    # return active_user

# def active_emails(users: list[dict]) -> list[str]:
#     ...
# ожидаем: ['a@x.com', 'c@x.com']
# print(active_emails(users))


# ── 3. Разворот списка внутри словаря (flatten + unique) ───────────
# У каждого поста есть список тегов. Верни ВСЕ уникальные теги,
# отсортированные. Инструмент: два цикла (или comprehension) + set + sorted.
posts = [
    {"title": "p1", "tags": ["py", "api"]},
    {"title": "p2", "tags": ["api", "qa"]},
    {"title": "p3", "tags": ["py"]},
]
def all_tags(posts: list[dict]) -> list[str]:
    set_tags = {tag for p in posts for tag in p["tags"]}
    return sorted(set_tags)


    
# def all_tags(posts: list[dict]) -> list[str]:
#     ...
# ожидаем: ['api', 'py', 'qa']
# print(all_tags(posts))


# ── 4. Группировка по ключу -> список объектов ─────────────────────
# Сгруппируй товары по категории: {категория: [названия...]}.
# Инструмент: setdefault (ты его уже умеешь по staff_grouping).
products = [
    {"name": "milk",   "cat": "food"},
    {"name": "phone",  "cat": "tech"},
    {"name": "bread",  "cat": "food"},
    {"name": "laptop", "cat": "tech"},
]

def group_by_category(products: list[dict]) -> dict[str, list[str]]:
    grouped_dict = defaultdict(list)
    for product in products:
        grouped_dict[product['cat']].append(product['name'])
    return dict(grouped_dict)
    
# def group_by_category(products: list[dict]) -> dict[str, list[str]]:
#     ...
# ожидаем: {'food': ['milk', 'bread'], 'tech': ['phone', 'laptop']}
print(group_by_category(products))


# ── 5. Самый острый: два уровня агрегации ──────────────────────────
# По каждой категории верни СРЕДНИЙ рейтинг. Округли до 1 знака (round(x, 1)).
# Инструмент: сначала собери {cat: [ratings...]}, потом посчитай среднее.
reviews = [
    {"cat": "food", "rating": 4.0},
    {"cat": "tech", "rating": 5.0},
    {"cat": "food", "rating": 3.0},   # food: (4+3)/2 = 3.5
    {"cat": "tech", "rating": 4.0},   # tech: (5+4)/2 = 4.5
]
# def avg_rating_by_cat(reviews: list[dict]) -> dict[str, float]:
#     raitng_by_category = defaultdict(float)
#     for review in reviews:
#         raitng_by_category[review['cat']] += review['rating']
#     for k,v in raitng_by_category.items():
#         raitng_by_category[k] = round(v / 2, 1)
#     return dict(raitng_by_category)

def avg_rating_by_cat(reviews: list[dict]) -> dict[str, float]:
    category_rating = defaultdict(list)
    for review in reviews:
        category_rating[review['cat']].append(review['rating'])
    for k,v in category_rating.items():
        category_rating[k] = round(sum(v) / len(v), 1)
    return dict(category_rating)


# def avg_rating_by_cat(reviews: list[dict]) -> dict[str, float]:
#     ...
# ожидаем: {'food': 3.5, 'tech': 4.5}
print(avg_rating_by_cat(reviews))

from database import engine
from models import Item
from sqlalchemy.orm import Session


conn = engine.connect()
transaction = conn.begin()
session = Session(bind=conn)

session.add(Item(name='ghost', price = 1))
session.flush()

print(session.query(Item).count())
transaction.rollback()
print(session.query(Item).count())



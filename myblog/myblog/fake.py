import random

from faker import Faker

from myblog.extensions import db
from myblog.models import Admin, Category, Post

faker = Faker()

def faker_admin():
    admin = Admin(
        username='admin',
        password='123456'
    )
    db.session.add(admin)
    db.session.commit()


def faker_category(count=10):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=faker.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def faker_posts(nums=50):
    for i in range(nums):
        post = Post(
            title = faker.sentence(),
            body = faker.text(2000),
            category = Category.query.get(random.randint(2, Category.query.count())),
            timestamp = faker.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()

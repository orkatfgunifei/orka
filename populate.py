from app import db
from app.models.contact import ContactGroup, Gender, Contact
import random
from datetime import datetime


def get_random_name(names_list, size=1):
    name_lst = [names_list[random.randrange(0, len(names_list))].capitalize() for i in range(0, size)]
    return " ".join(name_lst)


try:
    db.session.add(ContactGroup(name='DEV Time'))
    db.session.add(ContactGroup(name='Clientes'))
    db.session.add(ContactGroup(name='Amigos'))
    db.session.commit()
except:
    db.session.rollback()

try:
    db.session.add(Gender(name='Masculino'))
    db.session.add(Gender(name='Feminino'))
    db.session.commit()
except:
    db.session.rollback()

f = open('NAMES.DIC', "rb")
names_list = [x.strip() for x in f.readlines()]

f.close()

for i in range(1, 50):
    c = Contact()
    c.name = get_random_name(names_list, random.randrange(2, 6))
    c.address = 'Rua ' + names_list[random.randrange(0, len(names_list))]
    c.personal_phone = random.randrange(1111111, 9999999)
    c.personal_celphone = random.randrange(1111111, 9999999)
    c.contact_group_id = random.randrange(1, 4)
    c.gender_id = random.randrange(1, 3)
    year = random.choice(range(1900, 2012))
    month = random.choice(range(1, 12))
    day = random.choice(range(1, 28))
    c.birthday = datetime(year, month, day)
    db.session.add(c)
    try:
        db.session.commit()
        print "inserido", c
    except:
        db.session.rollback()
    
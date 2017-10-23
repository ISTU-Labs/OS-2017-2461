# filename: happy_birthday.py
"""A basic (single function) API written using hug"""
import hug

@hug.get('/happy_birthday')
def happy_birthday(name, age:hug.types.number=1):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals())

# http://172.16.199.10:8000/happy_birthday?name=hug&age=1

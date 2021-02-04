from marshmallow import Schema, fields, post_load, ValidationError


class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f'{ self.name } is { self.age } years old and email: {self.email}'


class PersonSchema(Schema):
    name = fields.String()
    age = fields.Integer()
    email = fields.Email()

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)


input_data = {}
input_data['name'] = input("What is your name? ")
input_data['age'] = int(input("What is your age? "))
input_data['email'] = input("What is your email? ")

try:
    schema = PersonSchema()
    result = schema.load(input_data)

    # person = Person(name=input_data['name'], age=input_data['age'])
    print(result)

    result_deserialize = schema.dump(result)
    print(result_deserialize)

except ValidationError as err:
    print(err)
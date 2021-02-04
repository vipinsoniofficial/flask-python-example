from marshmallow import Schema, fields, post_load, ValidationError, validates, validate


class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f'{ self.name } is { self.age } years old and email: {self.email}'


def validate_age(age):
    if age < 20:
        # return False
        raise ValidationError('the age is not in criteria!')


class PersonSchema(Schema):
    name = fields.String(validate=validate.Length(max=10))
    age = fields.Integer(validate=validate_age)
    # age = fields.Integer()
    email = fields.Email()
    location = fields.String(required=True)  # location = fields.String(required=False)

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)

    @validates('age')
    def validate_age(self, age):
        if age > 60:
            # return False
            raise ValidationError('the age is out of criteria!')


input_data = {}
input_data['name'] = input("What is your name? ")
input_data['age'] = input("What is your age? ")
input_data['email'] = input("What is your email? ")

# print(input_data)
try:
    schema = PersonSchema()
    result = schema.load(input_data)
    # result = PersonSchema().load({"name": "john", "age": 20, "email": "abcdefgh@qwer.com"})
    # person = Person(name=input_data['name'], age=input_data['age'])
    print(result)

    # result_deserialize = PersonSchema().dump(result)
    result_deserialize = schema.dump(result)
    print(result_deserialize)

except ValidationError as err:
    # display error in the field error is has happened
    print(err)
    # valid_data = print valid data leaving aside the incorrect data(data not in correct format)
    print(err.valid_data)
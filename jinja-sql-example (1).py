from jinjasql import JinjaSql

j = JinjaSql(param_style='named')


template_all_user = """
    SELECT * from {{table_name | sqlsafe}}
"""
param_all_user ={
    "table_name": "info"
}


template_for_id = """
    SELECT * from {{table_name | sqlsafe}} where id = :id
"""

params_for_id = {
    "table_name": "info",
    "id": 1
}

template_update = """
    update {{table_name | sqlsafe }} 
    set firstname = :firstname, lastname= :lastname, age = :age, email = :email, password= :password
    where id = :id
"""

params_update = {
    "table_name": "info",
    "firstname": "firstname",
    "lastname": "lastname",
    "age": "age",
    "email": "email",
    "password": "password",
    "id": 1
}

template_by_email = """
    SELECT * from {{table_name | sqlsafe}}
    where id = :id
    {% if email %}
    and email = :email
    {% endif %}
"""

params_email = {
    "table_name": "info",
    "id": 2,
    "email": "string1"
}

all_user, bind_all = j.prepare_query(template_all_user, param_all_user)

user_by_id, bind_by_id = j.prepare_query(template_for_id, params_for_id)
print(user_by_id)
print(bind_by_id)

update_by_id, bind_upate = j.prepare_query(template_update, params_update)

user_by_email, bind_by_email = j.prepare_query(template_by_email, params_email)
print(user_by_email)
print(bind_by_email)

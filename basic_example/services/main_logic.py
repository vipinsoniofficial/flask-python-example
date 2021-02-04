from server import app, logging
from flask import request, jsonify
from model.main_model import user_schema, users_schema, User
from config import db

# logging.basicConfig(filename='main_logs.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


@app.route("/user", methods=["POST"])
def add_user():
    try:
        logging.info("In POST add_user method of main_logic.py")
        username = request.json['username']
        email = request.json['email']

        # validate  input
        if username and email and request.method == 'POST':
            logging.info("In if condition of POST add_user method of main_logic.py ")
            new_user = User(username, email)
            logging.info("after new_user added in main_logic.py")
            db.session.add(new_user)
            db.session.commit()

            logging.info("New User Details: username: {}, email: {}".format(username, email))
            logging.info("Done commit")

            all_users = User.query.all()
            result = users_schema.dump(all_users)
            return users_schema.jsonify(result)

        else:
            logging.warning("Not able to add new user")
            return 'Error while adding new user'

    except Exception as ex:
        logging.error("Error occurred in POST add_user method of main_logic.py")
        print(ex)


@app.route("/user", methods=["GET"])
def get_user():
    try:
        logging.info("In GET get_user method of main_logic.py")

        all_users = User.query.all()
        result = users_schema.dump(all_users)

        if all_users and result and request.method == 'GET':
            logging.info("Success: Displaying all the data")
            return jsonify(result)

        else:
            return 'Error in Extracting Data'

    except Exception as ex:
        logging.error("Error occurred in GET get_user method of main_logic. Not able to collect data")
        print(ex)


@app.route("/user/<id>", methods=["GET"])
def user_details(id):
    try:
        logging.info("In  GET/<id> user_details method of main_logic.py")

        if id and request.method == 'GET':
            user = User.query.get(id)
            logging.info("Success: Displaying all the data of {}".format(user))
            return jsonify(user)

        else:
            return 'Error in Extracting Data of id:{}'.format(id)

    except Exception as ex:
        logging.error("Error occurred in GET/<id> user_details method of main_logic. Not able to Collect data")
        print(ex)


@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    try:
        logging.info("In PUT/<id> user_update method of main_logic.py")

        if id and request.method == 'PUT':
            user = User.query.get(id)
            username = request.json['username']
            email = request.json['email']

            if username is not None and email is not None:
                user.email = email
                user.username = username

                db.session.commit()
                logging.info("success: updated {}".format(user))
                return jsonify(user)

            else:
                return 'Error username and email not available'

        else:
            return 'Error in updating data of id:{}'.format(id)

    except Exception as ex:
        logging.error("Error occurred in PUT user_update method of main_logic. Not able to update")
        print(ex)


@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    try:
        logging.info("In DELETE user_delete method of main_logic.py")
        if id and request.method == 'DELETE':
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()

            logging.info("success: Deleted {}".format(user))
            return jsonify(user)
        else:
            return 'Error in Deleting Data of id:{}'.format(id)

    except Exception as ex:
        logging.error("Error occurred in DELETE user_delete method of main_logic.Not able to delete")
        print(ex)

'''
if __name__ == "__main__":
    app.run(port=8333, debug=True)
'''
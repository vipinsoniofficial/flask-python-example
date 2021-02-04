from server import app, logging
from flask import request, redirect, url_for
from services.main_logic import *


@app.route('/start', methods=['POST', 'GET'])
def start():
    try:
        logging.info("In /start in main_controller.py")

        if request.methods == "POST":
            logging.info("Into POST condition in main_controller.py")
            username = request.json['username']
            email = request.json['email']

            if len(username) > 5 and len(email) > 14 and request.methods == 'POST':
                logging.info("redirecting to /post method of main_logic.py")
                return redirect(url_for('/user'), method='POST')

        elif request.methods == "GET":
            logging.info("Into GET condition in main_controller")
            logging.info("redirecting to /get method of main_logic.py")
            return redirect(url_for('/user'), method='GET')

        else:
            logging.warning("Method entered is not defined")
            return 'Invalid Choice'

    except Exception as ex:
        logging.error("Exception occurred at /start")
        print(ex)


@app.route('/start/<id>', methods=['GET', 'PUT', 'DELETE'])
def start_id(id):
    try:
        logging.info("In /start/<id> in main_controller")

        if request.methods == "PUT":
            logging.info("Into Put method in main_controller.py")
            logging.info("redirecting to /put/<id> method in main_logic.py")
            return redirect(url_for('/user/<id>'), method='PUT')

        elif request.methods == "DELETE":
            logging.info("Into Delete method in main_controller")
            logging.info("redirecting to /delete/<id> method in main_logic.py")
            return redirect(url_for('/user/<id>'), method='DELETE')

        elif request.methods == "GET":
            logging.info("Into GET/<id> method in main_controller")
            logging.info("redirecting to /get/<id> method in main_logic.py")
            return redirect(url_for('/user/<id>'), method='GET')

    except Exception as ex:
        logging.error("Exception occurred at /start/<id>")
        print(ex)


if __name__ == "__main__":
    app.run(port=8888, debug=True)
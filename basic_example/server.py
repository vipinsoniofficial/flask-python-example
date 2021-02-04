from flask import Flask
import logging

logging.basicConfig(filename='main_logs.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("In API Started")
app = Flask(__name__)

import os, json, time, re, sys
from flask import Flask, request, abort
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

import requests
import json
import hashlib
import datetime
import moment
import random
import pika
import functools
import threading
import mysql.connector

# mongoConfig = {
# 	"username": os.environ['MONGO_USERNAME'],
# 	"password": os.environ['MONGO_PASSWORD'],
# 	"server": os.environ['MONGO_HOST'],
# 	"port": os.environ['MONGO_PORT']
# }

# mysqlConfig = {
# 	"username": os.environ['MYSQL_USERNAME'],
# 	"password": os.environ['MYSQL_PASSWORD'],
# 	"database": os.environ['MYSQL_DATABASE'],
# 	"host": os.environ['MYSQL_HOST']
# }

# rabbitmqConfig = {
#     "host": os.environ['RABBITMQ_HOST'],
# 	"port": os.environ['RABBITMQ_PORT'],
#     "commentTopic": os.environ['RABBITMQ_COMMENT_TOPIC']
# }
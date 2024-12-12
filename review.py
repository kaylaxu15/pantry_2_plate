import flask
from flask import Flask, render_template, session, jsonify, request
import DatabaseClient
import pandas as pd
import numpy as np
import json
from urllib.parse import unquote
import dotenv
import auth
import os
from top import app
import cloudinary
import cloudinary.uploader
import re

# add reviews field to database
db = DatabaseClient.DatabaseClient()
users_collection = db["Users"]
users_collection.updateMany({}, {"$set":{"reviews": {}}}) 


from flask import Flask, render_template, request, redirect, url_for,Blueprint,jsonify
# from Event_Management.app import views, models, forms
import psycopg2
from Event_Management.database import *


try:
    connection = psycopg2.connect(
        user = "21CS30043",
        password = "21CS30043",
        host = "10.5.18.71",
        database = "21CS30043"
        )
    cursor = connection.cursor()
except Exception as err:
    print(f"Error: {err}") 
    
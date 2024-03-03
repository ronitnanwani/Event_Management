from flask import Flask, render_template, request, redirect, url_for,Blueprint,jsonify
# from Event_Management.app import views, models, forms
import psycopg2
from Event_Management.database import *


try:
    connection = psycopg2.connect(
        user = "postgres",
        password = "pass@1234",
        host = "localhost",
        database = "event_management"
        )
    cursor = connection.cursor()
except Exception as err:
    print(f"Error: {err}") 
    
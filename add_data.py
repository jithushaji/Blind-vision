import sqlite3
import os
from Capture_Image import *
from Train_Image import *

path='TrainingImage/'
exists=os.path.isdir(path)
if exists==False:
    os.mkdir(path)
createtable="""CREATE TABLE IF NOT EXISTS Blindvision (ID INTEGER PRIMARY KEY,Name TEXT NOT NULL);"""
connection=sqlite3.connect("Database.db")
cursor=connection.cursor()
cursor.execute(createtable)

takeImages()
TrainImages()
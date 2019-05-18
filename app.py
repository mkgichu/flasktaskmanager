from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pygal

app = Flask(__name__)

#uniform resource identifier
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://rffrvoovfekvmk:3eb746fa4ffef479c9dc20c226696cf7cdacb3a30b24d21d123f96100801b26c@ec2-23-23-92-204.compute-1.amazonaws.com:5432/d6f1ri327ml2r2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = ""
db = SQLAlchemy(app)

from models import TaskModel

@app.before_first_request
def create():
    db.create_all()


@app.route('/')
def home():
    task= TaskModel.read_all()
    # read on list comprehension
    status_list = [x.status for x in task]
    print(status_list)

    pie_chart = pygal.Pie()
    pie_chart.title = "task_status"
    pie_chart.add("completed projects", status_list.count("complete"))
    pie_chart.add("cancelled projects", status_list.count("cancelled"))
    pie_chart.add("pending projects", status_list.count("pending"))
    graph = pie_chart.render_data_uri()




    return render_template("index.html",task=task,graph = graph)

@app.route("/new", methods =['POST'])
def newTask():
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["description"]
        startdate = request.form["startdate"]
        enddate = request.form["enddate"]
        status = request.form["status"]

        task=TaskModel(title=title, description=description,startdate=startdate,enddate=enddate, status=status)
        task.insert_record()
        return redirect(url_for('home'))


@app.route("/edit/<int:id>", methods =['POST'])
def editTask(id):
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["description"]
        startdate = request.form["startdate"]
        enddate = request.form["enddate"]
        status = request.form["status"]

        TaskModel.update_by_id(id=id,title=title, description=description,startdate=startdate,enddate=enddate,status=status )
        return redirect(url_for('home'))

@app.route("/delete/<int:id>")
def deleteTask(id):
    if request.method=="GET":
        TaskModel.delete_by_id(id)
        return redirect(url_for("home"))



if __name__ == 'main':
    app.run()

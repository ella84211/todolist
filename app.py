import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, g
from functools import wraps


"""The functions and corresponding html pages for index, login, logout, and register have been adapted from my solution to the finance pset."""


app = Flask(__name__)
app.secret_key = 'LltwwctAtklsjfmayIwsllatmwmaboatpOdWwbr16814964'


# Note for myself (ignore)
"""Checklist for adding a new table (for a user):
    Add the table when they register
    Add function in app.py to display items
        Make sure, if necessary, it has @login_required
    Make html page(s) for the table
        If applicable:
            Make sure items can be starred urgent
            Make sure items can be deleted
    Add ways to get to the page from other pages
    Delete the table in delete account"""


@app.before_request
def before_request():
    g.db = sqlite3.connect('list.db')
    g.cursor = g.db.cursor()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    username = session["username"]
    if request.method == "POST":
        title = request.form.get("title")
        task = request.form.get("task")
        titlenote = request.form.get("titlenotes")
        tasknote = request.form.get("tasknotes")
        link = request.form.get("link")
        if task:
            query = f"INSERT INTO {username} (task, tasknote) values (?, ?)"
            g.cursor.execute(query, (task, tasknote))
            g.db.commit()
        if title:
            if link:
                query = f"INSERT INTO {username} (title, link, titlenote) values (?, ?, ?)"
                g.cursor.execute(query, (title, link, titlenote))
                g.db.commit()
        return redirect("/")
    else:
        titles = []
        tasks = []
        titlenotes = []
        tasknotes = []
        links = []
        urgenttitles = []
        urgenttasks = []
        urgenttitlenotes = []
        urgenttasknotes = []
        urgentlinks = []
        titlecolors = []
        taskcolors = []
        urgenttitlecolors = []
        urgenttaskcolors = []
        queryone = f"SELECT title FROM {username}"
        one = g.cursor.execute(queryone)
        title = one.fetchall()
        querytwo = f"SELECT task FROM {username}"
        two = g.cursor.execute(querytwo)
        task = two.fetchall()
        querythree = f"SELECT titlenote FROM {username}"
        three = g.cursor.execute(querythree)
        titlenote = three.fetchall()
        queryfour = f"SELECT tasknote FROM {username}"
        four = g.cursor.execute(queryfour)
        tasknote = four.fetchall()
        queryfive = f"SELECT link FROM {username}"
        five = g.cursor.execute(queryfive)
        link = five.fetchall()
        querysix = f"SELECT title FROM {username}urgent"
        six = g.cursor.execute(querysix)
        urgenttitle = six.fetchall()
        queryseven = f"SELECT task FROM {username}urgent"
        seven = g.cursor.execute(queryseven)
        urgenttask = seven.fetchall()
        queryeight = f"SELECT titlenote FROM {username}urgent"
        eight = g.cursor.execute(queryeight)
        urgenttitlenote = eight.fetchall()
        querynine = f"SELECT tasknote FROM {username}urgent"
        nine = g.cursor.execute(querynine)
        urgenttasknote = nine.fetchall()
        queryten = f"SELECT link FROM {username}urgent"
        ten = g.cursor.execute(queryten)
        urgentlink = ten.fetchall()
        queryeleven = f"SELECT titlecolor from {username}"
        eleven = g.cursor.execute(queryeleven)
        titlecolor = eleven.fetchall()
        querytwelve = f"SELECT taskcolor from {username}"
        twelve = g.cursor.execute(querytwelve)
        taskcolor = twelve.fetchall()
        querythirteen = f"SELECT titlecolor from {username}urgent"
        thirteen = g.cursor.execute(querythirteen)
        urgenttitlecolor = thirteen.fetchall()
        queryfourteen = f"SELECT taskcolor from {username}urgent"
        fourteen = g.cursor.execute(queryfourteen)
        urgenttaskcolor = fourteen.fetchall()
        urgenttitlerows = 0
        for row in urgenttitle:
            if urgenttitlenote[urgenttitlerows][0] is not None:
                urgenttitlenotes.append(urgenttitlenote[urgenttitlerows][0])
            if urgenttitle[urgenttitlerows][0] is not None:
                urgenttitles.append(urgenttitle[urgenttitlerows][0])
            if urgentlink[urgenttitlerows][0] is not None:
                if "https://" in urgentlink[urgenttitlerows][0]:
                    newlink = urgentlink[urgenttitlerows][0][8:]
                    urgentlinks.append(newlink)
                else:
                    urgentlinks.append(urgentlink[urgenttitlerows][0])
            if urgenttitlecolor[urgenttitlerows][0] is not None:
                urgenttitlecolors.append(urgenttitlecolor[urgenttitlerows][0])
            urgenttitlerows += 1
        urgenttaskrows = 0
        for row in urgenttask:
            if urgenttasknote[urgenttaskrows][0] is not None:
                urgenttasknotes.append(urgenttasknote[urgenttaskrows][0])
            if urgenttask[urgenttaskrows][0] is not None:
                urgenttasks.append(urgenttask[urgenttaskrows][0])
            if urgenttaskcolor[urgenttaskrows][0] is not None:
                urgenttaskcolors.append(urgenttaskcolor[urgenttaskrows][0])
            urgenttaskrows += 1
        titlerows = 0
        for row in title:
            if titlenote[titlerows][0] is not None:
                titlenotes.append(titlenote[titlerows][0])
            if title[titlerows][0] is not None:
                titles.append(title[titlerows][0])
            if link[titlerows][0] is not None:
                if "https://" in link[titlerows][0]:
                    newlink = link[titlerows][0][8:]
                    links.append(newlink)
                else:
                    links.append(link[titlerows][0])
            if titlecolor[titlerows][0] is not None:
                titlecolors.append(titlecolor[titlerows][0])
            titlerows += 1
        taskrows = 0
        for row in task:
            if tasknote[taskrows][0] is not None:
                tasknotes.append(tasknote[taskrows][0])
            if task[taskrows][0] is not None:
                tasks.append(task[taskrows][0])
            if taskcolor[taskrows][0] is not None:
                taskcolors.append(taskcolor[taskrows][0])
            taskrows += 1
        return render_template("index.html", titles=titles, tasks=tasks, titlenotes=titlenotes, tasknotes=tasknotes, links=links, urgenttitles=urgenttitles, urgenttasks=urgenttasks, urgenttitlenotes=urgenttitlenotes, urgenttasknotes=urgenttasknotes, urgentlinks=urgentlinks, urgenttaskcolors=urgenttaskcolors, urgenttitlecolors=urgenttitlecolors, taskcolors=taskcolors, titlecolors=titlecolors)


@app.route("/history", methods = ["GET", "POST"])
@login_required
def history():
    username = session["username"]
    titles = []
    tasks = []
    titlenotes = []
    tasknotes = []
    links = []
    queryone = f"SELECT title FROM {username}history"
    one = g.cursor.execute(queryone)
    title = one.fetchall()
    querytwo = f"SELECT task FROM {username}history"
    two = g.cursor.execute(querytwo)
    task = two.fetchall()
    querythree = f"SELECT titlenote FROM {username}history"
    three = g.cursor.execute(querythree)
    titlenote = three.fetchall()
    queryfour = f"SELECT tasknote FROM {username}history"
    four = g.cursor.execute(queryfour)
    tasknote = four.fetchall()
    queryfive = f"SELECT link FROM {username}history"
    five = g.cursor.execute(queryfive)
    link = five.fetchall()
    titlerows = 0
    for row in title:
        if titlenote[titlerows][0] is not None:
            titlenotes.append(titlenote[titlerows][0])
        if title[titlerows][0] is not None:
            titles.append(title[titlerows][0])
        if link[titlerows][0] is not None:
            if "https://" in link[titlerows][0]:
                newlink = link[titlerows][0][8:]
                links.append(newlink)
            else:
                links.append(link[titlerows][0])
        titlerows += 1
    taskrows = 0
    for row in task:
        if tasknote[taskrows][0] is not None:
            tasknotes.append(tasknote[taskrows][0])
        if task[taskrows][0] is not None:
            tasks.append(task[taskrows][0])
        taskrows += 1
    return render_template("history.html", titles=titles, tasks=tasks, titlenotes=titlenotes, tasknotes=tasknotes, links=links)


@app.route("/color", methods=["GET", "POST"])
def color():
    if request.method == "POST":
        username = session["username"]
        urgenttaskname = request.form.get("urgenttasknamecolor")
        urgenttitlename = request.form.get("urgenttitlenamecolor")
        taskname = request.form.get("tasknamecolor")
        titlename = request.form.get("titlenamecolor")
        color = request.form.get("color")
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'saddlebrown', 'grey', 'black']
        if color not in colors:
            return render_template("404.html")
        if urgenttaskname:
            query = f"UPDATE {username}urgent SET taskcolor = ? WHERE task = ?"
            g.cursor.execute(query, (color, urgenttaskname))
            g.db.commit()
        if urgenttitlename:
            query = f"UPDATE {username}urgent SET titlecolor = ? WHERE title = ?"
            g.cursor.execute(query, (color, urgenttitlename))
            g.db.commit()
        if taskname:
            query = f"UPDATE {username} SET taskcolor = ? WHERE task = ?"
            g.cursor.execute(query, (color, taskname))
            g.db.commit()
        if titlename:
            query = f"UPDATE {username} SET titlecolor = ? WHERE title = ?"
            g.cursor.execute(query, (color, titlename))
            g.db.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route("/urgent", methods=["GET", "POST"])
def urgent():
    if request.method == "POST":
        username = session["username"]
        taskname = request.form.get("taskname")
        titlename = request.form.get("titlename")
        if taskname:
            queryone = f"INSERT INTO {username}urgent SELECT * FROM {username} WHERE task = ?"
            g.cursor.execute(queryone, (taskname,))
            g.db.commit()
            querytwo = f"DELETE FROM {username} WHERE task = ?"
            g.cursor.execute(querytwo, (taskname,))
            g.db.commit()
        if titlename:
            queryone = f"INSERT INTO {username}urgent SELECT * FROM {username} WHERE title = ?"
            g.cursor.execute(queryone, (titlename,))
            g.db.commit()
            querytwo = f"DELETE FROM {username} WHERE title = ?"
            g.cursor.execute(querytwo, (titlename,))
            g.db.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route("/noturgent", methods=["GET", "POST"])
def noturgent():
    if request.method == "POST":
        username = session["username"]
        taskname = request.form.get("urgenttaskname")
        titlename = request.form.get("urgenttitlename")
        if taskname:
            queryone = f"INSERT INTO {username} SELECT * FROM {username}urgent WHERE task = ?"
            g.cursor.execute(queryone, (taskname,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}urgent WHERE task = ?"
            g.cursor.execute(querytwo, (taskname,))
            g.db.commit()
        if titlename:
            queryone = f"INSERT INTO {username} SELECT * FROM {username}urgent WHERE title = ?"
            g.cursor.execute(queryone, (titlename,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}urgent WHERE title = ?"
            g.cursor.execute(querytwo, (titlename,))
            g.db.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    username = session["username"]
    if request.method == "POST":
        tasknameadd = request.form.get("tasknameadd")
        titlenameadd = request.form.get("titlenameadd")
        if tasknameadd:
            queryone = f"INSERT INTO {username} SELECT * FROM {username}history WHERE task = ?"
            g.cursor.execute(queryone, (tasknameadd,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}history WHERE task = ?"
            g.cursor.execute(querytwo, (tasknameadd,))
            g.db.commit()
        if titlenameadd:
            queryone = f"INSERT INTO {username} SELECT * FROM {username}history WHERE title = ?"
            g.cursor.execute(queryone, (titlenameadd,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}history WHERE title = ?"
            g.cursor.execute(querytwo, (titlenameadd,))
            g.db.commit()
        return redirect("/history")
    else:
        return redirect("/history")


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    username = session["username"]
    if request.method == "POST":
        tasknameremove = request.form.get("tasknameremove")
        titlenameremove = request.form.get("titlenameremove")
        if tasknameremove:
            query = f"DELETE FROM {username}history WHERE task = ?"
            g.cursor.execute(query, (tasknameremove,))
            g.db.commit()
        if titlenameremove:
            query = f"DELETE FROM {username}history WHERE title = ?"
            g.cursor.execute(query, (titlenameremove,))
            g.db.commit()
        return redirect("/history")
    else:
        return redirect("/history")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        username = session["username"]
        urgenttaskname = request.form.get("urgenttaskname")
        urgenttitlename = request.form.get("urgenttitlename")
        taskname = request.form.get("taskname")
        titlename = request.form.get("titlename")
        if urgenttaskname:
            queryone = f"INSERT INTO {username}history SELECT * FROM {username}urgent WHERE task = ?"
            g.cursor.execute(queryone, (urgenttaskname,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}urgent WHERE task = ?"
            g.cursor.execute(querytwo, (urgenttaskname,))
            g.db.commit()
        if urgenttitlename:
            queryone = f"INSERT INTO {username}history SELECT * FROM {username}urgent WHERE title = ?"
            g.cursor.execute(queryone, (urgenttitlename,))
            g.db.commit()
            querytwo = f"DELETE FROM {username}urgent WHERE title = ?"
            g.cursor.execute(querytwo, (urgenttitlename,))
            g.db.commit()
        if taskname:
            queryone = f"INSERT INTO {username}history SELECT * FROM {username} WHERE task = ?"
            g.cursor.execute(queryone, (taskname,))
            g.db.commit()
            querytwo = f"DELETE FROM {username} WHERE task = ?"
            g.cursor.execute(querytwo, (taskname,))
            g.db.commit()
        if titlename:
            queryone = f"INSERT INTO {username}history SELECT * FROM {username} WHERE title = ?"
            g.cursor.execute(queryone, (titlename,))
            g.db.commit()
            querytwo = f"DELETE FROM {username} WHERE title = ?"
            g.cursor.execute(querytwo, (titlename,))
            g.db.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        a = g.cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = a.fetchall()
        if len(rows) != 1 or rows[0][2] != request.form.get("password"):
            return render_template("404.html")
        session["username"] = rows[0][0]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("nomatch.html")
        characters = ['(', ')', '-', "'", '"', ';', '/']
        for char in characters:
            if char in username:
                return render_template("username.html")
        a = g.cursor.execute("SELECT * FROM users WHERE lowerusername = ?", (username.lower(),))
        rows = a.fetchall()
        if len(rows) != 0:
            return render_template("usernamealreadytaken.html")
        g.cursor.execute("INSERT INTO users (username, lowerusername, password) VALUES (?, ?, ?)", (username, username.lower(), password))
        g.db.commit()
        b = g.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = b.fetchall()
        session["username"] = row[0][0]
        queryone = f"CREATE TABLE {username}(title, task, titlenote, tasknote, link, titlecolor, taskcolor)"
        g.cursor.execute(queryone)
        g.db.commit()
        querytwo = f"CREATE TABLE {username}urgent(title, task, titlenote, tasknote, link, titlecolor, taskcolor)"
        g.cursor.execute(querytwo)
        g.db.commit()
        querythree = f"CREATE TABLE {username}history(title, task, titlenote, tasknote, link, titlecolor, taskcolor)"
        g.cursor.execute(querythree)
        g.db.commit()
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/deleteaccount")
@login_required
def deleteaccount():
    return render_template("/deleteaccount.html")


@app.route("/deleteaccountfinal")
@login_required
def deleteaccountfinal():
    username = session["username"]
    queryone = f"DROP TABLE {username}"
    g.cursor.execute(queryone)
    g.db.commit()
    querytwo = f"DROP TABLE {username}history"
    g.cursor.execute(querytwo)
    g.db.commit()
    querythree = f"DROP TABLE {username}urgent"
    g.cursor.execute(querythree)
    g.db.commit()
    queryfour = f"DELETE FROM users WHERE username = '{username}'"
    g.cursor.execute(queryfour)
    g.db.commit()
    session.clear()
    return redirect("/")
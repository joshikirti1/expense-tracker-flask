from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kirti@123",
    database="expense_tracker"
)

@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()
        cursor.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect("/dashboard")
        else:
            return "Invalid email or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM expenses WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    expenses = cursor.fetchall()
    cursor.close()

    return render_template("dashboard.html", name=session["user_name"], expenses=expenses)

@app.route("/add-expense", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]
    expense_date = request.form["expense_date"]

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, title, amount, category, expense_date) VALUES (%s, %s, %s, %s, %s)",
        (session["user_id"], title, amount, category, expense_date)
    )
    db.commit()
    cursor.close()

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id):
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM expenses WHERE id=%s AND user_id=%s",
        (expense_id, session["user_id"])
    )
    db.commit()
    cursor.close()

    return redirect("/dashboard")

@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if "user_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]

        cursor.execute(
            "UPDATE expenses SET title=%s, amount=%s, category=%s, expense_date=%s WHERE id=%s AND user_id=%s",
            (title, amount, category, expense_date, expense_id, session["user_id"])
        )
        db.commit()
        cursor.close()
        return redirect("/dashboard")

    # GET request: fetch existing expense
    cursor.execute(
        "SELECT * FROM expenses WHERE id=%s AND user_id=%s",
        (expense_id, session["user_id"])
    )
    expense = cursor.fetchone()
    cursor.close()

    if not expense:
        return redirect("/dashboard")

    return render_template("edit_expense.html", expense=expense)

if __name__ == "__main__":
    app.run(debug=True)
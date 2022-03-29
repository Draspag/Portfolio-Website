import os
from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
import smtplib, ssl

from flask import Flask

app = Flask(__name__)
Bootstrap(app)


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
# Create a secure SSL context

sender_email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = f"Subject: {request.form.get('subject')} \n\n " \
                  f"Email: {request.form.get('email')}" \
                  f"Name: {request.form.get('name')} \n" \
                  f"{request.form.get('message')}"

        receiver_email = request.form.get('email')

        # context = ssl.create_default_context()
        with smtplib.SMTP(host=smtp_server, port=port) as connection:
            connection.starttls()
            connection.login(sender_email, password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=sender_email,
                                msg=message)

        return render_template("index.html", submitted=True)
    return render_template("index.html", submitted=False)

if __name__ == "__main__":
    app.run(debug=True)
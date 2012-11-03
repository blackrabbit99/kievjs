from flask import Flask, redirect, url_for, flash, render_template

from db import mongo_init

import settings

app = Flask(__name__)
app.config.from_object(settings)

CAMPAIGNS = getattr(settings, "CAMPAIGNS", {})


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/confirm/<campaign>/<code>/')
def confirm(campaign, code):
    if CAMPAIGNS.get(campaign) is None:
        flash("Sorry, campaign not found", "alert-error")
        return redirect(url_for("index"))

    users = mongo_init().users
    campaign = CAMPAIGNS.get(campaign)

    user = users.find_one({"internalid": code})

    if not user:
        flash("Sorry, can't find such user", "alert-error")
        return redirect(url_for("index"))

    user[campaign] = "confirmed"
    users.save(user)

    flash(
        "You're successfully confirmed in current campaign",
        "alert-success")
    return redirect(url_for("index"))


def main():
    app.run()


if __name__ == '__main__':
    main()

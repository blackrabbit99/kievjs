from flask import Flask, redirect, url_for, flash, render_template

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

    # TODO: read user from mongo
    # TODO: mark as confirmed in provided campaign

    flash(
        "You're successfully confirmed in current campaign",
        "alert-success")
    return redirect(url_for("index"))


def main():
    app.run()


if __name__ == '__main__':
    main()

from flask import Blueprint, render_template, url_for, flash, redirect

main = Blueprint('main', __name__)

@main.route('/')
def home():

    return render_template("main/home.html", title="Home")
from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from APP.models import User, Log
from flask_login import current_user, login_required
from APP.logApp.forms import LogForm
from APP import db

logApp = Blueprint('logApp', __name__)

@logApp.route('/logApp')
@login_required
def logApp_page():
    page = request.args.get('page', 1, type=int)
    logs = Log.query.order_by(Log.event_datetime.desc()).paginate(page=page, per_page=5)
    return render_template("logApp/logApp.html", title="logApp", logs=logs)

@logApp.route('/logApp/new', methods=['GET', 'POST'])
@login_required
def logApp_new():
    form = LogForm()
    if form.validate_on_submit():
        #Add Log to database#
        log = Log(comment=form.comment.data, location=form.location.data, author=current_user)
        db.session.add(log)
        db.session.commit()

        flash('Your log has been created', 'success')
        return redirect(url_for('logApp.logApp_page'))
    return render_template('logApp/log_new.html', title="New Log", form=form)

@logApp.route('/logApp/update/<log_id>', methods=['GET', 'POST'])
@login_required
def logApp_update(log_id):
    # check to make sure log_id exists #
    log = Log.query.get_or_404(log_id)
    if log.author != current_user:
        abort(403)

    form = LogForm()
    if form.validate_on_submit():
        log.comment = form.comment.data
        log.location = form.location.data
        db.session.commit()
        flash("This log has been updated", 'success')
        return redirect(url_for('logApp.logApp_page'))
    elif request.method == 'GET':
        form.comment.data = log.comment
        form.location.data = log.location

    return render_template('logApp/log_update.html', title='Update Log', form=form)

@logApp.route('/logApp/delete/<log_id>', methods=['POST'])
@login_required
def logApp_delete(log_id):
    log = Log.query.get_or_404(log_id)
    if log.author != current_user:
        abort(403)
    db.session.delete(log)
    db.session.commit()
    flash("Your log has been deleted", 'success')
    return redirect(url_for('logApp.logApp_page'))

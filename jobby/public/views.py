from flask import render_template, Blueprint, request, redirect, url_for, abort, flash, jsonify
from flask_login import current_user
from sqlalchemy import or_, and_
from jobby.models import (
    Tasks, Bids, Users,
    WorkExperiences, Educations,
    Views, Notification, Reviews, Offers,
    Notification, TaskSkills, Skills
    )
from jobby import db
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid, os, json
from utils import allowed_offer_file, get_extension, UPLOAD_OFFER_FOLDER, get_category, send_email

public = Blueprint('public',__name__)

@public.route('/')
def index():
    return render_template('public/index.html')

@public.route('/search/<where>', methods=['GET','POST'])
def search(where):
    if where == 'index':
        keyword = request.form['keyword'] or None
        location = request.form['location'] or None
        category = request.form['category'] or None

        return redirect(url_for('.browseTasks', lc=location, kw=keyword, ct=category))
    elif where == 'tasklist':
        keyword = request.form['task_search'] or None
        location = request.form['location'] or None
        category = request.form['category'] or None
        budget_min = request.form['budget_min'] or None
        budget_max = request.form['budget_max'] or None
        checks = request.form.getlist('flexRadioDefault')

        return redirect(url_for('.browseTasks', lc=location, kw=keyword, ct=category,
            bn=budget_min, bx=budget_max, cx=checks))

    elif where == 'freelist':
        keyword = request.form['free_search'] or None
        location = request.form['location'] or None
        category = request.form['category'] or None
        skill = request.form['skill'] or None
        rating = request.form.getlist('rating')
        print(rating)

        return redirect(url_for('.browseFreelancers', lc=location, kw=keyword, ct=category, rt=rating, sk=skill))

@public.route('/project/<task_url>', methods=['GET', 'POST'])
def task_page(task_url):
    task_id = task_url.split('-')[-1]
    task = Tasks.query.filter_by(id=task_id).first_or_404()
    category = get_category(task.category)
    if request.method == 'GET':
        task.addView()
        sk = TaskSkills.query.filter_by(task_id=task.id).all()
        return render_template('tasks/single-task-page.html',task=task, sk=sk, category=category)
    else:
        bid_amount = request.form['bid_amount']
        qtyInput = request.form['qtyInput']
        qtyOption = request.form['qtyOption']
        bidMessage = request.form['bidMessage']

        bid = Bids(bid_amount=bid_amount, num_delivery=qtyInput, type_delivery=qtyOption,
            message=bidMessage, user_id=current_user.id, task_id=task_id)
        notification = Notification(task_id=task_id, not_from=current_user.id, not_to=task.poster.id, not_type=1)
        task.num_bids += 1
        current_user.num_bids += 1
        db.session.add(bid)
        db.session.add(notification)
        db.session.commit()
        return jsonify({'success': True, 'msg': url_for('manage.activeBids')})

@public.route('/projects')
def browseTasks():
    keyword = request.args.get('kw', type=str)
    location = request.args.get('lc', type=str)
    category = request.args.get('ct', type=str)
    budget_min = request.args.get('bn', type=str)
    budget_max = request.args.get('bx', type=str)
    checks = request.args.get('cx', type=str)
    tag = request.args.get('tag', type=str)
    page = request.args.get('page', type=int)
    str_cat = get_category(request.args.get('ct', type=str))

    if request.args:
        tasks = db.session.query(Tasks)

        if keyword:
            tasks = Tasks.query.whoosh_search(keyword)

        if tag:
            tasks = tasks.filter(Tasks.TSkills.any(TaskSkills.skill==tag))

        if checks:
            if checks == 'lasthour':
                lasthour = datetime.now() - timedelta(hours = 1)
                print(lasthour)
                tasks = tasks.filter(Tasks.time_posted >= lasthour)
            elif checks == 'oneday':
                oneday = datetime.now() - timedelta(1)
                tasks = tasks.filter(Tasks.time_posted >= oneday)
            elif checks == 'threedays':
                threedays = datetime.now() - timedelta(3)
                tasks = tasks.filter(Tasks.time_posted >= threedays)
            elif checks == 'sevendays':
                sevendays = datetime.now() - timedelta(7)
                tasks = tasks.filter(Tasks.time_posted >= sevendays)
            else:
                fourteendays = datetime.now() - timedelta(14)
                tasks = tasks.filter(Tasks.time_posted >= fourteendays)

        if location:
            tasks = tasks.filter(Tasks.location==location)
        if category:
            tasks = tasks.filter(Tasks.category==category)
        if budget_min:
            tasks = tasks.filter(Tasks.budget_min >= int(budget_min))
        if budget_max:
            tasks = tasks.filter(Tasks.budget_max <= int(budget_max))

        if keyword:
            tasks = tasks.paginate(page=page, per_page=10)
        else:
            tasks = tasks.paginate(page=page, per_page=4)
    else:
        tasks = Tasks.query.paginate(page=page, per_page=4)
    return render_template('public/tasks-list.html', tasks=tasks,
        kw=keyword, lc=location, ct=category, str_cat=str_cat,
        bn=budget_min, bx=budget_max, cx=checks, tag=tag)

@public.route('/freelancer/<int:user_id>', methods=['GET', 'POST'])
def freelancer(user_id):
    user = Users.query.filter_by(id=user_id, status='freelancer').first_or_404()
    if request.method == 'GET':
        user.addView()
        return render_template('public/freelancer-profile.html', user=user)
    else:
        offer = Offers(offered=user, offers=current_user)
        offer.subject = request.form['subject']
        offer.message = request.form['offerMessage']
        offer.offered_task = int(request.form['offeredTask'])
        if 'formFile' in request.files:
            file = request.files['formFile']
            filename = file.filename
            if allowed_offer_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                offer.filename = unique_filename
                file.save(os.path.join(UPLOAD_OFFER_FOLDER, unique_filename))

        notif = Notification(notification_from=current_user, notification_to=user, not_type=4)
        db.session.add(offer)
        db.session.add(notif)
        db.session.commit()
        flash('Your offer has been succesfully sent!')
        return redirect(request.url)

@public.route('/freelancers')
def browseFreelancers():
    keyword = request.args.get('kw', type=str)
    location = request.args.get('lc', type=str)
    category = request.args.get('ct', type=str)
    rating = request.args.get('rt', type=str)
    skill = request.args.get('sk', type=str)
    tag = request.args.get('tag', type=str)
    page = request.args.get('page', type=int)
    str_cat = get_category(request.args.get('ct', type=str))
    freelancers = db.session.query(Users).filter(Users.status=='freelancer')

    if request.args:
        if keyword:
            freelancers = Users.query.whoosh_search(keyword).filter(Users.status=='freelancer')

        if tag:
            freelancers = freelancers.filter(Users.UserSkills.any(Skills.skill==tag))

        if rating:
            freelancers = freelancers.filter(Users.rating >= float(rating))

        if location:
            freelancers = freelancers.filter(Users.country==location)

        if category:
            freelancers = freelancers.filter(Users.field_of_work==category)

        if skill:
            freelancers = freelancers.filter(Users.UserSkills.any(Skills.skill==skill))

        if keyword:
            freelancers = freelancers.paginate(page=page, per_page=10)
        else:
            freelancers = freelancers.paginate(page=page, per_page=4)
    else:
        freelancers = freelancers.paginate(page=page, per_page=4)
    return render_template('public/freelancers-list.html', freelancers=freelancers,
        kw=keyword, lc=location, ct=category, str_cat=str_cat,
        rt=rating, sk=skill, tag=tag, page=page)

@public.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('public/contact.html')
    else:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        comment = request.form['comment']
        honey = request.form['honey']
        if honey: #honeypot field for spam bots sending emails. If its filled don't send email.
            flash('something went wrong try again')
            return render_template('public/contact.html')
        else:
            send_email(name, email, subject, comment)
            flash("Thanks. Your message has been sent.")
            return redirect(request.url)

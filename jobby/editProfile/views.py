from flask import render_template, Blueprint, request, flash, redirect, url_for, abort, jsonify
from flask_login import current_user, login_required
from jobby.models import Users, Skills, WorkExperiences, Educations
from jobby import db, last_updated, csrf
import os, uuid, re, json, bleach
from PIL import Image
from utils import crop_max_square, allowed_img_file, get_extension, UPLOAD_IMG_FOLDER
from werkzeug.utils import secure_filename

editProfile = Blueprint('editProfile',__name__)

@editProfile.route('/editProfile', methods=['POST'])
@login_required
def editProfile_personel():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone_number = request.form['phone_number']

    if len(name) < 3 or len(name) > 30 or len(surname) < 3 or len(surname) > 30:
        flash("The length of name and surname should be between 3 and 30")
        return redirect(request.url)

    if len(email) > 50:
        flash("Incorrect Email!")
        return redirect(request.url)

    if email != current_user.email:
        flash("Confirmation email has been sent!")

    current_user.name = name
    current_user.surname = surname
    current_user.email = email
    current_user.phone_number = phone_number

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            current_user.profile_picture = unique_filename
            image = Image.open(file)
            i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
            i.save(os.path.join(UPLOAD_IMG_FOLDER, unique_filename), quality=95)
    db.session.commit()
    return redirect(request.url)

@editProfile.route('/editProfile/profile', methods=['POST'])
@login_required
def editProfile_profile():
    data = request.get_json(force=True)
    current_user.field_of_work = data['field_of_work']
    current_user.tagline = data['tagline']
    current_user.country = data['location']
    current_user.introduction = bleach.clean(data['introduction'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    current_user.check_status()
    db.session.commit()
    return jsonify({"success": True, "editProfileType": "p"})

@editProfile.route('/editProfile/skill', methods=['POST'])
@login_required
def editProfile_skill():
    data = request.get_json(force=True)
    skill = data['skill']
    level = data['level']
    new_skill = Skills(skill=skill, level=level, user_id=current_user.id)
    db.session.add(new_skill)
    db.session.commit()
    current_user.check_status()
    return jsonify({"success": True, "editProfileType": 's', "skill_id": new_skill.id, "skill": new_skill.skill, 'level': new_skill.level})

@editProfile.route('/editProfile/workExp', methods=['POST'])
@login_required
def editProfile_workExp():
    data = request.get_json(force=True)
    description = bleach.clean(data['desc_work'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    workExp = WorkExperiences(position=data['position'], company=data['company'], start_month=data['start_month_job'],
        start_year=data['start_year_job'], end_month=data['end_month_job'], end_year=data['end_year_job'],
        description=description, user_id=current_user.id)
    db.session.add(workExp)
    db.session.commit()
    return jsonify({"success": True, "editProfileType": 'w', 'workExp_id': workExp.id, "workExp": workExp.position, 'company': workExp.company})

@editProfile.route('/editProfile/education', methods=['POST'])
@login_required
def editProfile_education():
    data = request.get_json(force=True)
    description = bleach.clean(data['desc_edu'], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])
    edu = Educations(field=data['field'], school=data['school'], start_month=data['start_month_edu'],
        start_year=data['start_year_edu'], end_month=data['end_month_edu'], end_year=data['end_year_edu'],
        description=description, user_id=current_user.id)
    db.session.add(edu)
    db.session.commit()
    return jsonify({"success": True, "editProfileType": 'e', "edu_id": edu.id, "field": edu.field, 'school': edu.school})

@editProfile.route('/editProfile/social', methods=['POST'])
@login_required
def editProfile_social():
    data = request.get_json(force=True)

    current_user.facebook = data['facebook']
    current_user.twitter = data['twitter']
    current_user.instagram = data['instagram']
    current_user.github = data['github']
    current_user.youtube = data['youtube']
    current_user.linkedin = data['linkedin']

    db.session.commit()

    return jsonify({"success": True, 'editProfileType': 'so'})

@editProfile.route('/deleteItem', methods=['POST'])
@login_required
def deleteItem():
    data = request.get_json(force=True)
    itemType, itemId = data['type_id'].split('_')
    if itemType == 'w':
        item = WorkExperiences.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'w'})
    elif itemType == 's':
        item = Skills.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        current_user.check_status()
        db.session.commit()
        return jsonify({"success": True, 'currentField': 's'})
    elif itemType == 'e':
        item = Educations.query.filter_by(id=itemId, user_id=current_user.id).first()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"success": True, 'currentField': 'e'})

@editProfile.route('/editProfile')
@login_required
def editProfile_page():
    skills = Skills.query.filter_by(user_id=current_user.id).all()
    workExps = WorkExperiences.query.filter_by(Worker=current_user).all()
    edus = Educations.query.filter_by(student=current_user).all()
    return render_template('editProfile/editProfile.html', last_updated=last_updated, skills=skills,
        workExps=workExps, edus=edus)

@editProfile.app_errorhandler(413)
def file_too_large(e):
    flash('The file size is too big! At most 2Mb.')
    return redirect(request.url)

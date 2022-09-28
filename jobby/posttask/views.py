from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from jobby import db, last_updated
from jobby.models import Users, Tasks, TaskSkills
import bleach, uuid, os
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
from utils import allowed_img_file, get_extension, UPLOAD_TASK_FOLDER, crop_max_square

posttask = Blueprint('posttask',__name__)

@posttask.route('/posttask', methods=['GET', 'POST'])
@login_required
def post_task():
    if request.method == 'POST':
        project_name = request.form["project_name"].capitalize()
        location = request.form["location"]
        budget_min = request.form["budget_min"] or 0
        budget_max = request.form["budget_max"] or 0
        category = request.form["category"]
        skills_list = request.form.getlist('skills_list')[0].split(',')

        if len(skills_list) > 5 or len(skills_list) < 1:
            return jsonify({'success': False, 'msg': 'Add at least 1 at most 5 skills!'})

        description = bleach.clean(request.form["description"], tags=bleach.sanitizer.ALLOWED_TAGS+['u', 'br', 'p'])

        task = Tasks(project_name=project_name, location=location, budget_min=budget_min, time_posted=datetime.now(),
                     budget_max=budget_max, category=category, description=description, user_id=current_user.id)

        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename
            if allowed_img_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                task.task_pic = unique_filename
                image = Image.open(file)
                i = crop_max_square(image).resize((356, 200), Image.LANCZOS)
                i.save(os.path.join(UPLOAD_TASK_FOLDER, unique_filename), quality=95)
            else:
                return jsonify({'success': False, 'msg': 'Allowed image files jpeg, png, jpg'})
        else:
            return jsonify({'success': False, 'msg': 'Please add an image relevant to your project!'})

        db.session.add(task)
        db.session.commit()

        for skill in skills_list:
            tskills = TaskSkills(skill=skill.capitalize(), task_id=task.id)
            db.session.add(tskills)
        db.session.commit()
        return jsonify({'success': True, 'msg': url_for('public.task_page', task_url=task.generate_task_link())})
    else:
        if not current_user.email_approved:
            flash('Your email has not been confirmed yet. You cannot post a project!')
        return render_template('tasks/post-a-task.html', last_updated=last_updated)

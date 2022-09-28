import sys
import os
sys.path.append(os.path.dirname(__file__))

from jobby import create_app, socketio
from flask import abort
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib import sqla
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from jobby.models import (
    Users, Tasks, Bids, Skills,
    Messages, WorkExperiences,
    Educations, Views, Notification,
    Reviews, Offers, TaskSkills
    )
from jobby import db
import flask_whooshalchemy as wa

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            abort(404)
        if current_user.is_authenticated and current_user.email == "anakutdigital@gmail.com":
          return True

        # if current_user.is_authenticated:
        #     return True

        return abort(404)

    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(MyModelView):
    column_editable_list = ['email', 'name', 'surname']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list

class EduView(MyModelView):
    column_editable_list = ['field', 'school']
    column_searchable_list = column_editable_list
    column_filters = column_editable_list

class TaskView(MyModelView):
    column_editable_list = ['project_name', 'category']
    column_searchable_list = column_editable_list
    column_filters = column_editable_list

class WorkExpView(MyModelView):
    column_editable_list = ['position', 'company']
    column_searchable_list = column_editable_list
    column_filters = column_editable_list

app = create_app()
wa.whoosh_index(app, Tasks)
wa.whoosh_index(app, Users)

admin = Admin(
    app,
    'My Dashboard',
    template_mode='bootstrap3',
)
admin.add_view(UserView(Users, db.session))
admin.add_view(TaskView(Tasks, db.session))
admin.add_view(EduView(Educations, db.session))
admin.add_view(WorkExpView(WorkExperiences, db.session))
admin.add_view(MyModelView(Notification, db.session))
admin.add_view(MyModelView(Bids, db.session))
admin.add_view(MyModelView(Reviews, db.session))
admin.add_view(MyModelView(Messages, db.session))
admin.add_view(MyModelView(TaskSkills, db.session))
admin.add_view(MyModelView(Offers, db.session))
admin.add_view(MyModelView(Views, db.session))

if __name__ == '__main__':
    socketio.run(app, debug=True)

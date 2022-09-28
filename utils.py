# !/usr/bin/python
import os
import sys
import os
sys.path.append(os.path.dirname(__file__))
from flask_mail import Message

from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail
mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(name, email, subject, message):
    app = current_app._get_current_object()
    msg = Message(subject='Jobby Contact',
        sender="your sender email here",
        recipients=["your email here"])
    msg.body = "name: {}, email: {}, subject: {}, message: {}".format(name, email, subject, message)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def send_confirmation_email(user):
    app = current_app._get_current_object()
    token = user.get_confirmation_token()
    msg = Message(subject='Confirmation email',
        sender="your sender email here",
        recipients=[user.email])
    msg.html = render_template('account/email_confirmation.html', token=token, name=user.name)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def dir_last_updated(folder):
    return ""
        # str(max(os.path.getmtime(os.path.join(root_path, f))
        # for root_path, dirs, files in os.walk(folder)
        # for f in files))

ALLOWED_IMG_EXTENSIONS = {'jpeg', 'jpg', 'png'}
ALLOWED_OFFER_EXTENSIONS = {'docx', 'doc', 'pdf'}

UPLOAD_IMG_FOLDER = os.path.join(os.getcwd(), 'jobby/static/images')
UPLOAD_TASK_FOLDER = os.path.join(os.getcwd(), 'jobby/static/images/taskpics')
UPLOAD_OFFER_FOLDER = os.path.join(os.getcwd(), 'jobby/static/files')

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def allowed_offer_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_OFFER_EXTENSIONS

def get_extension(filename):
    return '.'+ filename.rsplit('.', 1)[1].lower()

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def get_category(categor_num):
    categories = {
        '1': 'Programming',
        '2': 'Writing',
        '3': 'Graphics Design',
        '4': 'Digital Marketing',
        '5': 'Data Science',
        '6': 'Video & Animation',
        '7': 'Lifestyle',
        '8': 'Finance',
        '9': 'Other'
    }

    return categories.get(categor_num)

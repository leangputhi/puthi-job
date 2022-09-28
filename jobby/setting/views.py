from flask import render_template, Blueprint, request, url_for, jsonify
from flask_login import current_user, login_required
from jobby import db, last_updated
from werkzeug.security import check_password_hash, generate_password_hash

setting = Blueprint('setting',__name__)

@setting.route('/setting/security', methods=['POST'])
@login_required
def setting_security():
    data = request.get_json(force=True)
    password = data['password']
    new_password = data['new_password']
    confirm_password = data['confirm_password']
    if len(new_password.strip()) < 6 or new_password != confirm_password or not check_password_hash(current_user.password, password):
        return jsonify({"success": False, "msg": "Some thing went wrong. Reason might be your password length is less than 6, or passwords didn't match or your password is not on our systems!"})
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        return jsonify({"success": True, "msg": "Your password has been changed!"})


@setting.route('/setting')
@login_required
def setting_page():
    return render_template('setting/settings.html', last_updated=last_updated)

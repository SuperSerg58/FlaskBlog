from flask import Blueprint, render_template
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')  # имя_сайта/users/login


@blueprint.route('')
@admin_required
def admin_index():
    title = 'Admin Panel'
    return render_template('admin/admin.html', title=title)

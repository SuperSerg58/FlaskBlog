from flask import Blueprint
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')  # имя_сайта/users/login


@blueprint.route('')
@admin_required
def admin_index():
    return 'Hello Admin'

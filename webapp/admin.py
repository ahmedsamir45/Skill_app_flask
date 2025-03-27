from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from webapp import bcrypt
from flask_login import current_user

admin_page=Blueprint("admin_page",__name__)


class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8)"
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
        # return True


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
        # return True


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
        # return True
    
class SkillsModelView(ModelView):
    column_list = ['id', 'title', 'prog', 'desc', 'user_id']
    form_columns = ['title', 'prog', 'desc', 'user_id']
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

class JobsModelView(ModelView):
    column_list = ['id', 'title', 'company', 'posted_by', 'date_posted', 'deadline']
    column_searchable_list = ['title', 'company']
    column_filters = ['type', 'company']
    form_columns = ['title', 'type', 'company', 'company_url', 'description', 
                   'skills_required', 'link_to_apply', 'deadline', 'posted_by']
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

from webapp.models import Skills
from flask import render_template ,url_for,flash ,redirect,request,Blueprint
from webapp.forms import AddForm,DeleteForm,UpdateForm
from webapp import db
from flask_login import current_user,login_required


skill_pages=Blueprint("skill_pages",__name__)


@skill_pages.route("/skills")
@login_required
def skills():
    skills=Skills.query.filter_by(user_id=current_user.id)
    length = len(list(skills))
    return render_template('skills.html',pagetitle='Skillspage',page_head='My Skills',description='This Skills Page',skills = skills,custom = 'skills',js="main2",length=length)


@skill_pages.route("/delete",methods=['GET','POST'])
@login_required
def delete():
    form= DeleteForm()
    
    skills=Skills.query.filter_by(user_id=current_user.id)
    skills2=Skills.query.filter_by(user_id=current_user.id).all()
    if len(skills2)!=0:
        if form.validate_on_submit():
            skill_d = request.form.get('my-skills')

            skill=Skills.query.filter_by(user_id=current_user.id,title=skill_d).first()
            db.session.delete(skill)
            db.session.commit()
            flash(f"Skill deleted successfully for {skill.title}", "success")
            return redirect(url_for("skills"))
    else:
        flash(f"You do not have skills", category='info')
        return redirect(url_for("skills"))
    return render_template('delete.html',custom='delete',skills=skills ,form=form)

@skill_pages.route("/update",methods=['GET','POST'])
@login_required
def update():
    form= UpdateForm()
    
    skills=Skills.query.filter_by(user_id=current_user.id)
    skills2=Skills.query.filter_by(user_id=current_user.id).all()
    if len(skills2)!=0:
        if form.validate_on_submit():
            skill_u = request.form.get('my-skills')
            progress =  form.skillProg.data

            skill=Skills.query.filter_by(user_id=current_user.id,title=skill_u).first()
            skill.prog = progress
            db.session.commit()
            flash(f" Progress of Skill  updated successfully for {skill_u}", "success")
            return redirect(url_for("skills"))
    else:
        flash(f"You do not have skills", category='info')
        return redirect(url_for("skills"))
    
    return render_template('update.html',custom='update',skills=skills ,form=form)




@skill_pages.route("/add",methods=['GET','POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        skill = Skills(title=form.title.data, user_id=current_user.id, prog=form.skillProg.data, desc=form.desc.data)
        db.session.add(skill)
        db.session.commit()
        flash(f"Skill added successfully for {form.title.data}", "success")
        return redirect(url_for("skills"))
    return render_template('add.html',custom='add',form=form)



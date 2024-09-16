from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .settings.db import db
from sqlalchemy import text
from werkzeug.security import generate_password_hash
import urllib.request
import shutil

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/projectteam', methods=['GET', 'POST'])
@login_required
def projectteam():

    session = db.session

    if request.method == 'POST': 
        project_search = request.form.get('project_search') 
        if len(project_search) < 1:             # type: ignore
            return redirect(url_for('views.projectteam'))
        else:
            query = text("""
                SELECT ptm.project_team_id, prj.project_name, usr.first_name, 
                       CASE WHEN ptm.st_user_leader = 1 THEN 'X' ELSE '' END as st_user_leader
                FROM app.project prj
                JOIN app.project_team ptm ON prj.project_id = ptm.project_id
                JOIN app.user usr ON usr.id = ptm.user_id
                WHERE UPPER(prj.project_name) LIKE UPPER(:search_term)
                ORDER BY prj.project_name ASC, ptm.st_user_leader DESC, usr.first_name ASC
            """)
            result = session.execute(query, {'search_term': f"%{project_search}%"})
            data = result.fetchall()
            return render_template("projectteam.html", output_data=data, user=current_user)  
    else:
        query = text("""
            SELECT ptm.project_team_id, prj.project_name, usr.first_name, 
                   CASE WHEN ptm.st_user_leader = 1 THEN 'X' ELSE '' END as st_user_leader
            FROM app.project prj
            JOIN app.project_team ptm ON prj.project_id = ptm.project_id
            JOIN app.user usr ON usr.id = ptm.user_id
            ORDER BY prj.project_name ASC, ptm.st_user_leader DESC, usr.first_name ASC
        """)
        result = session.execute(query)
        data = result.fetchall()
        return render_template("projectteam.html", output_data=data, user=current_user)

@views.route('/modifyuser', methods=['GET', 'POST'])
@login_required
def modifyuser():
    session = db.session

    if request.method == 'POST': 
        username_search = request.form.get('username_search')
        if len(username_search) < 1: # type: ignore
            query = text("SELECT id, first_name, email, user_type_id FROM app.user ORDER BY first_name")
            result = session.execute(query)
            data = result.fetchall()
            return render_template("modifyuser.html", output_data=data, user=current_user)
        else:
            query = text("""
                SELECT id, first_name, email, user_type_id 
                FROM app.user 
                WHERE UPPER(first_name) LIKE UPPER(:search_term)
                ORDER BY first_name
            """)
            result = session.execute(query, {'search_term': f"%{username_search}%"})
            data = result.fetchall()
            return render_template("modifyuser.html", output_data=data, user=current_user)
    else:
        query = text("SELECT id, first_name, email, user_type_id FROM app.user ORDER BY first_name")
        result = session.execute(query)
        data = result.fetchall()
        return render_template("modifyuser.html", output_data=data, user=current_user)
@views.route('/usertype', methods=['GET', 'POST'])
@login_required
def usertype():
    session = db.session
    
    if request.method == 'POST': 
        usertype_search = request.form.get('usertype_search')
        if len(usertype_search) < 1:     # type: ignore
            query = text("SELECT * FROM app.user_type ORDER BY user_type_name")
            result = session.execute(query)
            data = result.fetchall()
            return render_template("usertype.html", output_data=data, user=current_user)     
        else:
            query = text("""
                SELECT * FROM app.user_type 
                WHERE UPPER(user_type_name) LIKE UPPER(:search_term) 
                ORDER BY user_type_name
            """)
            result = session.execute(query, {'search_term': f"%{usertype_search}%"})
            data = result.fetchall()
            return render_template("usertype.html", output_data=data, user=current_user)  
    else:                  
        query = text("SELECT * FROM app.user_type ORDER BY user_type_name")
        result = session.execute(query)
        data = result.fetchall()
        return render_template("usertype.html", output_data=data, user=current_user)

@views.route('/researchline', methods=['GET', 'POST'])
@login_required
def researchline():
    session = db.session
    
    if request.method == 'POST':
        researchline_search = request.form.get('researchline_search')
        if len(researchline_search) < 1:     # type: ignore
            query = text("SELECT * FROM app.research_line ORDER BY research_line_name")
            result = session.execute(query)
            data = result.fetchall()
            return render_template("researchline.html", output_data=data, user=current_user)     
        else:
            query = text("""
                SELECT * FROM app.research_line 
                WHERE UPPER(research_line_name) LIKE UPPER(:search_term) 
                ORDER BY research_line_name
            """)
            result = session.execute(query, {'search_term': f"%{researchline_search}%"})
            data = result.fetchall()
            return render_template("researchline.html", output_data=data, user=current_user)        
    else:
        query = text("SELECT * FROM app.research_line ORDER BY research_line_name")
        result = session.execute(query)
        data = result.fetchall()
        return render_template("researchline.html", output_data=data, user=current_user)


@views.route('/usertypedata', methods=['GET', 'POST']) # type: ignore
@login_required
def usertypedata():
    session = db.session
    
    if request.method == 'POST':
        user_type_id = request.form.get("user_type_id")
        user_type_name = request.form.get("user_type_name")

        if request.args.get('type_operation', '') == 'D':
            user_user_type_count = session.execute(
                text("SELECT count(0) FROM app.user WHERE user_type_id = :user_type_id"),
                {'user_type_id': user_type_id}
            ).scalar()

            if user_user_type_count > 0: # type: ignore
                flash('There are users using this user type!', category='error')
                return redirect(url_for('views.usertype'))
            else:
                session.execute(
                    text("DELETE FROM app.user_type WHERE user_type_id = :user_type_id"),
                    {'user_type_id': user_type_id}
                )
                session.commit()
                flash('Data deleted!', category='success')
                return redirect(url_for('views.usertype'))

        if request.args.get('type_operation', '') == 'A':
            session.execute(
                text("INSERT INTO app.user_type (user_type_name) VALUES (:user_type_name)"),
                {'user_type_name': user_type_name}
            )
            session.commit()
            flash('Data inserted!', category='success')
            return redirect(url_for('views.usertype'))

        if request.args.get('type_operation', '') == 'U':
            session.execute(
                text("UPDATE app.user_type SET user_type_name = :user_type_name WHERE user_type_id = :user_type_id"),
                {'user_type_name': user_type_name, 'user_type_id': user_type_id}
            )
            session.commit()
            flash('Data updated!', category='success')
            return redirect(url_for('views.usertype'))

        query = text("SELECT * FROM app.user_type ORDER BY user_type_name")
        data = session.execute(query).fetchall()
        return render_template("usertype.html", output_data=data, user=current_user)

    if request.method == 'GET':
        user_type_id = request.args.get('user_type_id', '')
        user_type_name = request.args.get('user_type_name', '')

        type_operation = 'Delete' if request.args.get('type_operation', '') == 'D' else 'Update' if request.args.get('type_operation', '') == 'U' else 'Add'

        query = text("SELECT user_type_id, user_type_name FROM app.user_type ORDER BY user_type_name")
        data_user_type = session.execute(query).fetchall()

        return render_template("usertypedata.html", user=current_user, user_type_id=user_type_id, user_type_name=user_type_name, usertype_list=data_user_type, type_operation=type_operation)


@views.route('/researchlinedata', methods=['GET', 'POST']) # type: ignore
@login_required
def researchlinedata():
    session = db.session
    
    if request.method == 'POST':
        research_line_id = request.form.get("research_line_id")
        research_line_name = request.form.get("research_line_name")

        if request.args.get('type_operation', '') == 'D':
            research_line_project_count = session.execute(
                text("SELECT count(0) FROM app.project WHERE research_line_id = :research_line_id"),
                {'research_line_id': research_line_id}
            ).scalar()

            if research_line_project_count > 0: # type: ignore
                flash('There are projects using this research line!', category='error')
                return redirect(url_for('views.researchline'))
            else:
                session.execute(
                    text("DELETE FROM app.research_line WHERE research_line_id = :research_line_id"),
                    {'research_line_id': research_line_id}
                )
                session.commit()
                flash('Data deleted!', category='success')
                return redirect(url_for('views.researchline'))

        if request.args.get('type_operation', '') == 'A':
            session.execute(
                text("INSERT INTO app.research_line (research_line_name) VALUES (:research_line_name)"),
                {'research_line_name': research_line_name}
            )
            session.commit()
            flash('Data inserted!', category='success')
            return redirect(url_for('views.researchline'))

        if request.args.get('type_operation', '') == 'U':
            session.execute(
                text("UPDATE app.research_line SET research_line_name = :research_line_name WHERE research_line_id = :research_line_id"),
                {'research_line_name': research_line_name, 'research_line_id': research_line_id}
            )
            session.commit()
            flash('Data updated!', category='success')
            return redirect(url_for('views.researchline'))

        query = text("SELECT * FROM app.research_line ORDER BY research_line_name")
        data = session.execute(query).fetchall()
        return render_template("researchline.html", output_data=data, user=current_user)

    if request.method == 'GET':
        research_line_id = request.args.get('research_line_id', '')
        research_line_name = request.args.get('research_line_name', '')

        type_operation = 'Delete' if request.args.get('type_operation', '') == 'D' else 'Update' if request.args.get('type_operation', '') == 'U' else 'Add'

        query = text("SELECT research_line_id, research_line_name FROM app.research_line ORDER BY research_line_name")
        data_research_line = session.execute(query).fetchall()

        return render_template("researchlinedata.html", user=current_user, research_line_id=research_line_id, research_line_name=research_line_name, researchline_list=data_research_line, type_operation=type_operation)

@views.route('/projectresearch', methods=['GET', 'POST'])
@login_required
def projectresearch():
    session = db.session
    
    if request.method == 'POST':
        project_search = request.form.get('project_search')
        if len(project_search) < 1: # type: ignore
            query = text("SELECT * FROM app.project ORDER BY project_name")
            data = session.execute(query).fetchall()
            return render_template("projectresearch.html", output_data=data, user=current_user)
        else:
            query = text("""
                SELECT * FROM app.project 
                WHERE UPPER(project_name) LIKE UPPER(:search_term)
                ORDER BY project_name
            """)
            data = session.execute(query, {'search_term': f"%{project_search}%"}).fetchall()
            return render_template("projectresearch.html", output_data=data, user=current_user)
    else:
        query = text("SELECT * FROM app.project ORDER BY project_name")
        data = session.execute(query).fetchall()
        return render_template("projectresearch.html", output_data=data, user=current_user)


@views.route('/projectdata', methods=['GET', 'POST']) # type: ignore
@login_required
def projectdata():
    session = db.session

    if request.method == 'POST':
        project_id = request.form.get("project_id")
        project_name = request.form.get("project_name")
        project_description = request.form.get("project_description")
        research_line_id = request.form.get("research_line_id")

        if not research_line_id or research_line_id == 'null':
            flash('Fill out all data to execute transaction!', category='error')
        else:
            if request.args.get("type_operation") == 'D':
                project_team_count = session.execute(
                    text("SELECT count(0) FROM app.project_team WHERE project_id = :project_id"),
                    {'project_id': project_id}
                ).scalar()

                if project_team_count > 0: # type: ignore
                    flash('There are project teams using this project!', category='error')
                    return redirect(url_for('views.projectresearch'))
                else:
                    session.execute(
                        text("DELETE FROM app.project WHERE project_id = :project_id"),
                        {'project_id': project_id}
                    )
                    session.commit()
                    flash('Data deleted!', category='success')
                    return redirect(url_for('views.projectresearch'))

            if request.args.get('type_operation', '') == 'A':
                session.execute(
                    text("INSERT INTO app.project (project_name, project_description, research_line_id) VALUES (:project_name, :project_description, :research_line_id)"),
                    {'project_name': project_name, 'project_description': project_description, 'research_line_id': research_line_id}
                )
                session.commit()
                flash('Data inserted!', category='success')
                return redirect(url_for('views.projectresearch'))

            if request.args.get('type_operation', '') == 'U':
                session.execute(
                    text("UPDATE app.project SET project_name = :project_name, project_description = :project_description, research_line_id = :research_line_id WHERE project_id = :project_id"),
                    {'project_name': project_name, 'project_description': project_description, 'research_line_id': research_line_id, 'project_id': project_id}
                )
                session.commit()
                flash('Data updated!', category='success')
                return redirect(url_for('views.projectresearch'))

        query = text("SELECT * FROM app.project ORDER BY project_name")
        data = session.execute(query).fetchall()
        return render_template("projectresearch.html", output_data=data, user=current_user)

    if request.method == 'GET':
        project_id = request.args.get('project_id', '')
        project_name = request.args.get('project_name', '')
        project_description = request.args.get('project_description', '')

        type_operation = 'Add'
        if request.args.get('type_operation', '') == 'D':
            type_operation = 'Delete'
        elif request.args.get('type_operation', '') == 'U':
            type_operation = 'Update'

        research_line_name = None

        if project_id:
            research_line_name = session.execute(
                text("SELECT rsh.research_line_name FROM app.project prj JOIN app.research_line rsh ON rsh.research_line_id = prj.research_line_id WHERE prj.project_id = :project_id"),
                {'project_id': project_id}
            ).scalar()

        data_research_line = session.execute(
            text("SELECT research_line_id, research_line_name FROM app.research_line ORDER BY research_line_name")
        ).fetchall()

        return render_template("projectdata.html", user=current_user, project_id=project_id,
                               project_name=project_name, project_description=project_description,
                               researchline_name=research_line_name, researchline_list=data_research_line,
                               type_operation=type_operation)


@views.route('/modifyuserdata', methods=['GET', 'POST']) # type: ignore
@login_required
def modifyuserdata():
    session = db.session

    if request.method == 'POST':
        user_id = request.form.get('user_id', '')
        user_type_id = request.form.get("user_type_id")
        first_name = request.form.get("first_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if request.args.get('type_operation', '') == 'D':
            project_team_count = session.execute(
                text("SELECT count(0) FROM app.project_team WHERE user_id = :user_id"),
                {'user_id': user_id}
            ).scalar()

            if project_team_count > 0: # type: ignore
                flash('There are project teams using this user!', category='error')
                return redirect(url_for('views.modifyuser'))
            else:
                session.execute(
                    text("DELETE FROM app.user WHERE id = :user_id"),
                    {'user_id': user_id}
                )
                session.commit()
                flash('Data deleted!', category='success')
                return redirect(url_for('views.modifyuser'))

        if request.args.get('type_operation', '') == 'U':
            if password1 != password2:
                flash('Passwords don\'t match.', category='error')
                return redirect(url_for('views.modifyuser'))

            elif len(password1) < 7: # type: ignore
                flash('Password must be at least 7 characters.', category='error')
                return redirect(url_for('views.modifyuser'))

            else:
                session.execute(
                        text(
                            "UPDATE app.user SET first_name = :first_name, user_type_id = :user_type_id, password = :password WHERE id = :user_id"
                        ),  # type: ignore
                        {
                            'first_name': first_name,
                            'user_type_id': user_type_id,
                            'password': generate_password_hash(password1, method='pbkdf2:sha256'), # type: ignore
                            'user_id': user_id
                        }
                    )
                session.commit()
                flash('Data updated!', category='success')
                return redirect(url_for('views.modifyuser'))

        data = session.execute(
            text("SELECT id, first_name, email, user_type_id FROM app.user ORDER BY first_name")
        ).fetchall()

        return render_template("modifyuser.html", output_data=data, user=current_user)

    if request.method == 'GET':
        user_id = request.args.get('user_id', '')
        first_name = request.args.get('first_name', '')
        email = request.args.get('email', '')

        type_operation = 'Update' if request.args.get('type_operation', '') == 'U' else 'Delete'

        user_type_name_user = None

        if user_id:
            user_type_name_user = session.execute(
                text("SELECT ust.user_type_name FROM app.user usr JOIN app.user_type ust ON usr.user_type_id = ust.user_type_id WHERE usr.id = :user_id"),
                {'user_id': user_id}
            ).scalar()

        data_user_type = session.execute(
            text("SELECT * FROM app.user_type ORDER BY user_type_name")
        ).fetchall()

        return render_template("modifyuserdata.html", user=current_user, user_id=user_id,
                               first_name=first_name, email=email,
                               user_type_name=user_type_name_user, usertype_list=data_user_type,
                               type_operation=type_operation)



    if request.method == 'GET':
        user_id = request.args.get('user_id', '')
        first_name = request.args.get('first_name', '')
        email = request.args.get('email', '')

        type_operation = 'Update' if request.args.get('type_operation', '') == 'U' else 'Delete'

        user_type_name_user = None

        if user_id:
            user_type_name_user = session.execute(
                text("SELECT ust.user_type_name FROM app.user usr JOIN app.user_type ust ON usr.user_type_id = ust.user_type_id WHERE usr.id = :user_id"),
                {'user_id': user_id}
            ).scalar()

        data_user_type = session.execute(
            text("SELECT * FROM app.user_type ORDER BY user_type_name")
        ).fetchall()

        return render_template("modifyuserdata.html", user=current_user, user_id=user_id,
                               first_name=first_name, email=email,
                               user_type_name=user_type_name_user, usertype_list=data_user_type,
                               type_operation=type_operation)


@views.route('/projectteamdata', methods=['GET', 'POST']) # type: ignore
@login_required
def projectTeamData():
    session = db.session

    if request.method == 'POST':
        project_team_id = request.form.get("project_team_id")
        project_id = request.form.get("project_id")
        user_id = request.form.get("user_id")
        st_user_leader = request.form.get("st_user_leader")

        if project_id == 'null' or user_id == 'null' or st_user_leader == 'null':
            flash('Fill out all data to execute transaction!', category='error')
            return redirect(url_for('views.projectteam'))

        if request.args.get("type_operation") == 'D':
            session.execute(text("DELETE FROM app.project_team WHERE project_team_id = :project_team_id"), {'project_team_id': project_team_id})
            flash('Data deleted!', category='success')
            session.commit()
            return redirect(url_for('views.projectteam'))

        if request.args.get("type_operation") == 'A':
            existing_team = session.execute(
                text("SELECT count(0) FROM app.project_team WHERE user_id = :user_id AND project_id = :project_id"),
                {'user_id': user_id, 'project_id': project_id}
            ).scalar()

            if existing_team > 0: # type: ignore
                flash('Already there is a project for this user!', category='error')
            else:
                session.execute(
                    text("INSERT INTO app.project_team (project_team_id, project_id, user_id, st_user_leader) VALUES (nextval('app.project_team_project_team_id_seq'), :project_id, :user_id, :st_user_leader)"),
                    {'project_id': project_id, 'user_id': user_id, 'st_user_leader': st_user_leader}
                )
                flash('Data inserted!', category='success')

            session.commit()
            return redirect(url_for('views.projectteam'))

        if request.args.get("type_operation") == 'U':
            session.execute(
                text("UPDATE app.project_team SET st_user_leader = :st_user_leader WHERE project_team_id = :project_team_id"),
                {'st_user_leader': st_user_leader, 'project_team_id': project_team_id}
            )
            flash('Data updated!', category='success')
            session.commit()
            return redirect(url_for('views.projectteam'))

    if request.method == 'GET':
        project_team_id = request.args.get('project_team_id', '')

        if project_team_id:
            team_member = session.execute(
                text("""
                SELECT ptm.project_team_id, prj.project_name, usr.first_name, ptm.st_user_leader, ptm.user_id, ptm.project_id
                FROM app.project prj
                JOIN app.project_team ptm ON prj.project_id = ptm.project_id
                JOIN app.user usr ON usr.id = ptm.user_id
                WHERE ptm.project_team_id = :project_team_id
                """), {'project_team_id': project_team_id}
            ).fetchone()

            project_name = team_member.project_name # type: ignore
            first_name = team_member.first_name # type: ignore
            user_id = team_member.user_id # type: ignore
            project_id = team_member.project_id # type: ignore
            st_user_leader = team_member.st_user_leader # type: ignore
        else:
            project_name = ""
            first_name = ""
            user_id = ""
            project_id = ""
            st_user_leader = ""

        type_operation = request.args.get('type_operation', 'Add')
        if type_operation == 'D':
            type_operation = 'Delete'
        elif type_operation == 'U':
            type_operation = 'Update'

        data_user = session.execute(text("SELECT id, first_name FROM app.user ORDER BY first_name")).fetchall()
        data_project = session.execute(text("SELECT project_id, project_name FROM app.project ORDER BY project_name")).fetchall()
        data_team = session.execute(text("""
            SELECT ptm.project_team_id, prj.project_name, usr.first_name, ptm.st_user_leader
            FROM app.project prj
            JOIN app.project_team ptm ON prj.project_id = ptm.project_id
            JOIN app.user usr ON usr.id = ptm.user_id
            ORDER BY prj.project_name, usr.first_name
        """)).fetchall()

        return render_template("projectteamdata.html", user=current_user,
                               project_team_id=project_team_id,
                               project_id=project_id,
                               user_id=user_id,
                               st_user_leader=st_user_leader,
                               project_name=project_name,
                               first_name=first_name,
                               team_list=data_team,
                               project_list=data_project,
                               user_list=data_user,
                               type_operation=type_operation)


@views.route('/uploadonto', methods=['POST']) # type: ignore
def uploadfileonto():   
    if request.method == 'POST':   
        urlfile = request.form.get('urlfile')
        if urlfile !='':                    

            output_file = ".\\website\\onto\\homogenise.owl"
             
            with urllib.request.urlopen(urlfile) as response, open(output_file, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            flash('Ontology added successfully!', category='success')
        else:
            flash('Repeat operation and selecting a OWL file!', category='success')

        return render_template("uploadonto.html", user=current_user)         

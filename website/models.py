from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from website.settings import db

Base = declarative_base()
Base.metadata.schema = 'app'

class research_line(Base):

    __tablename__ = 'research_line'

    research_line_id = Column(Integer(), primary_key=True)
    research_line_name = Column(String(100), nullable=False) 
    research_lines = relationship('project', backref='research_line')


class user_type(Base):

    __tablename__ = 'user_type'

    user_type_id = Column(Integer(), primary_key=True)
    user_type_name = Column(String(100), nullable=False) 
    user_types = relationship('user', backref='user_type')


class user(Base, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    user_type_id = Column(Integer(), ForeignKey('user_type.user_type_id'), nullable=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(150))
    first_name = Column(String(150), nullable=False)
    projects_team = relationship('project_team', backref='user')
    audit_logs = relationship('audit_log', backref='user')

class audit_log(Base):

    __tablename__ = 'audit_log'

    auditlog_id = Column(Integer(), primary_key=True)    
    table_name = Column(String(50), nullable=False)  
    column_table = Column(String(50), nullable=False)  
    user_id = Column(Integer(), ForeignKey('user.id'))
    first_name_name = Column(String(50), nullable=False)
    dt_auditlog = Column(DateTime(), default=datetime.now, nullable=False)  
    action_type = Column(Integer(), nullable=False) 
    old_data_column = Column(Text, nullable=False)  
    new_data_column = Column(Text, nullable=False)  

class project(Base):

    __tablename__ = 'project'

    project_id = Column(Integer(), primary_key=True)    
    research_line_id = Column(Integer(), ForeignKey('research_line.research_line_id'))
    project_name = Column(String(200), nullable=False) 
    project_description = Column(String(400), nullable=False) 
    projects_team = relationship('project_team', backref='project')    

class project_team(Base):

    __tablename__ = 'project_team'

    project_team_id = Column(Integer(), primary_key=True)
    project_id = Column(Integer(), ForeignKey('project.project_id'))
    user_id = Column(Integer(), ForeignKey('user.id'))
    st_user_leader = Column(Integer(), nullable=False)
    __table_args__ = (UniqueConstraint('project_id', 'user_id', name='uk_project_team_project_id_user_id'), )  
    
engine = db.get_engine()
Base.metadata.create_all(engine)      
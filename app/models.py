
from app.forms import UserForm
from datetime import datetime, timezone
from flask import url_for,redirect,flash
from flask_admin import expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager,current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, WriteOnlyMapped, relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

class PatientData(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(150), index=True)
    last_name:Mapped[str] = mapped_column(String(150), index=True)
    age:Mapped[int] = mapped_column(Integer())
    address:Mapped[str] = mapped_column(String(300), index=True)
    date:Mapped[datetime] = mapped_column(default=lambda:datetime.now(timezone.utc))
    consultation:WriteOnlyMapped['ConsultationData'] = relationship('ConsultationData', back_populates='patient')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'address': self.address
        }
    
    
class ConsultationData(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    height:Mapped[float] = mapped_column(Float())
    weight:Mapped[float] = mapped_column(Float())
    imc:Mapped[float] = mapped_column(Float())
    temperature:Mapped[float] = mapped_column(Float())
    ta:Mapped[str] = mapped_column(String())
    fr:Mapped[float] = mapped_column(Float())
    sat:Mapped[str] = mapped_column(String())
    fc:Mapped[str] = mapped_column(String())
    clinic_history:Mapped[str] = mapped_column(String(500))
    medical_records:Mapped[str] = mapped_column(String(500))
    physical_exam:Mapped[str] = mapped_column(String(500))
    lab_exams:Mapped[str] = mapped_column(String(500))
    diagnostic:Mapped[str] = mapped_column(String(500))
    patient_id:Mapped[int] = mapped_column(ForeignKey(PatientData.id), index=True)
    date:Mapped[datetime] = mapped_column(default=lambda:datetime.now(timezone.utc))
    patient:Mapped['PatientData'] = relationship('PatientData',back_populates='consultation')
    prescription:WriteOnlyMapped['Prescription'] = relationship('Prescription',back_populates='consultation')
    plan:WriteOnlyMapped['Plan'] = relationship('Plan',back_populates='consultationData')

    
class Prescription(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    medicine:Mapped[str] = mapped_column(String())
    dose:Mapped[int] = mapped_column(Integer())
    instructions:Mapped[str] = mapped_column(String())
    notes:Mapped[str] = mapped_column(String())
    consultation_id:Mapped[int] = mapped_column(ForeignKey(ConsultationData.id), index=True)
    patient_id:Mapped[int] = mapped_column(ForeignKey(PatientData.id), index=True)
    consultation:Mapped['ConsultationData'] = relationship('ConsultationData',back_populates='prescription')
    
    
class Plan(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    medicine:Mapped[str] = mapped_column(String())
    dose:Mapped[int] = mapped_column(Integer())
    instructions:Mapped[str] = mapped_column(String())
    consultation_id:Mapped[int] = mapped_column(ForeignKey(ConsultationData.id), index=True)
    consultationData:Mapped['ConsultationData'] = relationship('ConsultationData',back_populates='plan')
    date:Mapped[datetime] = mapped_column()
    
class PatientNotifications(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String())
    last_name:Mapped[str] = mapped_column(String())
    age:Mapped[int] = mapped_column(Integer())
    address:Mapped[str] = mapped_column(String())
    patient_id:Mapped[int] = mapped_column(ForeignKey(PatientData.id))
    
class PrescriptionNotifications(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String())
    last_name:Mapped[str] = mapped_column(String())
    patient_id:Mapped[int] = mapped_column(ForeignKey(PatientData.id))
    consultation_id:Mapped[int] = mapped_column(ForeignKey(ConsultationData.id))    

class User(db.Model, UserMixin):
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(),unique=True)
    password_hash:Mapped[str] = mapped_column(String())
    role:Mapped[str] = mapped_column(String())
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    @property
    def is_admin(self):
        return self.role == 'Admin'
    
    def __repr__(self):
        return f'User("{self.username}")'
    
class CustomAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated and current_user.role == 'admin':
            return self.render('admin/index.html')
        flash('No tienes permisos para entrar al panel de administrador', 'warning')
        return redirect(url_for('main.index'))

class UserAdmin(ModelView):
    column_list = ['username', 'role']

    def create_form(self, obj=None):
        return UserForm(obj=obj)

    def edit_form(self, obj=None):
        return UserForm(obj=obj)

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data) 

admin = Admin(name='MyApp', template_mode='bootstrap4', index_view=CustomAdminView(url='/administrador'))            
# Add UserAdmin view
admin.add_view(UserAdmin(User, db.session))
from . import consultation
from app import socketio
from app.models import ConsultationData, PatientData, Plan, Prescription,db, PatientNotifications, PrescriptionNotifications
from app.helpers import format_name, generate_nonce

from app.forms import ConsultationForm, FindPatient, PrescriptionForm
from flask import request, flash, render_template, redirect, url_for, jsonify, abort
from flask_login import login_required
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

nonce = generate_nonce()

@consultation.route('/nueva_consulta/<int:id>', methods=['GET', 'POST'])
@login_required
def new_consultation(id):
    form = ConsultationForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            delete_notification = PatientNotifications.query.filter_by(patient_id=id).first()
        
            consultation = ConsultationData(height=form.height.data,
                                    weight=form.weight.data,
                                    imc=form.imc.data,
                                    temperature=form.temperature.data,
                                    ta=form.ta.data,
                                    fr=form.fr.data,
                                    sat=form.sat.data,
                                    fc=form.fc.data,
                                    clinic_history=form.clinic_history.data,
                                    medical_records=form.medical_records.data,
                                    physical_exam=form.physical_exam.data,
                                    lab_exams=form.lab_exams.data,
                                    diagnostic=form.diagnostic.data,
                                    patient_id=id)
            
            
            db.session.add(consultation)
            db.session.delete(delete_notification)
            db.session.commit()
            
            patient = PatientData.query.filter_by(id=id).first()
            prescription_notifications = PrescriptionNotifications(name=patient.name,last_name=patient.last_name,patient_id=id,consultation_id=consultation.id)
            
            db.session.add(prescription_notifications)
            db.session.commit()
            
            patient_name = {'name': patient.name,
                        'last_name': patient.last_name,
                        'id': consultation.id,
                        'patient_id': id}
            
            socketio.emit('patient',patient_name)    
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al acceder a la base de datos: {str(e)}', 'warning')
            return redirect(url_for('consultation.new_consultation', id=id))
        for key in form.medicines.entries:
            medicine = key.medicine.data
            dose = key.dose.data
            instructions = key.instructions.data
            
            if medicine and dose and instructions:
                try:
                    plan = Plan(medicine=medicine,
                                dose=dose,
                                instructions=instructions,
                                consultation_id=consultation.id,
                                date=consultation.date)
                    db.session.add(plan)
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()
                    flash(f'Error al acceder a la base de datos: {str(e)}', 'warning')
                    return redirect(url_for('consultation.new_consultation', id=id))
        flash('Consulta fue creada exitosamente', 'success');
        return redirect(url_for('patient.notifications'))

    return render_template('new_consultation.html', form=form, title='Nueva Consulta',id=id)

@consultation.route('/consulta_expediente', methods=['GET'])
@login_required
#@consultation.csrf.exempt
def consult_file():
    form = FindPatient(request.args)
    name = ""
    last_name = ""
    consultation= None
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Adjust as needed
    
    if form.validate():
        name = format_name(form.name.data)
        last_name = format_name(form.last_name.data)
        patient = PatientData.query.filter_by(name=name,last_name=last_name).first()
        if patient:
            consultation_id = 1  # replace with desired consultation ID

            consultation_query = db.session.query(
                ConsultationData,
                func.group_concat(Plan.medicine, ', ').label('medicines'),
                func.group_concat(Plan.dose, ', ').label('doses'),
                func.group_concat(Plan.instructions, ', ').label('instructions')
            ).join(Plan, ConsultationData.id == Plan.consultation_id).\
                filter(ConsultationData.patient_id == patient.id).\
                group_by(ConsultationData.id).\
                    order_by(ConsultationData.date.desc())

            
            consultation = consultation_query.paginate(page=page, per_page=5)
        else:
            flash('El paciente no existe en la base de datos','warning')
        
    return render_template('consult_file.html',form=form, consultation=consultation, title="Consultar Expediente",nonce=nonce,name=name,last_name=last_name)

#Dont forget to add logic so it throws an error if url is modified with different consultation id
@consultation.route('/crear_receta/<int:pid>/<int:id>',methods=['GET','POST'])
@login_required
def create_prescription(pid,id):
    form = PrescriptionForm()
    check = ConsultationData.query.filter_by(patient_id = pid).order_by(ConsultationData.date.desc()).first()
    
    if check == None  or check.patient_id != pid or check.id != id:
        abort(404)
    
    if form.validate_on_submit(): 
        try:  
            prescription_notification = PrescriptionNotifications.query.filter_by(patient_id=pid,consultation_id=id).first()
            if prescription_notification:
                db.session.delete(prescription_notification)  
                
            medicine = Prescription(medicine=form.medicine.data,
                                    dose=form.dose.data,
                                    instructions=form.instructions.data,
                                    notes=form.notes.data,
                                    consultation_id=id,
                                    patient_id=pid)
            
            db.session.add(medicine)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al acceder a la base de datos: {str(e)}', 'warning')
            return redirect(url_for('consultation.create_prescription',pid=pid,id=id))
        
        flash('Receta Creada Exitosamente', 'success')
        return jsonify({'status' : 'success',
                'message' : 'success',
                'medicine': medicine.medicine,
                'dose' : medicine.dose,
                'instructions' : medicine.instructions,
                'notes' : medicine.notes}),200
            
    return render_template ('create_prescription.html', title='Crear Receta', form=form,id=id,pid=pid, nonce=nonce)

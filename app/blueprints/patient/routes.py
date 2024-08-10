from . import patient
from app import socketio
from app.models import db
from app.forms import PatientForm, ButtonNewConsultation, FindPatient, EmptyForm, PatientNotFoundForm
from app.helpers import format_name, generate_nonce
from app.models import PatientData, PatientNotifications
from flask import render_template, jsonify, flash, url_for, redirect, request, render_template_string, session
from flask_login import login_required

from sqlalchemy.exc import SQLAlchemyError

nonce = generate_nonce()

@patient.route('/nuevo_expediente', methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    if 'name' in session:
        form.name.data = session['name']

    if 'last_name' in session:
        form.last_name.data = session['last_name']

    if form.validate_on_submit():
        name = format_name(form.name.data)
        last_name = format_name(form.last_name.data)
        age = form.age.data
        address = form.address.data
        patient = PatientData.query.filter_by(name=name,last_name=last_name).first()
        if patient:
            print(f'Paciente {patient}')
            flash('El paciente ya existe!','error')
            return redirect(url_for('main.index'))
        try:
            new_patient = PatientData(
                name= name,
                last_name= last_name,
                age= age,
                address=address
            )
       
            
            db.session.add(new_patient)
            db.session.commit()
            
            notification = PatientNotifications(name=new_patient.name, last_name=new_patient.last_name, age=new_patient.age,address=new_patient.address,patient_id=new_patient.id)
            db.session.add(notification)
            db.session.commit()
            
            new_patient_dict = {'name': name,'last_name':last_name, 'age': age, 'address':address, 'id': new_patient.id}

            socketio.emit('new_patient', new_patient_dict)
            session.pop('name',None)
            session.pop('last_name',None)
            flash('Paciente agregado exitosamente y notificacion de consulta enviada','success')
            #return redirect(url_for('main.index')) 
            return jsonify({'status':'agregado exitosamente',
                            'redirect' : url_for('main.index')}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al acceder a la base de datos: {str(e)}', 'warning')
            return jsonify({'status': 'error', 'message': f'Error al acceder a la base de datos: {str(e)}'}), 500

    return render_template('new_patient.html', form=form, title='Nuevo Expediente')


@patient.route('/notificaciones', methods=['GET'])
@login_required
def notifications():
    button = ButtonNewConsultation()
    try:
        notifications = PatientNotifications.query.all()
    except Exception as e:
        flash('Error al cargar notificaciones','error')
        return render_template('app/templates/500.html')  
    return render_template('notifications.html', title='Notificaciones',button=button,nonce=nonce,notifications=notifications)

@patient.route('/buscar_paciente',methods=['GET'])
@login_required
def find_patient():
    form = FindPatient(request.args)
    send_form = EmptyForm()
    new_patient = PatientNotFoundForm()
 
    if form.validate():
        name = format_name(form.name.data)
        last_name = format_name(form.last_name.data)

        patient = PatientData.query.filter_by(name=name,last_name=last_name).first()
        if patient:
            return jsonify({'found': True, 
                            'id' : patient.id,
                            'name': patient.name, 
                            'last_name' : patient.last_name,
                            'age': patient.age,
                            'address' : patient.address,
                            'url' : url_for('patient.send_consult',patient_id=patient.id),
                            'send_form' : render_template_string('{{ form.csrf_token }}{{ form.submit }}', form=send_form) }), 200
        else:
            session['name'] = name
            session['last_name'] = last_name
            return jsonify({'found': False,
                            'url' : url_for('patient.new_file'),
                            'send_form' : render_template_string('{{ form.csrf_token }}{{ form.submit }}',form=new_patient) }), 200
    return render_template('find_patient.html', title='Buscar Paciente',form=form)

@patient.route('/enviar_notificacion_consulta/<int:patient_id>', methods=['POST'])
@login_required
def send_consult(patient_id):
    try:
        # Perform any necessary actions with the patient ID
        # For example, retrieve patient data from the database
        patient = PatientData.query.filter_by(id=patient_id).first()

        # Check if patient exists
        if patient:
            try:
                notification = PatientNotifications(name=patient.name, last_name=patient.last_name, age=patient.age,address=patient.address,patient_id=patient.id)
                db.session.add(notification)
                db.session.commit()
                # Emit the patient data using Socket.IO
                socketio.emit('new_patient', {'id':patient.id,'name': patient.name,'last_name':patient.last_name, 'age': patient.age, 'address': patient.address})
                # Return a success response
                flash('Notificacion de Consulta Enviada','success')
                return redirect(url_for('patient.find_patient'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Error al acceder a la base de datos: {str(e)}', 'warning')
                return redirect(url_for('patient.find_patient'))
            except Exception as e:
                flash(f'Occurio un error: {str(e)}','warning')
                return redirect(url_for('patient.find_patient'))
        else:
            # Return a 404 Not Found response if patient does not exist
            return jsonify({'status': 'error', 'message': 'Paciente no encontrado'}), 404
    except Exception as e:
        # Return a 500 Internal Server Error response with the error message
        return jsonify({'status': 'error', 'message': 'Un error a occurrido: {}'.format(str(e))}), 500
    
@patient.route('/new_file', methods=['POST'])
def new_file():
    return redirect(url_for('patient.new_patient'))

@patient.route('/formulario_consulta/<int:id>', methods=['POST'])
@login_required
def to_consultation_form(id):
    return redirect(url_for('consultation.new_consultation',id=id))

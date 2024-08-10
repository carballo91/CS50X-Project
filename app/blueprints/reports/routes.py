from . import reports
from app.models import db
from app.helpers import generate_nonce
from app.forms import ButtonNewConsultation, DateSearchForm, YearSearchForm
from app.models import Prescription, ConsultationData, PatientData, Plan, PrescriptionNotifications
from flask import render_template, make_response, url_for, request
from flask_login import login_required
from sqlalchemy import func, extract
from weasyprint import HTML, CSS

nonce = generate_nonce()

@reports.route('/receta')
@login_required
def prescription():
    button = ButtonNewConsultation()
    notifications = PrescriptionNotifications.query.all()
    return render_template('prescription.html',title='receta',button=button,notifications=notifications)

@reports.route('/generate_pdf/<int:id>')
@login_required
def generate_pdf(id):
    data = db.session.query(Prescription, ConsultationData,PatientData) \
        .select_from(Prescription) \
        .join(ConsultationData) \
        .join(PatientData) \
        .filter(Prescription.consultation_id == id) \
        .all()
    # Path to the HTML file
    html_file = render_template('pdf_template.html',data=data)
    
    css = ['app/static/css/pdf.css']
    # Convert the HTML file to a PDF
    pdf = HTML(string=html_file).write_pdf(stylesheets=css)
    
    # Create a response object to send the PDF to the client
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    return response

@reports.route('/prueba')
def prueba():
    return render_template('pdf_template.html')

@reports.route('/reporte')
@login_required
def report():     
    form = DateSearchForm(request.args)
    year_form = YearSearchForm(request.args)
    months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    month = None
    year = None

    if form.validate():
        month = form.month.data
        year = form.year.data
        reports = get_reports(month,year)
        total = total_medicines(reports)
        month = months[month-1]
    elif year_form.validate():
        year = year_form.year1.data
        reports=get_reports(year=year)
        total = total_medicines(reports)
    else:
        #This query retrieves all the medicine reports
        reports = get_reports()
        total = total_medicines(reports)
        
    return render_template('report.html',title='Reportes',reports=reports,nonce=nonce,form=form,year_form=year_form,total=total,month = month, year=year)

def total_medicines(report):
    total = 0
    for t in report:
        total += t.count
    return total

def get_reports(month=None, year=None):
    # This subquery gets the medicines that are in both Prescription table and Plan table
    subquery = db.session.query(Prescription.medicine).join(Plan, Prescription.medicine == Plan.medicine).distinct()

    # Base query
    base_query = db.session.query(
        Plan.medicine,
        func.count(Plan.medicine).label('count')
    ).filter(Plan.medicine.not_in(subquery))

    # Add filters based on provided month and year
    if year:
        base_query = base_query.filter(extract('year', Plan.date) == year)
    if month:
        base_query = base_query.filter(extract('month', Plan.date) == month)

    # Group by medicine and execute the query
    reports = base_query.group_by(Plan.medicine).order_by(func.count(Plan.medicine).desc()).all()

    return reports

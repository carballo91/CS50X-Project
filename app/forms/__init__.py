"""
Forms Package
-------------

This package contains WTForms used in the Flask application for various functionalities.
"""

# Import forms from submodules
from .patient_forms import PatientForm, MedicineForm, ConsultationForm, EmptyForm, PatientNotFoundForm, ButtonNewConsultation
from .search_forms import FindPatient
from .prescription_forms import PrescriptionForm
from .filter_forms import DateSearchForm, YearSearchForm
from .auth_forms import Login, UserForm

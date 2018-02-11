from django.conf.urls import url, include
from .views import *
urlpatterns = [
    
    url(r'^party-names/', PartyNames.as_view(), name = 'party_names'),
    url(r'^add/', AddParty.as_view(), name='add party'),
    url(r'^edit/(?P<party_id>.*)/', EditParty.as_view(), name = 'edit_party'),
    url(r'^view/(?P<party_id>.*)/', ViewParty.as_view(), name = 'View_Party'),
    url(r'^editInvoice/(?P<invoice_id>\d+)/', EditInvoice.as_view(), name = 'Edit_Invoice'),
    url(r'^deleteInvoice/(?P<invoice_id>\d+)/', DeleteInvoice.as_view(), name = 'Delete_Invoice'),
    url(r'^generatePDF/(?P<party_id>\d+)/',GeneratePDF.as_view(), name= 'generate_pdf'),
    url(r'^', Cover.as_view(), name = 'Cover'),
]
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.urls import *
import datetime as datetime
from .utils import render_to_pdf
from django.template.loader import get_template
# Create your views here.

class Cover(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cover.html', {})

class PartyNames(View):
    def get(self, request, *args, **kwargs):
        party_list = Party.objects.all()
        context = {'party' : party_list}
        return render(request, 'party-names.html', context)

class AddParty(View):
    def get(self, request, *args, **kwargs):
        form = PartyNamesForm()
        context = { 'form': form }
        return render(request, 'add.html', context)

    def post(self, request, *args, **kwargs):
        form = PartyNamesForm(request.POST or None)
        context = { 'form': form }
        if form.is_valid():
            form.save()
        
        return redirect('party_names')

class EditParty(View):
    def get(self, request, *args, **kwargs):
        party_id = self.kwargs.get('party_id')
        party_object = Party.objects.filter(id = party_id)
        form = PartyNamesForm()
        form.fields['name'].initial = party_object[0].name
        form.fields['joining_date'].initial = party_object[0].joining_date
        form.fields['contact'].initial = party_object[0].contact
        form.fields['address'].initial = party_object[0].address
        context = { 'form' : form}
        return render(request, 'edit.html', context)

    def post(self, request, *args, **kwargs):
        party_id = self.kwargs.get('party_id')
        party_object = Party.objects.filter(id = party_id).first()
        form = PartyNamesForm(request.POST, instance = party_object)
        if form.is_valid():
            edit_form = form.save(commit = False)
            edit_form.save()
        return redirect('party_names')

class ViewParty(View):
    def get(self, request, *args, **kwargs):
        party_id = self.kwargs.get('party_id')
        party_info = Party.objects.filter(id = party_id).first()
        form = AccountForm()
        accounts = Accounts.objects.filter(party_id_id = party_id).order_by('-pk')[:30]
        context = { 'party_info' : party_info, 'accounts' : accounts, 'form' : form}
        return render(request, 'viewParty.html', context)

    def post(self, request, *args, **kwargs):
        party_id = self.kwargs.get('party_id')
        form = AccountForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit = False)
            post.party_id_id = party_id
            post.vehicle_no = post.vehicle_no.upper()
            print('#')
            print(post.party_id)
            post.amount = post.rate * post.quantity
            post.save()
        return redirect(reverse('View_Party',kwargs={'party_id':party_id}))

class EditInvoice(View):
    def get(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')
        invoice_object = Accounts.objects.filter(id = invoice_id)
        form = AccountForm()
        form.fields['date'].initial = invoice_object[0].date
        form.fields['item'].initial = invoice_object[0].item
        form.fields['vehicle_no'].initial = invoice_object[0].vehicle_no
        form.fields['challan_no'].initial = invoice_object[0].challan_no
        form.fields['quantity'].initial = invoice_object[0].quantity
        form.fields['rate'].initial = invoice_object[0].rate
        context = { 'form' : form ,'party_id' : invoice_object[0].party_id_id}
        return render(request, 'editInvoice.html', context)
    
    def post(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')
        invoice_object = Accounts.objects.filter(id = invoice_id)
        form = AccountForm(request.POST, instance = invoice_object[0])
        if form.is_valid():
            edit_form= form.save(commit= False)
            edit_form.amount = edit_form.rate * edit_form.quantity
            edit_form.save()
        return redirect(reverse('View_Party', kwargs={'party_id': invoice_object[0].party_id_id }))

class DeleteInvoice(View):
    def get(self, request, *args, **kwargs):
        invoice_id = self.kwargs.get('invoice_id')
        delete_object_info = Accounts.objects.filter(id = invoice_id)
        party_id = delete_object_info[0].party_id_id
        print(party_id)
        delete_object = Accounts.objects.filter(id = invoice_id).delete()        
        return redirect(reverse('View_Party', kwargs={'party_id': party_id}))


class GeneratePDF(View):
    def post(self, request, *args, **kwargs):
        template = get_template('preview.html')
        party_id = self.kwargs.get('party_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        bill = request.POST.get('bill')
        today_date = datetime.datetime.now()
        party_name = Party.objects.filter(id = party_id).values_list('name',flat = True)
        dates = Accounts.objects.filter(party_id_id = party_id, date__range=(start_date,end_date)).values('item', 'vehicle_no', 'date', 'challan_no', 'quantity', 'rate', 'amount')
        #print(dates)
        date_only = today_date.date()
        date_only = str(date_only).split('-')
        date_only = date_only[2]+"-"+date_only[1]+"-"+date_only[0]
        end_date = end_date.split('-')
        end_date = end_date[2]+"-"+end_date[1]+"-"+end_date[0]
        start_date = start_date.split('-')
        start_date = start_date[2]+"-"+start_date[1]+"-"+start_date[0]
        total_amount = 0
        total_quantity = 0
        l = []
        t = 0
        """for i in dates:
            temp = {}
            total_amount+= i.amount
            total_quantity+= i.quantity
            t = t + 1
            l.append(t)
        dates['temp'] = l"""

        for i in range(0, len(dates)):
            total_amount += dates[i]['amount']
            total_quantity += dates[i]['quantity']
            dates[i]['sr_no'] = i + 1
        print(dates)    
        context = {'party_id' : party_id ,'party_name': party_name[0], 'start_date':start_date,'end_date':end_date, 'today_date':today_date,'bill': bill,'dates':dates,'total_amount': total_amount,'total_quantity':total_quantity, 'sr_no': l }
        #print(context)
        return render(request, 'preview.html', context)
        """ 
        html = template.render(context)
        pdf = render_to_pdf('preview.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = party_name[0]+"_%s.pdf" %(date_only)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        """
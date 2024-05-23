from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import KioskCheck
from django.contrib.auth.decorators import login_required

@login_required
def completion_rate_data(request):
    # Aggregate data: count the number of KioskCheck entries per month
    data = (
        KioskCheck.objects
        .annotate(month=TruncMonth('completed_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    labels = [entry['month'].strftime("%B %Y") for entry in data]
    counts = [entry['count'] for entry in data]

    response_data = {
        "labels": labels,
        "data": counts
    }

    return JsonResponse(response_data)


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'login/login.html')
    # return HttpResponse("Hello World")


def survey(request):
    if request.method == 'POST':
        printer = request.POST['printer']
        reams_used = request.POST['reamsUsed']
        issues = request.POST['issues']
        toner_status = request.POST['tonerStatus']
        issue_description = request.POST['issueDescription']
        ricoh_ticket = request.POST['ricohTicket']
        servicenow_ticket = request.POST['serviceNowTicket']

        kiosk_check = KioskCheck.objects.create(
            user=request.user,
            printer=printer,
            reams_used=reams_used,
            issues=issues,
            toner_status=toner_status,
            issue_description=issue_description,
            ricoh_ticket=ricoh_ticket,
            servicenow_ticket=servicenow_ticket
        )

        if request.is_ajax():
            return JsonResponse({'success': True})

        return redirect('display_data')

    return render(request, 'login/printer-page.html')


def displayData(request):
    data = KioskCheck.objects.all()
    return render(request, 'login/display_data.html', {'data': data})


@login_required
def dashboard(request):
    return render(request, 'login/dashboard.html')

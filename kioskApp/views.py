from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import KioskCheck
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    """
    View to handle user registration.

    This view processes the registration form, creates a new user, and logs them in.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'login/register.html', {'form': form})

@login_required
def completion_rate_data(request):
    """
    View to aggregate and return the number of KioskCheck entries per month in JSON format.

    This view calculates the number of kiosk checks completed each month and returns the data as
    a JSON response. The data is used to render charts in the frontend.

    :param request: HttpRequest object
    :return: JsonResponse with labels (months) and data (counts)
    """
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


def login_view(request):
    """
    View to handle user login.

    This view authenticates the user using the provided username and password. If authentication
    is successful, the user is redirected to the index page. If authentication fails, an error
    message is displayed.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'login/login.html', {'error': 'Invalid username or password'})
    return render(request, 'login/login.html')



@login_required
def survey(request):
    """
    View to handle the kiosk check survey form submission.

    This view processes the POST request from the survey form, creates a new KioskCheck entry,
    and redirects to the display data page or returns a JSON response if the request is AJAX.

    :param request: HttpRequest object
    :return: HttpResponse for GET request, redirect or JsonResponse for POST request
    """
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


@login_required
def display_data(request):
    """
    View to display all KioskCheck entries.

    This view retrieves all KioskCheck entries from the database and renders them on the display
    data page.

    :param request: HttpRequest object
    :return: HttpResponse with the rendered display data template
    """
    data = KioskCheck.objects.select_related('user').all()
    return render(request, 'login/display_data.html', {'data': data})


@login_required
def dashboard(request):
    """
    View to render the dashboard page.

    This view renders the dashboard template for logged-in users.

    :param request: HttpRequest object
    :return: HttpResponse with the rendered dashboard template
    """
    return render(request, 'login/dashboard.html')


def logout_view(request):
    """
    View to handle user logout.

    This view logs out the user and redirects to the login page.

    :param request: HttpRequest object
    :return: redirect to login page
    """
    auth_logout(request)
    return redirect('login')

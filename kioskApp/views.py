import openpyxl
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import KioskCheck, ChargingStationCheck
from .forms import UserRegisterForm, ChargingStationForm
from .forms import KioskCheckForm
from django.contrib import messages


@login_required
def delete_charging_station_check(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this record.")
        return redirect('display_charging_station_data')

    item = get_object_or_404(ChargingStationCheck, pk = pk)
    item.delete()
    messages.success(request, "The record has been deleted successfully.")
    return redirect('display_charging_station_data')


def display_charging_station_data(request):
    checks = ChargingStationCheck.objects.all().order_by('-completed_date')
    paginator = Paginator(checks, 10)  # Show 10 checks per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'login/display_charging_station_data.html', context)


def charging_station_view(request):
    if request.method == 'POST':
        form = ChargingStationForm(request.POST)
        if form.is_valid():
            charging_station_check = form.save(commit = False)
            charging_station_check.user = request.user
            charging_station_check.save()
            return redirect('display_charging_station_data')  # Redirect to a new URL or render a success message
    else:
        form = ChargingStationForm()

    return render(request, 'login/charging_station.html', {'form': form})


@login_required
def export_data(request):
    # Create an HttpResponse object with the appropriate Excel header.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="kioskCheckHistory.xlsx"'

    # Create a workbook and add a worksheet.
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Kiosk Check Data'

    # Define the column headers.
    columns = ['User', 'Printer', 'Reams Used', 'Issues', 'Toner Status', 'Issue Description', 'Ricoh Ticket', 'ServiceNow Ticket', 'Completed Date']
    worksheet.append(columns)

    # Get all KioskCheck entries and populate the worksheet.
    for kiosk_check in KioskCheck.objects.select_related('user').all():
        row = [
            kiosk_check.user.username,
            kiosk_check.printer,
            kiosk_check.reams_used,
            kiosk_check.issues,
            kiosk_check.toner_status,
            kiosk_check.issue_description,
            kiosk_check.ricoh_ticket,
            kiosk_check.servicenow_ticket,
            kiosk_check.completed_date.strftime('%Y-%m-%d %H:%M:%S')
        ]
        worksheet.append(row)

    # Save the workbook to the response.
    workbook.save(response)
    return response


def delete_kiosk_check(request, pk):
    if request.method == 'POST':
        kiosk_check = get_object_or_404(KioskCheck, pk=pk)
        kiosk_check.delete()
        return redirect('display_data')  # Assuming 'display_data' is the name of the URL for your table view
    return HttpResponseForbidden("You are not allowed to access this page.")


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
    if request.method == 'POST':
        form = KioskCheckForm(request.POST)
        if form.is_valid():
            kiosk_check = form.save(commit=False)
            kiosk_check.user = request.user
            kiosk_check.save()
            if request.is_ajax():
                return JsonResponse({'success': True})
            return redirect('display_data')
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = KioskCheckForm()
    return render(request, 'login/printer-page.html', {'form': form})


@login_required
def display_data(request):
    entries_per_page = request.GET.get('entries_per_page', 10)
    entries_per_page = int(entries_per_page)

    # Order the queryset by 'completed_date'
    data = KioskCheck.objects.all().order_by('-completed_date')  # or 'completed_date' for ascending order

    paginator = Paginator(data, entries_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'login/display_data.html', {'page_obj': page_obj, 'entries_per_page': entries_per_page})


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

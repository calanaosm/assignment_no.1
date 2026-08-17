from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import (
    Customer, 
    TableCategory,
    Table,
    ReservationStatus,
    Reservation,
    Payment,
    AuditLog,
)
from .forms import (
    CustomerForm, 
    TableCategoryForm,
    TableForm,
    ReservationStatusForm,
    ReservationForm,
    PaymentForm,
)

def create_audit_log(reservation, action, performed_by, details):
    AuditLog.objects.create(
        reservation=reservation,
        action=action,
        performed_by=performed_by,
        details=details
    )

# --- Customer Views ---
def customer_list(request):
    customers = Customer.objects.all()
    output = "Customers:\n" + "\n".join([f"{c.first_name} {c.last_name} - {c.email}" for c in customers])
    return HttpResponse(output)

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return HttpResponse(
        f"Customer: {customer.first_name} {customer.last_name}<br>"
        f"Email: {customer.email}<br>"
        f"Phone: {customer.phone}"
    )

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('reservation_app:customer-detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return HttpResponse("Customer creation form is ready.")

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('reservation_app:customer-detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return HttpResponse(f"Update customer: {customer.first_name} {customer.last_name}")

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('reservation_app:customer-list')
    return HttpResponse(f"Are you sure you want to delete customer: {customer.first_name} {customer.last_name}?")


# --- Table Category Views ---
def table_category_list(request):
    table_categories = TableCategory.objects.all()
    output = "Table Categories:\n" + "\n".join([f"{cat.name} - {cat.description}" for cat in table_categories])
    return HttpResponse(output)

def table_category_detail(request, pk):
    table_category = get_object_or_404(TableCategory, pk=pk)
    return HttpResponse(f"Table Category: {table_category.name}<br>Description: {table_category.description}")

def table_category_create(request):
    if request.method == 'POST':
        form = TableCategoryForm(request.POST)
        if form.is_valid():
            table_category = form.save()
            return redirect('reservation_app:table-category-detail', pk=table_category.pk)
    else:
        form = TableCategoryForm()
    return HttpResponse("Table Category creation form is ready.")

def table_category_update(request, pk):
    table_category = get_object_or_404(TableCategory, pk=pk)
    if request.method == 'POST':
        form = TableCategoryForm(request.POST, instance=table_category)
        if form.is_valid():
            table_category = form.save()
            return redirect('reservation_app:table-category-detail', pk=table_category.pk)
    else:
        form = TableCategoryForm(instance=table_category)
    return HttpResponse(f"Update table category: {table_category.name}")

def table_category_delete(request, pk):
    table_category = get_object_or_404(TableCategory, pk=pk)
    if request.method == 'POST':
        table_category.delete()
        return redirect('reservation_app:table-category-list')
    return HttpResponse(f"Are you sure you want to delete table category: {table_category.name}?")


# --- Table Views ---
def table_list(request):
    tables = Table.objects.all()
    return HttpResponse(f"Tables: {', '.join([table.table_number for table in tables])}")

def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return HttpResponse(f"Table: {table} - Capacity: {table.capacity} - Location: {table.location}")

def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save()
            return redirect('reservation_app:table-detail', pk=table.pk)
    else:
        form = TableForm()
    return HttpResponse("Table creation form is ready.")

def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            table = form.save()
            return redirect('reservation_app:table-detail', pk=table.pk)
    else:
        form = TableForm(instance=table)
    return HttpResponse(f"Update table: {table.table_number}")

def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        table.delete()
        return redirect('reservation_app:table-list')
    return HttpResponse(f"Are you sure you want to delete table: {table.table_number}?")


# --- Reservation Status Views ---
def reservation_status_list(request):
    reservation_statuses = ReservationStatus.objects.all()
    return HttpResponse(f"Reservation Statuses: {', '.join([status.name for status in reservation_statuses])}")

def reservation_status_detail(request, pk):
    status = get_object_or_404(ReservationStatus, pk=pk)
    return HttpResponse(f"Reservation Status: {status.name} - Description: {status.description}")

def reservation_status_create(request):
    if request.method == 'POST':
        form = ReservationStatusForm(request.POST)
        if form.is_valid():
            reservation_status = form.save()
            return redirect('reservation_app:reservation-status-detail', pk=reservation_status.pk)
    else:
        form = ReservationStatusForm()
    return HttpResponse("Reservation Status creation form is ready.")

def reservation_status_update(request, pk):
    reservation_status = get_object_or_404(ReservationStatus, pk=pk)
    if request.method == 'POST':
        form = ReservationStatusForm(request.POST, instance=reservation_status)
        if form.is_valid():
            reservation_status = form.save()
            return redirect('reservation_app:reservation-status-detail', pk=reservation_status.pk)
    else:
        form = ReservationStatusForm(instance=reservation_status)
    return HttpResponse(f"Update reservation status: {reservation_status.name}")

def reservation_status_delete(request, pk):
    reservation_status = get_object_or_404(ReservationStatus, pk=pk)
    if request.method == 'POST':
        reservation_status.delete()
        return redirect('reservation_app:reservation-status-list')
    return HttpResponse(f"Are you sure you want to delete reservation status: {reservation_status.name}?")


# --- Reservation Views ---
def reservation_list(request):
    reservations = Reservation.objects.all()

    customer_id = request.GET.get('customer')
    reservation_date = request.GET.get('reservation_date')

    if customer_id:
        reservations = reservations.filter(customer_id=customer_id) 

    if reservation_date:
        reservations = reservations.filter(reservation_date=reservation_date)

    return HttpResponse(f"Reservations: {list(reservations)}")

def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return HttpResponse(f"Reservation: {reservation}")

def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            create_audit_log(reservation, "Created", str(request.user), 'Reservation created.')
            return redirect('reservation_app:reservation-detail', pk=reservation.pk)
    else:
        form = ReservationForm()
    return HttpResponse("Reservation creation form is ready.")

def reservation_update(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save()
            create_audit_log(reservation, "Updated", str(request.user), 'Reservation updated.')
            return redirect('reservation_app:reservation-detail', pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)
    return HttpResponse(f"Update reservation: {reservation}")

def reservation_delete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        create_audit_log(reservation, "Cancelled", str(request.user), 'Reservation cancelled/deleted.')
        reservation.delete()
        return redirect('reservation_app:reservation-list')
    return HttpResponse(f"Are you sure you want to delete reservation: {reservation}?")


# --- Payment Views ---
def payment_list(request):
    payments = Payment.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        payments = payments.filter(reservation_id=reservation_id)
    return HttpResponse(f"Payments: {list(payments)}")

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return HttpResponse(f"Payment: {payment}")

def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return redirect('reservation_app:payment-detail', pk=payment.pk)
    else:
        form = PaymentForm()
    return HttpResponse("Payment creation form is ready.")

def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            return redirect('reservation_app:payment-detail', pk=payment.pk)
    else:
        form = PaymentForm(instance=payment)
    return HttpResponse(f"Update payment: {payment}")

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('reservation_app:payment-list')
    return HttpResponse(f"Are you sure you want to delete payment: {payment}?")


# --- Audit Log Views ---
def audit_log_list(request):
    audit_logs = AuditLog.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        audit_logs = audit_logs.filter(reservation_id=reservation_id)
    return HttpResponse(f"Audit Logs: {list(audit_logs)}")

def audit_log_detail(request, pk):
    audit_log = get_object_or_404(AuditLog, pk=pk)
    return HttpResponse(f"Audit Log: {audit_log}")

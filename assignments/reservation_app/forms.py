from django import forms
from .models import (
    Customer, 
    TableCategory, 
    Table,
    ReservationStatus, 
    Reservation, 
    Payment
)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_at', 'updated_at']

class TableCategoryForm(forms.ModelForm):
    class Meta:
        model = TableCategory
        exclude = ['created_at', 'updated_at']

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        exclude = ['created_at', 'updated_at']
        widgets = {
            'capacity': forms.NumberInput(attrs={'min': 1}),
        }

class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = ReservationStatus
        exclude = ['created_at', 'updated_at']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['created_at', 'updated_at']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'guests': forms.NumberInput(attrs={'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()

        guests = cleaned_data.get('guests')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        table = cleaned_data.get('table')

        # Guest count must be positive
        if guests is not None and guests <= 0:
            self.add_error('guests', 'Guest count must be greater than zero.')

        # End time must be later than start time
        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', "End time must be later than start time.")

        # Table capacity must accommodate guests
        if table and guests:
            if table.capacity < guests:
                self.add_error('guests', 'Guest count exceeds the table capacity.')

        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['created_at', 'updated_at']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'paid_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

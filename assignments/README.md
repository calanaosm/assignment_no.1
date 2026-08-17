INFOSYS 22 – ASSIGNMENT #1
DJANGO TABLE RESERVATION SYSTEM
Simple Activity Documentation

Project: assignments
App: reservation_app
Database	SQLite (db.sqlite3)

1. Introduction
This activity is about building the backend of a Django Table Reservation System. The main parts are the models, forms, views, and URLs required by the activity.
2. Objectives
Create the required Django models.
Create forms for entering and editing data.
Add validation for reservations.
Create views for the required operations.
Connect the views using URLs.
Test the Django project and database.
3. Project Structure
assignments/
├── config/
├── reservation_app/
└── db.sqlite3
	└── manage.py
4. Models
The system has seven main models:
Customer – stores customer information.
TableCategory – stores table categories.
Table – stores restaurant tables, including location and capacity.
ReservationStatus – stores reservation statuses.
Reservation – stores customer reservations.
Payment – stores payments related to reservations.
AuditLog – records important reservation actions.
5. Forms
The main ModelForms are:
CustomerForm
TableCategoryForm
TableForm
ReservationStatusForm
ReservationForm
PaymentForm
The ReservationForm is especially important because it validates the reservation data.
Reservation validation includes:
Guests must be a positive number.
End time must be later than start time.
Guests must not exceed the selected table's capacity.
AuditLog does not need a public form because audit records are created by the system.
6. Views
Views receive requests and perform the required operations. The activity includes views for customers, table categories, tables, reservation statuses, reservations, payments, and audit logs.
List – displays records.
Detail – displays one record.
Create – creates a new record.
Update – changes an existing record.
Delete/Cancel – removes or cancels a record where required.
Filter – filters reservations by customer or reservation date.
7. URLs
The project URL configuration connects the main project to the reservation_app application's URLs.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservation_app.urls')),
]
8. Audit Log
The system uses a create_audit_log() helper to automatically record important reservation actions. The log stores the reservation, action, person who performed it, timestamp, and details.
9. Database and Testing
Django migrations were created and applied.
The required models were registered in Django Admin.
The database used is SQLite.
The Django system check returned: System check identified no issues (0 silenced).
10. Basic Requirements
A customer can be created and can have multiple reservations.
A table can be assigned to a table category.
A reservation is connected to a customer, table, and reservation status.
A reservation records the date, time, and number of guests.
A reservation cannot exceed table capacity.
A payment can be connected to a reservation.
Important reservation actions can be recorded in the AuditLog.
11. Conclusion
The Django Table Reservation System connects the required models, forms, views, and URLs. The backend was checked successfully, and the main database relationships and reservation validation rules were implemented.





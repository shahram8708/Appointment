from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from .forms import AppointmentForm

def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            subject_user = 'Appointment Confirmation'
            message_user = render_to_string('confirmation_email.html', {'appointment': appointment})
            email_from = settings.EMAIL_HOST_USER
            recipient_list_user = [appointment.email]

            pdf_content = generate_pdf(appointment)
            pdf_filename = f'Appointment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

            email_user = EmailMessage(subject_user, message_user, email_from, recipient_list_user)
            email_user.attach(pdf_filename, pdf_content, 'application/pdf')

            email_user.send(fail_silently=False)
            
            subject_admin = 'New Appointment Registered'
            message_admin = f'A new appointment has been registered:\n\nName: {appointment.name}\nEmail: {appointment.email}\nDate and Time: {appointment.date_time}'
            email_to_admin = settings.ADMIN_EMAIL_ADDRESS  

            send_mail(subject_admin, message_admin, email_from, [email_to_admin], fail_silently=False)

            return redirect('confirmation_page')  
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})

def confirmation_page(request):
    return render(request, 'confirmation_page.html')

def generate_pdf(appointment):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, f'Appointment ID: {appointment.id}')
    c.drawString(100, 700, f'Name: {appointment.name}')
    c.drawString(100, 600, f'Email: {appointment.email}')
    c.drawString(100, 500, f'Date and Time: {appointment.date_time}')
    c.save()
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content

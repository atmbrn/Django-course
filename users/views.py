from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Send email to admin
            send_mail(
                'New User Registration',
                f'Username: {user.username}\nEmail: {user.email}',
                'from@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )

            # Send welcome email to user
            email = EmailMessage(
                'Welcome!',
                render_to_string('users/emails/user_welcome.html', {'username': user.username}),
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()

            return redirect('success_url')  # Redirect to a success page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

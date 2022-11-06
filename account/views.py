from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.forms import RegistrationForm
from account.tokens import account_activation_token


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')

    register_form = RegistrationForm(request.POST or None)

    if register_form.is_valid():
        user = register_form.save(commit=False)
        user.email = register_form.cleaned_data['email']
        user.set_password(register_form.cleaned_data['password'])
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        subject = 'Activate your Account'
        message = render_to_string('account/registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject=subject, message=message)
        return HttpResponse('registered successfully and activation sent')

    return render(request, 'account/registration/register.html', {'form': register_form})


@login_required
def dashboard(request):
    return HttpResponse('Dashboard')

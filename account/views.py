from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from account.forms import RegistrationForm
from account.models import UserBase
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


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except():
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
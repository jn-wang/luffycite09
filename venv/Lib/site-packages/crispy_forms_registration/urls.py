from django.conf.urls import patterns, url
from registration.backends.default.views import RegistrationView
from crispy_forms_registration.forms import CrispyAuthenticationForm
from crispy_forms_registration.forms import CrispyRegistrationForm
from crispy_forms_registration.forms import CrispyPasswordResetForm
from crispy_forms_registration.forms import CrispyPasswordChangeForm
from crispy_forms_registration.forms import CrispySetPasswordForm

urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', {
        'authentication_form': CrispyAuthenticationForm,
        }, name='login'),
    url(r'^password/change/$', 'password_change', {
        'password_change_form': CrispyPasswordChangeForm,
        }, name='auth_password_change'),
    url(r'^password/reset/$', 'password_reset', {
        'password_reset_form': CrispyPasswordResetForm,
        }, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', {
            'set_password_form': CrispySetPasswordForm
        }, name='auth_password_reset_confirm'),
)

urlpatterns += patterns(
    '',
    url(r'^register/$',
        RegistrationView.as_view(form_class=CrispyRegistrationForm),
        name='registration_register'),
)

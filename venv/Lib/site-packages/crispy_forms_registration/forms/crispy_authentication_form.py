# coding=utf-8
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django.contrib.auth.forms import AuthenticationForm


class CrispyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CrispyAuthenticationForm, self).__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_action = '.'

        helper.layout = Layout(
            'username',
            'password',
            FormActions(
                Submit('submit', 'Ingresar', css_class='btn-lg btn-block')
            ),
            HTML(u"""
            {% load url from future %}

            <input type="hidden" name="next" value="{{ next }}" />

            <div class="form-group with_margin_top password_reset_link">
                <a href="{% url 'auth_password_reset' %}">
                    ¿Olvidaste tu contraseña?
                </a>
            </div>
            """)
        )

        self.helper = helper

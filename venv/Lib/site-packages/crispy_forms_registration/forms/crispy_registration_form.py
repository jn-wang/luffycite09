# coding=utf-8
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from registration.forms import RegistrationForm


class CrispyRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(CrispyRegistrationForm, self).__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_class = 'form-horizontal form_without_actions_decoration'
        helper.form_method = 'post'
        helper.form_action = '.'
        helper.add_input(Submit('submit', u'¡Registrarse!'))

        self.helper = helper

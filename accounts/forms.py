from django import forms
from django.db import connection

from .models import User


class RegistrationForm(forms.ModelForm):
    error_messages = {
        'Form Error': 'Error occurred due to invalid data.'
    }
    first_name = forms.CharField(
        label='First Name',
        strip=True,
        min_length=1,
        help_text='Enter your first name.',
    )
    middle_name = forms.CharField(
        label='Middle Name',
        strip=True,
        required=False,
        help_text='Enter your middle name.',
    )
    last_name = forms.CharField(
        label='Last Name',
        strip=True,
        min_length=1,
        help_text='Enter your last name.',
    )
    url = forms.URLField(
        label='Author URL',
        widget=forms.URLInput,
        help_text='Enter a homepage URL.',
        required=False
    )
    type = forms.ChoiceField(
        label='Author Type',
        widget=forms.RadioSelect,
        choices=[
            ('Student', 'Student'),
            ('Faculty', 'Faculty'),
        ],
        help_text='Select the kind of author you are (Student/Faculty).',
    )

    class Meta:
        model = User
        fields = ['email', ]

    def clean(self):
        """
        Validate form data.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        typ = cleaned_data.get('type')

        if 'first_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('first_name')):
            self.add_error('first_name', 'Name cannot contain numbers.')

        if 'middle_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('middle_name')):
            self.add_error('middle_name', 'Name cannot contain numbers.')

        if 'last_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('last_name')):
            self.add_error('last_name', 'Name cannot contain numbers.')

        if 'type' in cleaned_data and typ != 'Student' and typ != 'Faculty':
            self.add_error('type', 'Invalid value for type.')

        return self.cleaned_data
    
    def save(self, **kwargs):
        """
        Save the form. 
        """
        obj = super(RegistrationForm, self).save(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute('SELECT `id` ' +
                           'FROM `author` ' +
                           'WHERE email=%s;', [self.cleaned_data['email']], )
            row = cursor.fetchone()

            if row is not None and row[0] is None:
                obj.author_id = row[0]
            else:
                cursor.execute('SELECT MAX(`id`) FROM `author`;')
                row = cursor.fetchone()

                if row is not None and row[0] is not None:
                    a_id = row[0] + 1
                else:
                    a_id = 1

                obj.author_id = a_id

                args = [a_id, ]

                args += list(map(
                    (lambda x: x if x is not None and x != '' else None),
                    [
                        self.cleaned_data['email'],
                        self.cleaned_data['first_name'],
                        self.cleaned_data['middle_name'],
                        self.cleaned_data['last_name'],
                        self.cleaned_data['url'],
                        self.cleaned_data['type'],
                    ]
                ))

                sql = 'INSERT ' +\
                      'INTO `author`(`id`, `email`, `first_name`, `middle_name`, `last_name`, `url`, `type`) ' +\
                      'VALUES(%s, %s, %s, %s, %s, %s, %s);'

                cursor.execute(sql, args)

        return obj


class DashboardForm(forms.Form):
    institute = forms.ChoiceField(
        label='Institute',
        choices=[],
        help_text='Choose your institute from the list. ' +
                  'If your institute does not exist, add one from the dashboard menu.'
    )
    department = forms.ChoiceField(
        label='Department',
        choices=[],
        help_text='Choose your department from the list.' +
                  'If your department does not exist, add one from the dashboard menu.'
    )

    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)

        with connection.cursor() as cursor:
            cursor.execute('SELECT `id`, `name` FROM `department`;')
            tbl = cursor.fetchall()

            dept_choices = list(map(
                lambda row: (row[0], row[1]),
                tbl
            ))

            cursor.execute('SELECT `id`, `name` FROM `institute`;')
            tbl = cursor.fetchall()

            inst_choices = list(map(
                lambda row: (row[0], row[1]),
                tbl
            ))

        self.fields['institute'].choices = inst_choices
        self.fields['department'].choices = dept_choices


class FacultyApprovalForm(forms.Form):
    pass

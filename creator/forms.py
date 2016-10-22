import copy

from django import forms
from django.db import connection


class AddInstituteForm(forms.Form):
    name = forms.CharField(
        label='Institute Name',
        help_text='Enter the name of the institute here.',
        min_length=1
    )
    city = forms.CharField(
        label='City',
        help_text='Enter the city of the institute here.',
        min_length=1
    )
    state = forms.CharField(
        label='State',
        help_text='Enter the state of the institute.',
        min_length=1
    )
    country = forms.CharField(
        label='Country',
        help_text='Enter the country the institute is in.',
        min_length=1
    )
    postal = forms.CharField(
        label='Postal Code',
        help_text='Enter the postal code of the institute here.',
        min_length=1
    )
    url = forms.URLField(
        label='Institute URL',
        help_text='Enter a URL of the institute.',
        min_length=1
    )

    def clean(self):
        cleaned_data = super(AddInstituteForm, self).clean()
        text_fields = {
            'name': cleaned_data.get('name'),
            'city': cleaned_data.get('city'),
            'state': cleaned_data.get('state'),
            'country': cleaned_data.get('country'),
        }

        for f in text_fields.keys():
            if f in cleaned_data and any(char.isdigit() for char in text_fields[f]):
                self.add_error('%s' % f, 'Field %s cannot contain numbers.' % f)

        if 'postal' in cleaned_data and not all(char.isdigit() for char in cleaned_data.get('postal')):
            self.add_error('postal', 'Postal code must be numeric.')

        if 'name' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `institute` ' +
                               'WHERE `name`=%s', [cleaned_data['name'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('name', 'Institute field with same name exists.')

        return self.cleaned_data


class AddDepartmentForm(forms.Form):
    name = forms.CharField(
        label='Department Name',
        help_text='Enter the name of the department here.',
        min_length=1
    )

    def clean(self):
        cleaned_data = super(AddDepartmentForm, self).clean()
        text_fields = {
            'name': cleaned_data.get('name'),
        }

        for f in text_fields.keys():
            if f in cleaned_data and any(char.isdigit() for char in text_fields[f]):
                self.add_error(f, 'Field %s cannot contain numbers.' % f)

        if 'name' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `department` ' +
                               'WHERE `name`=%s', [cleaned_data['name'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('name', 'Department with same name exists.')

        return self.cleaned_data


class AddFieldForm(forms.Form):
    name = forms.CharField(
        label='Field Name',
        help_text='Enter the name of the field here.',
        min_length=1
    )
    department1 = forms.ChoiceField(
        label='Department(s)',
        help_text='Choose the department(s) the field belongs to. ' +
                  'If a department does not exist. Add one from the menu.',
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super(AddFieldForm, self).__init__(*args, **kwargs)

        with connection.cursor() as cursor:
            cursor.execute('SELECT `id`, `name` FROM `department`;')
            tbl = cursor.fetchall()

            dept_choices = list(map(
                lambda row: (row[0], row[1]),
                tbl
            ))

            self.fields['department1'].choices = dept_choices

    def clean(self):
        cleaned_data = super(AddFieldForm, self).clean()
        text_fields = {
            'name': cleaned_data.get('name'),
        }

        for f in text_fields.keys():
            if f in cleaned_data and any(char.isdigit() for char in text_fields[f]):
                self.add_error(f, 'Field %s cannot contain numbers.' % f)

        if 'name' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `publication_field` ' +
                               'WHERE `title`=%s', [cleaned_data['name'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('name', 'Publication field with same name exists.')

        i = 0
        while True:
            if not 'department%d' % (i + 1) in cleaned_data:
                break
            i += 1

        for j in range(0, i):
            for k in range(j + 1, i):
                if cleaned_data['department%d' % (j + 1)] == cleaned_data['department%d' % (k + 1)]:
                    self.add_error('department%d' % (j + 1), 'Two department fields cannot be same')
                    self.add_error('department%d' % (k + 1), 'Two department fields cannot be same')

        return self.cleaned_data


class AddAuthorForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        strip=True,
        min_length=1,
        help_text='Enter the author\'s first name.',
    )
    middle_name = forms.CharField(
        label='Middle Name',
        strip=True,
        required=False,
        help_text='Enter the author\'s middle name.',
    )
    last_name = forms.CharField(
        label='Last Name',
        strip=True,
        min_length=1,
        help_text='Enter the author\'s last name.',
    )
    email = forms.EmailField(
        label='Email',
        help_text='Enter the author\'s Email here.'
    )
    url = forms.URLField(
        label='Author URL',
        widget=forms.URLInput,
        help_text='Enter a homepage URL for the author.',
        required=False
    )
    type = forms.ChoiceField(
        label='Author Type',
        widget=forms.RadioSelect,
        choices=[
            ('Student', 'Student'),
            ('Faculty', 'Faculty'),
        ],
        help_text='Select the kind of author (Student/Faculty).',
    )
    institute = forms.ChoiceField(
        label='Institute',
        choices=[],
        help_text='Choose the author\'s institute from the list. ' +
                  'If your institute does not exist, add one from the menu.'
    )
    department = forms.ChoiceField(
        label='Department',
        choices=[],
        help_text='Choose the author\'s department from the list. ' +
                  'If your department does not exist, add one from the menu.'
    )

    def __init__(self, *args, **kwargs):
        super(AddAuthorForm, self).__init__(*args, **kwargs)

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

    def clean(self):
        """
        Validate form data.
        """

        cleaned_data = super(AddAuthorForm, self).clean()
        typ = cleaned_data.get('type')

        if 'first_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('first_name')):
            self.add_error('first_name', 'Name cannot contain numbers.')

        if 'middle_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('middle_name')):
            self.add_error('middle_name', 'Name cannot contain numbers.')

        if 'last_name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('last_name')):
            self.add_error('last_name', 'Name cannot contain numbers.')

        if 'type' in cleaned_data and typ != 'Student' and typ != 'Faculty':
            self.add_error('type', 'Invalid value for type.')

        if 'email' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `author` ' +
                               'WHERE `email`=%s', [cleaned_data['email'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('email', 'Author with same Email exists.')

        return self.cleaned_data


class AddPublisherForm(forms.Form):
    name = forms.CharField(
        label='Publisher Name',
        strip=True,
        min_length=1,
        help_text='Enter the publisher\'s name.',
    )
    url = forms.URLField(
        label='Publisher URL',
        widget=forms.URLInput,
        help_text='Enter a homepage URL for the publisher.',
    )
    type = forms.ChoiceField(
        label='Publisher Type',
        widget=forms.RadioSelect,
        choices=[
            ('Journal', 'Journal'),
            ('Conference', 'Conference'),
            ('Publishing House', 'Publishing House'),
        ],
        help_text='Select the kind of publisher.',
    )

    def clean(self):
        """
        Validate form data.
        """

        cleaned_data = super(AddPublisherForm, self).clean()
        typ = cleaned_data.get('type')

        if 'name' in cleaned_data and any(char.isdigit() for char in cleaned_data.get('name')):
            self.add_error('first_name', 'Name cannot contain numbers.')

        if 'type' in cleaned_data and typ != 'Conference' and typ != 'Journal' and typ != 'Publishing House':
            self.add_error('type', 'Invalid value for type.')

        if 'url' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `publisher` ' +
                               'WHERE `url`=%s', [cleaned_data['url'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('url', 'Publisher with same URL exists.')

        return self.cleaned_data


class AddPublicationForm(forms.Form):
    title = forms.CharField(
        label='Title',
        help_text='The title of the publication.',
        min_length=1
    )
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea,
        help_text='A brief abstract of your publication.'
    )
    url = forms.URLField(
        label='URL',
        help_text='A URL for your publication.',
        required=False,
    )
    location = forms.CharField(
        label='Location',
        required=False,
        help_text='Enter a location for your publication, it can be the location ' +
                  'of the conference or that of the publisher.'
    )
    date = forms.DateField(
        label='Date of Publication',
        help_text='Date your publication was published. The format is "DD/MM/YYYY".',
        input_formats=['%d/%m/%Y', ]
    )
    code = forms.CharField(
        label='Publication Code',
        required=False,
        help_text='ISBN or similar code for the publication.'
    )
    publisher = forms.ChoiceField(
        label='Publisher',
        help_text='Choose the publisher from the list. If yours doesn\'t exist, add one from the menu.',
        choices=[]
    )
    author1 = forms.ChoiceField(
        label='Author(s)',
        help_text='Choose the author from the list. If yours does not exist, add one from the menu.',
        choices=[]
    )
    degree1 = forms.ChoiceField(
        label='Degree',
        help_text='The degree/status of author',
        choices=[
            ('first', 'First'),
            ('second', 'Second'),
            ('third', 'Third'),
            ('corresponding', 'Corresponding'),
            ('other', 'Other')
        ]
    )
    field1 = forms.ChoiceField(
        label='Field(s)/Area(s)',
        help_text='Choose the field(s) your publication belongs to. If yours does not exist, add one from the menu.',
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super(AddPublicationForm, self).__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            cursor.execute('SELECT `id`, `title` FROM `publication_field`;')
            tbl = cursor.fetchall()

            field_choices = list(map(
                lambda row: (row[0], row[1]),
                tbl
            ))

            cursor.execute('SELECT `id`, `first_name`, `last_name` FROM `author`;')
            tbl = cursor.fetchall()

            author_choices = list(map(
                lambda row: (row[0], row[1] + ' ' + row[2]),
                tbl
            ))

            cursor.execute('SELECT `id`, `name` FROM `publisher`;')
            tbl = cursor.fetchall()

            publ_choices = list(map(
                lambda row: (row[0], row[1]),
                tbl
            ))

        self.fields['publisher'].choices = publ_choices
        self.fields['field1'].choices = field_choices
        self.fields['author1'].choices = author_choices

    def clean(self):
        cleaned_data = copy.deepcopy(super(AddPublicationForm, self).clean())

        if 'url' in cleaned_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT `id` ' +
                               'FROM `publication` ' +
                               'WHERE `url`=%s', [cleaned_data['url'], ])
                row = cursor.fetchone()

                if row is not None and row[0]:
                    self.add_error('url', 'Publication with same URL exists.')

        i = 0
        while True:
            if not 'author%d' % (i + 1) in cleaned_data:
                break
            i += 1

        for j in range(0, i):
            for k in range(j + 1, i):
                if cleaned_data['author%d' % (j + 1)] == cleaned_data['author%d' % (k + 1)]:
                    self.add_error('author%d' % (j + 1), 'Two author fields cannot be same')
                    self.add_error('author%d' % (k + 1), 'Two author fields cannot be same')

        i = 0
        while True:
            if not 'field%d' % (i + 1) in cleaned_data:
                break
            i += 1

        for j in range(0, i):
            for k in range(j + 1, i):
                if cleaned_data['field%d' % (j + 1)] == cleaned_data['field%d' % (k + 1)]:
                    self.add_error('field%d' % (j + 1), 'Two fields cannot be same')
                    self.add_error('field%d' % (k + 1), 'Two fields cannot be same')

        return self.cleaned_data

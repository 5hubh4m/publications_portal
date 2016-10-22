from copy import deepcopy

from django.shortcuts import render, redirect
from django.db import connection
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView

from .forms import (
    AddAuthorForm,
    AddDepartmentForm,
    AddFieldForm,
    AddInstituteForm,
    AddPublisherForm,
    AddPublicationForm
)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddDetailsView(FormView):
    template_name = 'creator/add_form.html'

    def __init__(self):
        super(AddDetailsView, self).__init__()

    def get_context_data(self, **kwargs):
        context = super(AddDetailsView, self).get_context_data(**kwargs)
        context['title'] = self.title

        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id`=%s', [self.request.user.author_id, ])
            row = cursor.fetchone()

            if row is not None:
                context['username'] = row[1]

        return context


class AddAuthor(AddDetailsView):
    title = 'Author'
    form_class = AddAuthorForm

    def form_valid(self, form):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO ' + \
                  '`author`(`first_name`, `middle_name`, `last_name`, `email`, ' + \
                            '`url`, `type`, `institute.id`, `department.id`)' + \
                  'VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'

            args = list(map(
                (lambda x: x if x is not None and x != '' else None),
                [
                    form.cleaned_data['first_name'],
                    form.cleaned_data['middle_name'],
                    form.cleaned_data['last_name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['url'],
                    form.cleaned_data['type'],
                    form.cleaned_data['institute'],
                    form.cleaned_data['department'],
                ]
            ))

            cursor.execute(sql, args)

        return redirect('/add/successful')


class AddInstitute(AddDetailsView):
    title = 'Institute'
    form_class = AddInstituteForm

    def form_valid(self, form):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO ' + \
                  '`institute`(`name`, `city`, `state`, `country`, `postal_code`, `url`)' + \
                  'VALUES(%s, %s, %s, %s, %s, %s);'

            args = list(map(
                (lambda x: x if x is not None and x != '' else None),
                [
                    form.cleaned_data['name'],
                    form.cleaned_data['city'],
                    form.cleaned_data['state'],
                    form.cleaned_data['country'],
                    form.cleaned_data['postal'],
                    form.cleaned_data['url'],
                ]
            ))

            cursor.execute(sql, args)

        return redirect('/add/successful')


class AddDepartment(AddDetailsView):
    title = 'Department'
    form_class = AddDepartmentForm

    def form_valid(self, form):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO ' + \
                  '`department`(`name`)' + \
                  'VALUES(%s);'

            args = list(map(
                (lambda x: x if x is not None and x != '' else None),
                [form.cleaned_data['name'], ]
            ))

            cursor.execute(sql, args)

        return redirect('/add/successful')


class AddField(AddDetailsView):
    title = 'Publication Field'
    form_class = AddFieldForm
    template_name = 'creator/add_field.html'

    def __init__(self):
        super(AddField, self).__init__()
        self.no_of_extra_fields = 0

    def post(self, request, *args, **kwargs):
        print(request.POST)

        i = 0
        while True:
            if 'department%d' % (i + 1) not in request.POST:
                break
            i += 1

        self.no_of_extra_fields = i - 1

        return super(AddField, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(AddField, self).get_form(form_class)

        for i in range(0, self.no_of_extra_fields):
            form.fields['department%s' % (i + 2)] = deepcopy(form.fields['department1'])

        return form

    def form_valid(self, form):
        with connection.cursor() as cursor:
            cursor.execute('SELECT MAX(`id`) FROM `publication_field`;')
            row = cursor.fetchone()

            if (row is None) or (row is not None and row[0] is None):
                f_id = 1
            else:
                f_id = row[0] + 1

            sql = 'INSERT INTO ' + \
                  '`publication_field`(`id`, `title`)' + \
                  'VALUES(%s, %s);'
            args = [f_id, ]
            args += list(map(
                (lambda x: x if x is not None and x != '' else None),
                [form.cleaned_data['name'], ]
            ))

            cursor.execute(sql, args)

            for i in range(0, self.no_of_extra_fields + 1):
                dept = form.cleaned_data['department%d' % (i + 1)]
                cursor.execute('INSERT INTO ' +
                               '`field_has_department` (`field.id`, `department.id`) ' +
                               'VALUES(%s, %s);', [f_id, dept, ])

        return redirect('/add/successful')


class AddPublisher(AddDetailsView):
    title = 'Publication'
    form_class = AddPublisherForm

    def form_valid(self, form):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO ' + \
                  '`publisher`(`name`, `type`, `url`)' + \
                  'VALUES(%s, %s, %s);'

            args = list(map(
                (lambda x: x if x is not None and x != '' else None),
                [
                    form.cleaned_data['name'],
                    form.cleaned_data['type'],
                    form.cleaned_data['url'],
                ]
            ))

            cursor.execute(sql, args)

        return redirect('/add/successful')


class AddPublication(AddDetailsView):
    template_name = 'creator/add_publication.html'
    form_class = AddPublicationForm
    title = 'Publication'

    def __init__(self):
        super(AddPublication, self).__init__()
        self.no_of_extra_author_fields = 0
        self.no_of_extra_field_fields = 0

    def post(self, request, *args, **kwargs):
        print(request.POST)

        i = 0
        while True:
            if 'author%d' % (i + 1) not in request.POST:
                break
            i += 1

        self.no_of_extra_author_fields = i - 1

        i = 0
        while True:
            if 'field%d' % (i + 1) not in request.POST:
                break
            i += 1

        self.no_of_extra_field_fields = i - 1

        return super(AddPublication, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(AddPublication, self).get_form(form_class)

        for i in range(0, self.no_of_extra_author_fields):
            form.fields['author%s' % (i + 2)] = deepcopy(form.fields['author1'])
            form.fields['degree%s' % (i + 2)] = deepcopy(form.fields['degree1'])

        for i in range(0, self.no_of_extra_field_fields):
            form.fields['field%s' % (i + 2)] = deepcopy(form.fields['field1'])

        return form

    def form_valid(self, form):
        with connection.cursor() as cursor:
            cursor.execute('SELECT MAX(`id`) FROM `publication`;')
            row = cursor.fetchone()

            if (row is None) or (row is not None and row[0] is None):
                p_id = 1
            else:
                p_id = row[0] + 1

            cursor.execute('SELECT `type` ' +
                           'FROM `author` ' +
                           'WHERE `id`=%s;', [self.request.user.author_id, ])
            row = cursor.fetchone()

            if row[0] == 'Student':
                approved = False
                approved_by = None
            else:
                approved = True
                approved_by = self.request.user.author_id

            submitted_by = self.request.user.author_id

            sql = 'INSERT INTO ' + \
                  '`publication`(`id`, `title`, `description`, `url`, `location`, `date`, `publication_code`, ' +\
                  '`publisher.id`, `approved_by`, `approved`, `submitted_by`)' + \
                  'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            args = [p_id, ]
            args += list(map(
                (lambda x: x if x is not None and x != '' else None),
                [
                    form.cleaned_data['title'],
                    form.cleaned_data['description'],
                    form.cleaned_data['url'],
                    form.cleaned_data['location'],
                    form.cleaned_data['date'],
                    form.cleaned_data['code'],
                    form.cleaned_data['publisher'],
                    approved_by,
                    approved,
                    submitted_by
                ]
            ))

            cursor.execute(sql, args)

            for i in range(0, self.no_of_extra_author_fields + 1):
                author = form.cleaned_data['author%d' % (i + 1)]
                degree = form.cleaned_data['degree%d' % (i + 1)]
                cursor.execute('INSERT INTO ' +
                               '`publication_has_author` (`publication.id`, `author.id`, `degree`) ' +
                               'VALUES(%s, %s, %s);', [p_id, author, degree, ])

            for i in range(0, self.no_of_extra_field_fields + 1):
                field = form.cleaned_data['field%d' % (i + 1)]
                cursor.execute('INSERT INTO ' +
                               '`publication_has_field` (`publication.id`, `field.id`) ' +
                               'VALUES(%s, %s);', [p_id, field, ])

        return redirect('/add/successful')


@login_required(login_url='/login/')
def action_successful(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute('SELECT * ' +
                       'FROM `author` ' +
                       'WHERE `id`=%s', [request.user.author_id, ])
        row = cursor.fetchone()

        if row is not None:
            context['username'] = row[1]

    return render(request, 'creator/action_successful.html', context)

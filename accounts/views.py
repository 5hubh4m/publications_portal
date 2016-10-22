from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView
from django.db import connection

from .forms import RegistrationForm, DashboardForm
from .models import User


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DashBoard(FormView):
    form_class = DashboardForm
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoard, self).get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id`=%s', [self.request.user.author_id, ])
            row = cursor.fetchone()

            if row is not None:
                context['username'] = row[1]
                context['first_name'] = row[1]
                context['last_name'] = row[3]
                if row[2] is not None:
                    context['middle_name'] = row[2]
                context['type'] = row[8]
                context['url'] = row[4]

                if row[7] is not None:
                    cursor.execute('SELECT `name` ' +
                                   'FROM `department` ' +
                                   'WHERE `id`=%s', [row[7], ])
                    dept = cursor.fetchone()[0]
                    context['dept_id'] = row[7]
                    context['dept'] = dept

                if row[6] is not None:
                    cursor.execute('SELECT `name`, `city` ' +
                                   'FROM `institute` ' +
                                   'WHERE `id`=%s', [row[6], ])
                    inst, inst_city = cursor.fetchone()
                    context['inst_id'] = row[6]
                    context['inst'] = inst
                    context['inst_city'] = inst_city

                if row[8] == 'Faculty':
                    cursor.execute('SELECT `publication`.`id` ' +
                                   'FROM `publication`, `publication_has_author` ' +
                                   'WHERE `publication.id`=`publication`.`id` ' +
                                   'AND `publication`.`approved`=FALSE ' +
                                   'AND `author.id`=%s;',
                                   [self.request.user.author_id, ])
                    row = cursor.fetchall()
                    if row is not None:
                        context['unapproved'] = []
                        for r in row:
                            cursor.execute('SELECT `publication`.`id`, `title`, `description`, `publication`.`url`, ' +
                                           '`location`, `date`, ' +
                                           '`publication_code`, `author`.`first_name`, `author`.`last_name` ' +
                                           'FROM `publication`, `author` ' +
                                           'WHERE `publication`.`id`=%s AND ' +
                                           '`publication`.`submitted_by`=`author`.`id`;', [r[0], ])
                            x = cursor.fetchone()
                            if x is not None:
                                context['unapproved'] += [[
                                    x[0],
                                    x[1][:30] + '...',
                                    x[2][:30] + '...',
                                    x[3],
                                    x[4],
                                    x[5],
                                    x[6],
                                    x[7] + ' ' + x[8]
                                ], ]

        return context

    def get_form(self, form_class=None):
        form = super(DashBoard, self).get_form(form_class)

        with connection.cursor() as cursor:
            cursor.execute('SELECT `institute.id`, `department.id` ' +
                           'FROM `author` ' +
                           'WHERE `id`=%s', [self.request.user.author_id, ])
            row = cursor.fetchone()

            if row[0] is not None and row[1] is not None:
                form = None
            elif row[1] is None and row[0] is not None:
                form.fields.pop('department', None)
            elif row[0] is None and row[1] is not None:
                form.fields.pop('institute', None)

        return form

    def form_valid(self, form):
        with connection.cursor() as cursor:
            if 'department' in form.fields:
                cursor.execute('UPDATE `author`' +
                               'SET `department.id`=%s' +
                               'WHERE `id`=%s;', [form.cleaned_data['department'], self.request.user.author_id, ])

            if 'institute' in form.fields:
                cursor.execute('UPDATE `author`' +
                               'SET `institute.id`=%s' +
                               'WHERE `id`=%s;', [form.cleaned_data['institute'], self.request.user.author_id, ])

        return redirect('/dashboard/')


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(User.objects.make_random_password())
        obj.save()

        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()

        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'accounts/email.html',
            'subject_template_name': 'accounts/email_subject.txt',
            'request': self.request,
            'token_generator': default_token_generator,
            'html_email_template_name': None,
            'extra_email_context': None,
        }

        reset_form.save(**opts)

        return redirect('/signup/successful')


def is_faculty(a_id):
    if a_id is not None and type(a_id) == int:
        with connection.cursor() as cursor:
            cursor.execute('SELECT `type` ' +
                           'FROM `author` ' +
                           'WHERE `id`=%s;', [a_id, ])

            row = cursor.fetchone()
            if row is not None and row[0] is not None:
                return row[0] == 'Faculty'

    return False


@login_required(login_url='/login/')
@user_passes_test(lambda u: is_faculty(u.author_id), login_url='/dashboard/')
def approve(request, publication_id):
    if publication_id is not None:
        with connection.cursor() as cursor:
            cursor.execute('SELECT `id` ' +
                           'FROM `publication`, `publication_has_author` ' +
                           'WHERE `publication`.`id`=`publication.id` AND `author.id`=%s ' +
                           'AND `publication`.`id`=%s;',
                           [request.user.author_id, publication_id])
            row = cursor.fetchone()

            if row is not None and row[0] is not None:
                cursor.execute('UPDATE `publication` ' +
                               'SET `approved`=TRUE, `approved_by`=%s ' +
                               'WHERE `id`=%s;',
                               [request.user.author_id, publication_id])

        return redirect('/dashboard/')


@login_required(login_url='/login/')
def successful(request):
    return render(request, 'accounts/signup_successful.html')

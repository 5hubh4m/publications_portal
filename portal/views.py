from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.views.generic import FormView

from .forms import SearchForm


def index(request):
    context = {}

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `publication`.`id`, `title`, `description`, `date`, `location`, `publisher`.`id`, ' +
                       '`publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher` WHERE `publisher.id`=`publisher`.`id` ' +
                       'AND `approved`=TRUE ORDER BY `date` DESC;')
        tbl = cursor.fetchall()[:10]
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/index.html', context)


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'portal/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * ' +
                               'FROM `author` ' +
                               'WHERE `id` = %s;', [self.request.user.author_id, ])
                row = cursor.fetchone()

                context['username'] = row[1]

        return context

    def form_valid(self, form):
        key_word = form.cleaned_data['search']
        key_word = '%' + key_word + '%'

        context = {}
        if self.request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * ' +
                               'FROM `author` ' +
                               'WHERE `id` = %s;', [self.request.user.author_id, ])
                row = cursor.fetchone()

                context['username'] = row[1]

        with connection.cursor() as cursor:
            sql = """SELECT `publication`.`id`, `title`, `description`, `date`, `location`, `publisher`.`id`,
                     `publisher`.`name`, `publisher`.`type`
                     FROM `publication`, `publisher`
                     WHERE `approved`=TRUE AND (`title` LIKE %s OR `description` LIKE %s);"""

            cursor.execute(sql, [key_word, key_word])
            tbl = cursor.fetchall()
            if tbl is not None and tbl[0] is not None:
                context['publications'] = []
                for row in tbl:
                    get_publication(row, context)

        return render(self.request, 'portal/search.html', context)


def publication(request, publication_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `id` ' +
                       'FROM `publication` ' +
                       'WHERE `id`=%s;', [publication_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher`, `publication_has_author`, `author` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `publication.id`=`publication`.`id` ' +
                       'AND `author.id`=`author`.`id` AND `approved`=TRUE '
                       'AND `publication`.`id`=%s ORDER BY `date` DESC;', [publication_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/publication.html', context)


def author(request, author_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `id` ' +
                       'FROM `author` ' +
                       'WHERE `id`=%s;', [author_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * ' +
                       'FROM `author` ' +
                       'WHERE `id`=%s', [author_id, ])
        row = cursor.fetchone()

        if row is not None:
            context['username'] = row[1]
            context['first_name'] = row[1]
            context['last_name'] = row[3]
            if row[2] is not None:
                context['middle_name'] = row[2]
            context['type'] = row[8]
            context['url'] = row[4]
            context['email'] = row[5]

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

        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher`, `publication_has_author` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `publication.id`=`publication`.`id` ' +
                       'AND `author.id`=%s AND `approved`=TRUE ORDER BY `date` DESC;', [author_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/author.html', context)


def institute(request, institute_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `id` ' +
                       'FROM `institute` ' +
                       'WHERE `id`=%s;', [institute_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * ' +
                       'FROM `institute` ' +
                       'WHERE `id`=%s', [institute_id, ])
        row = cursor.fetchone()

        if row is not None:
            context['name'] = row[1]
            context['city'] = row[2]
            context['state'] = row[3]
            context['url'] = row[6]
            context['country'] = row[4]

        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher`, `publication_has_author`, `author` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `publication.id`=`publication`.`id` ' +
                       'AND `author.id`=`author`.`id` AND `approved`=TRUE ' +
                       'AND `institute.id`=%s ORDER BY `date` DESC;', [institute_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/institute.html', context)


def department(request, department_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `name` ' +
                       'FROM `department` ' +
                       'WHERE `id`=%s;', [department_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False
        else:
            context['name'] = row[0]

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher`, `publication_has_author`, `author` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `publication.id`=`publication`.`id` ' +
                       'AND `author.id`=`author`.`id` AND `approved`=TRUE '
                       'AND `department.id`=%s ORDER BY `date` DESC;', [department_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/department.html', context)


def field(request, field_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `title` ' +
                       'FROM `publication_field` ' +
                       'WHERE `id`=%s;', [field_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False
        else:
            context['title'] = row[0]

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT `department`.`id`, `name` ' +
                       'FROM `field_has_department`, `department` ' +
                       'WHERE `department.id`=`department`.`id` AND `field.id`=%s', [field_id, ])
        tb = cursor.fetchall()

        if tb is not None:
            context['departments'] = []
            for row in tb:
                context['departments'] += [[
                    row[0],
                    row[1]
                ], ]

        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher`, `publication_has_field` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `publication.id`=`publication`.`id` ' +
                       'AND `field.id`=%s AND `approved`=TRUE ORDER BY `date` DESC;', [field_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/field.html', context)


def publisher(request, publisher_id):
    context = {}
    found = True

    if request.user.is_authenticated:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * ' +
                           'FROM `author` ' +
                           'WHERE `id` = %s;', [request.user.author_id, ])
            row = cursor.fetchone()

            context = {
                'username': row[1]
            }

    with connection.cursor() as cursor:
        cursor.execute('SELECT `id` ' +
                       'FROM `publisher` ' +
                       'WHERE `id`=%s;', [publisher_id, ])
        row = cursor.fetchone()

        if row is None or row[0] is None:
            found = False

    if not found:
        return redirect('/404')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * ' +
                       'FROM `publisher` ' +
                       'WHERE `id`=%s', [publisher_id, ])
        row = cursor.fetchone()

        if row is not None:
            context['name'] = row[1]
            context['type'] = row[2]
            context['url'] = row[3]

        cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                       '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                       'FROM `publication`, `publisher` WHERE ' +
                       '`publisher.id`=`publisher`.`id` AND `approved`=TRUE ' +
                       'AND `publisher.id`=%s ORDER BY `date` DESC;', [publisher_id, ])
        tbl = cursor.fetchall()
        if tbl is not None:
            context['publications'] = []
            for r in tbl:
                get_publication(r, context)

    return render(request, 'portal/publisher.html', context)


def dump(request):
    if request.method == 'POST':
        ids = []
        for key in request.POST.keys():
            if key[:2] == 'id':
                ids.append(request.POST.get(key))

        if len(ids) > 0:
            context = {}
            response = '<?xml version="1.0" encoding="UTF-8"?>\n'
            response += '<publications>\n'
            for i in ids:
                response += '\t<publication>\n'
                context['publication'] = []
                with connection.cursor() as cursor:
                    cursor.execute('SELECT DISTINCT `publication`.`id`, `title`, `description`, `date`, `location`, ' +
                                   '`publisher`.`id`, `publisher`.`name`, `publisher`.`type` ' +
                                   'FROM `publication`, `publisher` WHERE ' +
                                   '`publisher.id`=`publisher`.`id` AND `approved`=TRUE ' +
                                   'AND `publication`.`id`=%s ORDER BY `date` DESC;', [i, ])
                    tbl = cursor.fetchall()
                    if tbl is not None:
                        context['publications'] = []
                        for r in tbl:
                            get_publication(r, context)
                publ = context['publications'][0]

                response += '\t\t<title>%s</title>\n' % (publ[1])
                response += '\t\t<description>%s</description>\n' % (publ[2])
                response += '\t\t<date>%s</date>\n' % (publ[3])
                response += '\t\t<published_by>%s</published_by>\n' % (publ[6])
                response += '\t\t<location>%s</location>\n' % (publ[4])
                response += '\t\t<type>%s</type>\n' % (publ[9])
                response += '\t\t<authors>\n'
                for a in publ[7]:
                    response += '\t\t\t<author>\n'
                    response += '\t\t\t\t<name>%s</name>\n' % (a[1])
                    response += '\t\t\t\t<institute>%s</institute>\n' % (a[4])
                    response += '\t\t\t\t<department>%s</department>\n' % (a[6])
                    response += '\t\t\t</author>\n'
                response += '\t\t</authors>\n'
                response += '\t\t<fields>\n'
                for f in publ[8]:
                    response += '\t\t\t<field>%s</field>\n' % (f[1])
                response += '\t\t</fields>\n'
            response += '</publications>\n'

            return HttpResponse(response, content_type='text/text')

    return redirect('/')


def not_found(request):
    return render(request, 'portal/404.html')


def author_deg2num(a):
    if a[2] == 'first':
        return 1
    elif a[2] == 'second':
        return 2
    elif a[2] == 'third':
        return 3
    elif a[2] == 'corresponding':
        return 1.5
    else:
        return 4


def get_publication(r, context):
    p_id = r[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT `author`.`id`, `first_name`, `middle_name`, `last_name`, ' +
                       '`degree`, `institute`.`id`, `institute`.`name`, `department`.`id`, ' +
                       '`department`.`name` ' +
                       'FROM `author`, `publication_has_author`, `institute`, `department` ' +
                       'WHERE `author.id`=`author`.`id` AND `publication.id`=%s ' +
                       'AND `institute.id`=`institute`.id AND `author`.`department.id`=`department`.`id`;',
                       [p_id, ])
        tbl2 = cursor.fetchall()

        auth = []
        if tbl2 is not None:
            for r2 in tbl2:
                auth += [[
                    r2[0],
                    '%s %s' % (r2[1], r2[3]) if r2[2] is None else '%s %s %s' % (r2[1], r2[2], r2[3]),
                    r2[4],
                    r2[5],
                    r2[6],
                    r2[7],
                    r2[8]
                ], ]

        cursor.execute('SELECT `publication_field`.`id`, `title` ' +
                       'FROM `publication_field`, `publication_has_field`' +
                       'WHERE `publication.id`=%s AND `field.id`=`publication_field`.`id`;', [p_id, ])
        tbl3 = cursor.fetchall()

        fields = []
        if tbl3 is not None:
            for r3 in tbl3:
                fields += [[
                    r3[0],
                    r3[1]
                ], ]

        context['publications'] += [[
            r[0],
            r[1],
            r[2],
            r[3],
            r[4],
            r[5],
            r[6],
            sorted(auth, key=author_deg2num),
            fields,
            r[7],
        ], ]

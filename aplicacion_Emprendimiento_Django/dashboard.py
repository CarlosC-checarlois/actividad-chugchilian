from django.utils.translation import gettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):

        self.children.append(modules.LinkList(
            _('Accesos rápidos'),
            children=[
                {'title': _('Volver al sitio'), 'url': '/', 'external': False},
                {'title': _('Cambiar contraseña'), 'url': '/admin/password_change/', 'external': False},
                {'title': _('Cerrar sesión'), 'url': '/admin/logout/', 'external': False},
            ],
            column=0,
            order=0
        ))

        self.children.append(modules.AppList(
            _('Aplicaciones'),
            column=1,
            order=0,
        ))

        self.children.append(modules.AppList(
            _('Autenticación y permisos'),
            models=('django.contrib.auth.*',),
            column=2,
            order=0,
        ))

        self.children.append(modules.RecentActions(
            _('Acciones recientes'),
            limit=8,
            column=0,
            order=1
        ))

        self.children.append(modules.Feed(
            _('Últimas noticias de Django'),
            feed_url='https://www.djangoproject.com/rss/weblog/',
            column=1,
            order=1
        ))

        self.children.append(modules.LinkList(
            _('Soporte'),
            children=[
                {'title': _('Documentación Django'), 'url': 'https://docs.djangoproject.com/', 'external': True},
                {'title': _('Django Users'), 'url': 'https://groups.google.com/g/django-users', 'external': True},
                {'title': _('GitHub Django'), 'url': 'https://github.com/django/django', 'external': True},
            ],
            column=2,
            order=1
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    def init_with_context(self, context):
        self.children.append(modules.ModelList(_('Modelos')))
        self.children.append(modules.RecentActions(
            _('Últimos cambios'),
            include_list=self.get_app_content_types(),
        ))

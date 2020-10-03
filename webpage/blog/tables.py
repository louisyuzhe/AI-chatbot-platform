import django_tables2 as tables

from chatterbot.ext.django_chatterbot.models import Statement

class StatementTable(tables.Table):
    class Meta:
        model = Statement
        template_name = "django_tables2/bootstrap.html"

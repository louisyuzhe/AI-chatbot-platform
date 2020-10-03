from django_filters import FilterSet

from chatterbot.ext.django_chatterbot.models import Statement

class StatementFilter(FilterSet):
    class Meta:
        model = Statement
        fields = {"text": ["contains"], "in_response_to": ["contains"], "conversation": ["exact"]}

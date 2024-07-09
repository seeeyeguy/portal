""" 
Serializer module for LDAP service requests/responses.
"""

from rest_framework import serializers


class LDAPSearchRequestSerializer(serializers.Serializer):
    """LDAP search request serializer."""

    search_term = serializers.CharField(allow_blank=False, required=True)
    match_whole_word = serializers.BooleanField(default=False)
    offset = serializers.IntegerField(min_value=1, default=1)
    limit = serializers.IntegerField(min_value=1)
    content_count = serializers.IntegerField(min_value=0, default=0)

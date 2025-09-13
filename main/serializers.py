from rest_framework import serializers


class HealthSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    db_time_ms = serializers.IntegerField(required=False)


class StatsSerializer(serializers.Serializer):
    active = serializers.BooleanField()
    db_time_ms = serializers.IntegerField(required=False)

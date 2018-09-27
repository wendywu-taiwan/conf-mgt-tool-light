from rest_framework import serializers
from RulesetComparer.models import Country, Environment


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    full_name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Country(validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.full_name = validated_data("full_name", instance.full_name)
        instance.save()
        return instance


class EnvironmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Environment(validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class RuleListItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    base_count = serializers.IntegerField()
    new_count = serializers.IntegerField()
    add_count = serializers.IntegerField()
    minus_count = serializers.IntegerField()
    modify_count = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RuleSerializer(serializers.Serializer):
    process = serializers.CharField(max_length=200)
    process_step = serializers.CharField(max_length=200)
    organization_id = serializers.CharField(max_length=200)
    owner_role = serializers.CharField(max_length=200)
    rule_type = serializers.CharField(max_length=200)
    key = serializers.CharField(max_length=200)
    value = serializers.CharField(max_length=200)
    expression = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ModifiedRuleValueSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    process = serializers.CharField(max_length=200)
    process_step = serializers.CharField(max_length=200)
    organization_id = serializers.CharField(max_length=200)
    owner_role = serializers.CharField(max_length=200)
    rule_type = serializers.CharField(max_length=200)
    rule_key = serializers.CharField(max_length=200)
    base_value = serializers.CharField(max_length=200)
    base_expression = serializers.CharField(max_length=200)
    compare_value = serializers.CharField(max_length=200)
    compare_expression = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

from rest_framework import serializers
from RulesetComparer.models import Country, Environment
from RulesetComparer.properties import dataKey


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
    table_type = serializers.CharField(max_length=200)
    base_count = serializers.IntegerField()
    new_count = serializers.IntegerField()
    add_count = serializers.IntegerField()
    remove_count = serializers.IntegerField()
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
    value = serializers.SerializerMethodField()
    expression = serializers.SerializerMethodField()

    def get_value(self, data):
        result = data[dataKey.RULE_KEY_RULE_VALUE].split(",")
        return result

    def get_expression(self, data):
        result = data[dataKey.RULE_KEY_RULE_EXPRESSION].split(",")
        return result

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ModifiedRuleValueSerializer(serializers.Serializer):
    process = serializers.CharField(max_length=200)
    process_step = serializers.CharField(max_length=200)
    organization_id = serializers.CharField(max_length=200)
    owner_role = serializers.CharField(max_length=200)
    rule_type = serializers.CharField(max_length=200)
    key = serializers.CharField(max_length=200)
    base_value = serializers.SerializerMethodField()
    base_expression = serializers.SerializerMethodField()
    compare_value = serializers.SerializerMethodField()
    compare_expression = serializers.SerializerMethodField()

    def get_base_value(self, data):
        result = data[dataKey.RULE_MODIFIED_KEY_BASE_VALUE].split(",")
        return result

    def get_base_expression(self, data):
        result = data[dataKey.RULE_MODIFIED_KEY_BASE_EXPRESSION].split(",")
        return result

    def get_compare_value(self, data):
        result = data[dataKey.RULE_MODIFIED_KEY_COMPARE_VALUE].split(",")
        return result

    def get_compare_expression(self, data):
        result = data[dataKey.RULE_MODIFIED_KEY_COMPARE_EXPRESSION].split(",")
        return result

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

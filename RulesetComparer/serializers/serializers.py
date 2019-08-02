from rest_framework import serializers

from RulesetComparer.models import MailContentType
from permission.models import Country, Environment, Module, Function
from RulesetComparer.properties import key


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ('id', 'name', 'icon_file_name')


class ModuleSerializer(serializers.ModelSerializer):
    functions = FunctionSerializer(many=True)

    class Meta:
        model = Module
        fields = ('id', 'name', 'icon_file_name', 'functions')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'full_name', "icon_file_name")


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'name', 'full_name')


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
        result = data[key.RULE_KEY_RULE_VALUE].split(",")
        return result

    def get_expression(self, data):
        result = data[key.RULE_KEY_RULE_EXPRESSION].split(",")
        return result

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ModifiedRuleValueSerializer(serializers.Serializer):
    combined_key = serializers.CharField(max_length=200)
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
        result = data[key.RULE_MODIFIED_KEY_BASE_VALUE].split(",")
        return result

    def get_base_expression(self, data):
        result = data[key.RULE_MODIFIED_KEY_BASE_EXPRESSION].split(",")
        return result

    def get_compare_value(self, data):
        result = data[key.RULE_MODIFIED_KEY_COMPARE_VALUE].split(",")
        return result

    def get_compare_expression(self, data):
        result = data[key.RULE_MODIFIED_KEY_COMPARE_EXPRESSION].split(",")
        return result

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class MailContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailContentType
        fields = ('id', 'name', 'title')

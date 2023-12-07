from rest_framework import serializers
from .models import Student, Teacher


def name_starts_with_s(value):
    if value[0].lower() == 's':
        raise serializers.ValidationError('Name should not start with "s"')


class StudentSerializers(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, validators=[name_starts_with_s])
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=50)

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError(
                "Students aged less than 18 are not allowed")
        return value

    def validate(self, attrs):
        name = attrs.get('name')
        city = attrs.get('city')

        if name == 'nayan' or name.startswith('z'):
            raise serializers.ValidationError(
                "Name (nayan) or name starting with 'z' is not allowed")

        if city.lower() == 'haveri':
            raise serializers.ValidationError("City 'Haveri' is not allowed")

        return attrs

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

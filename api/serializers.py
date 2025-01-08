from django.forms import CharField
from rest_framework import serializers
from .models import (
    SchoolProfile, CustomUser, JobPosting,
    Application, TeacherProfile
)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=128)
    user_type = serializers.ChoiceField(choices=[('school', 'School'), ('teacher', 'Teacher')])
    name = serializers.CharField(max_length=255, required=False)  # School-specific
    location = serializers.CharField(required=False)  # School-specific
    subject_expertise = serializers.CharField(max_length=255, required=False)  # Teacher-specific
    qualifications = serializers.CharField(max_length=255, required=False)  # Teacher-specific

    def validate(self, data):
        print('name' not in data,'++++++++++++++++++++')
        user_type = data.get('user_type')
        if user_type == 'school' and ('name' not in data or 'location' not in data):
            raise serializers.ValidationError("Schools must provide 'name' and 'address'.")
        if user_type == 'teacher' and ('subject_expertise' not in data or 'qualifications' not in data):
            raise serializers.ValidationError("Teachers must provide 'subject' and 'qualification'.")
        return data

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            user_type=user_type,
            password=password
        )
        if user_type == 'school':
            SchoolProfile.objects.create(user=user, name=validated_data['name'], location=validated_data['location'])
        elif user_type == 'teacher':
            TeacherProfile.objects.create(user=user, subject_expertise=validated_data['subject_expertise'], qualifications=validated_data['qualifications'])
        return user





class UserSerializer(serializers.ModelSerializer):
    """Serialized the CustomUser model"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class TeacherProfileSerializer(serializers.ModelSerializer):
    """Serializes the TeacherProfile Model"""

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'subject_expertise']

class SchoolProfileSerializer(serializers.ModelSerializer):
    """Serializes the SchoolProfile Model"""

    class Meta:
        model = SchoolProfile
        fields = ['id', 'user', 'name', 'location']

class JobPostingSerializer(serializers.ModelSerializer):
    """Serializes the JobPosting Model"""

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ['school']

        def create(self, validated_data):
            user = self.context['request'].user
            school = user.school  # Assuming the `School` model has a `OneToOneField` to the user
            validated_data['school'] = school
            return super().create(validated_data)

class ApplicationSerializer(serializers.ModelSerializer):
    """Serializes the Application Model"""

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['teacher']
    
    def create(self, validated_data):
        user_ = self.context['request'].user
        teacher = TeacherProfile.objects.filter(user=user_).first()
        print(teacher, '++++++++++++++++')
        validated_data['teacher'] = teacher
        return super().create(validated_data)
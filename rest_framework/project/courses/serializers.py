from rest_framework import serializers
from datetime import date

from .models import Instructor, Student, Course


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name', 'email', 'experience_years')

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError('Experience cannot be negative')
        return value


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'registered_at')


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all(), required=False
    )

    instructor_detail = InstructorSerializer(source='instructor', read_only=True)
    students_detail = StudentSerializer(source='students', many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'start_date',
            'instructor', 'students', 'instructor_detail', 'students_detail'
        )

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Start date cannot be in the past')
        return value

    def validate(self, attrs):
        students = attrs.get('students') if 'students' in attrs else None
        if students is not None and len(students) == 0:
            raise serializers.ValidationError('A course must have at least one student')
        return attrs

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        course = Course.objects.create(**validated_data)
        if students:
            course.students.set(students)
        return course

    def update(self, instance, validated_data):
        students = validated_data.pop('students', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if students is not None:
            instance.students.set(students)
        return instance

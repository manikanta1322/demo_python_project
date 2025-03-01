from rest_framework import serializers
from .models import Product
from .models import Student
from .models import MobileVerification


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'



class MobileVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileVerification
        fields = ['phone_number']

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .models import Student
from .serializers import StudentSerializer
from .models import MobileVerification
from .serializers import MobileVerificationSerializer
import random 

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class StudentListView(APIView):
    def get(self, request):
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(
                {"status": 200,"message": "Success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"status": 500, "message": "Internal Server Error. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": 200, "message": "Success"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"status": 400, "message": "Validation Error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"status": 500, "message": "Internal Server Error. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)  # Fetch the student by ID
        except Student.DoesNotExist:
            return Response(
                {"status": 404, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": 200, "message": "Student updated successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"status": 400, "message": "Validation Error", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {"status": 500, "message": "Internal Server Error. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return Response({"status": 200, "message": "Student deleted successfully"}, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"status": 404, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class RequestOTPAPIView(APIView):
    """API to request OTP"""
    def post(self, request):
        serializer = MobileVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user, created = MobileVerification.objects.get_or_create(phone_number=phone_number)
            user.generate_otp()
            
            return Response({
                "message": "OTP generated successfully!",
                "otp": user.otp  # Directly returning OTP for testing
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPAPIView(APIView):
    """API to verify OTP"""
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        try:
            user = MobileVerification.objects.get(phone_number=phone_number)
            if user.otp == otp:
                user.is_verified = True
                user.otp = None  # Clear OTP after verification
                user.save()
                return Response({"message": "Mobile number verified successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except MobileVerification.DoesNotExist:
            return Response({"error": "Mobile number not found"}, status=status.HTTP_404_NOT_FOUND)

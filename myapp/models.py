from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Student(models.Model):
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])

    def __str__(self):
        return self.name



class MobileVerification(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        """Generates a random 6-digit OTP"""
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return f"{self.phone_number} - Verified: {self.is_verified}"

from django.db import models
from django.contrib.auth.models import User
from accounts.models import Doctor


class Symptom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Disease(models.Model):
    disease_name = models.CharField(max_length=255, unique=True)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE, related_name='diseases')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.disease_name


class DiseaseReport(models.Model):
    report = models.CharField(max_length=200)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='diseasereport')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    cure_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diseasereport')

    def __str__(self):
        return self.report


class PredictDisease(models.Model):
    check_disease_name = models.CharField(max_length=255, unique=True)
    request_at = models.DateTimeField(auto_now_add=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='predicts')
    request_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predicts')

    def __str__(self):
        return self.check_disease_name

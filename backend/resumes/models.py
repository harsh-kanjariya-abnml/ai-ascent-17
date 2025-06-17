from django.db import models
import uuid

# Create your models here.

class SeniorityChoices(models.TextChoices):
    JUNIOR = 'junior', 'Junior'
    MID = 'mid', 'Mid-level'
    SENIOR = 'senior', 'Senior'
    LEAD = 'lead', 'Lead'
    PRINCIPAL = 'principal', 'Principal'

class QualificationChoices(models.TextChoices):
    HIGH_SCHOOL = 'high_school', 'High School'
    BACHELORS = 'bachelors', 'Bachelor\'s Degree'
    MASTERS = 'masters', 'Master\'s Degree'
    PHD = 'phd', 'PhD'
    DIPLOMA = 'diploma', 'Diploma'
    CERTIFICATION = 'certification', 'Certification'

class CandidateProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    skills = models.JSONField(default=list)  # Store as list of strings
    fe_score = models.IntegerField(default=0, help_text="Frontend score (0-100)")
    be_score = models.IntegerField(default=0, help_text="Backend score (0-100)")
    seniority = models.CharField(
        max_length=20,
        choices=SeniorityChoices.choices,
        default=SeniorityChoices.JUNIOR
    )
    qualifications = models.CharField(
        max_length=20,
        choices=QualificationChoices.choices,
        default=QualificationChoices.BACHELORS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - FE:{self.fe_score} BE:{self.be_score}"

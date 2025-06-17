import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.db import IntegrityError
from rest_framework import status

from .models import CandidateProfile, SeniorityChoices, QualificationChoices
from .resume_parser import process_resume

# Create your views here.


def health_check(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_http_methods(["POST"])
def process_resume_endpoint(request):
    """
    POST /process endpoint - Accepts a PDF resume file and processes it.
    """
    try:
        # Check if file is provided
        if 'resume' not in request.FILES:
            return JsonResponse(
                {"error": "No resume file provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resume_file = request.FILES['resume']
        
        # Validate file type
        if not resume_file.name.lower().endswith('.pdf'):
            return JsonResponse(
                {"error": "Only PDF files are supported"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (max 10MB)
        if resume_file.size > 10 * 1024 * 1024:
            return JsonResponse(
                {"error": "File size must be less than 10MB"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process the resume using the resume_parser service
        try:
            parsed_data = process_resume(resume_file)
        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to process resume: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save the processed data to CandidateProfile model
        try:
            candidate_profile = CandidateProfile.objects.create(
                name=parsed_data.get('name', 'Unknown'),
                skills=parsed_data.get('skills', []),
                fe_score=parsed_data.get('fe_score', 0),
                be_score=parsed_data.get('be_score', 0),
                seniority=parsed_data.get('seniority', SeniorityChoices.JUNIOR),
                qualifications=parsed_data.get('qualifications', QualificationChoices.BACHELORS)
            )
            
            return JsonResponse({
                "message": "Resume processed successfully",
                "candidate_id": str(candidate_profile.id),
                "candidate_data": {
                    "name": candidate_profile.name,
                    "skills": candidate_profile.skills,
                    "fe_score": candidate_profile.fe_score,
                    "be_score": candidate_profile.be_score,
                    "seniority": candidate_profile.seniority,
                    "qualifications": candidate_profile.qualifications
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to save candidate profile: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return JsonResponse(
            {"error": f"Internal server error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@require_http_methods(["POST"])
def get_candidates(request):
    """
    POST /get-candidates endpoint - Accepts filter criteria and returns matching candidates.
    """
    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON in request body"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract filter parameters
        skills_filter = data.get('skills', [])
        seniority_filter = data.get('seniority', None)
        qualifications_filter = data.get('qualifications', None)
        fe_score_min = data.get('fe_score_min', None)
        be_score_min = data.get('be_score_min', None)
        
        # Validate filter parameters
        if skills_filter and not isinstance(skills_filter, list):
            return JsonResponse(
                {"error": "Skills filter must be an array of strings"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if seniority_filter and seniority_filter not in [choice.value for choice in SeniorityChoices]:
            return JsonResponse(
                {"error": f"Invalid seniority value. Must be one of: {[choice.value for choice in SeniorityChoices]}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if qualifications_filter and qualifications_filter not in [choice.value for choice in QualificationChoices]:
            return JsonResponse(
                {"error": f"Invalid qualifications value. Must be one of: {[choice.value for choice in QualificationChoices]}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if fe_score_min is not None and (not isinstance(fe_score_min, int) or fe_score_min < 0 or fe_score_min > 100):
            return JsonResponse(
                {"error": "fe_score_min must be an integer between 0 and 100"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if be_score_min is not None and (not isinstance(be_score_min, int) or be_score_min < 0 or be_score_min > 100):
            return JsonResponse(
                {"error": "be_score_min must be an integer between 0 and 100"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Start with all candidate profiles
        queryset = CandidateProfile.objects.all()
        
        # Apply filters
        if skills_filter:
            # Filter candidates who have at least one of the specified skills
            for skill in skills_filter:
                queryset = queryset.filter(skills__icontains=skill)
        
        if seniority_filter:
            queryset = queryset.filter(seniority=seniority_filter)
        
        if qualifications_filter:
            queryset = queryset.filter(qualifications=qualifications_filter)
        
        if fe_score_min is not None:
            queryset = queryset.filter(fe_score__gte=fe_score_min)
        
        if be_score_min is not None:
            queryset = queryset.filter(be_score__gte=be_score_min)
        
        # Serialize the results
        candidates_data = []
        for candidate in queryset:
            candidates_data.append({
                "id": str(candidate.id),
                "name": candidate.name,
                "skills": candidate.skills,
                "fe_score": candidate.fe_score,
                "be_score": candidate.be_score,
                "seniority": candidate.seniority,
                "qualifications": candidate.qualifications,
                "created_at": candidate.created_at.isoformat(),
                "updated_at": candidate.updated_at.isoformat()
            })
        
        return JsonResponse({
            "candidates": candidates_data,
            "total_count": len(candidates_data),
            "filters_applied": {
                "skills": skills_filter,
                "seniority": seniority_filter,
                "qualifications": qualifications_filter,
                "fe_score_min": fe_score_min,
                "be_score_min": be_score_min
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return JsonResponse(
            {"error": f"Internal server error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

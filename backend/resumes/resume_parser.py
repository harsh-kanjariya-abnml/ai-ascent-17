"""
Resume parser service module.
This module provides functionality to parse PDF resumes and extract structured data using LLM.
"""

import re
import json
import os
from typing import Dict, Any, List
import PyPDF2
import openai
from django.conf import settings

# Configure OpenAI (you can also use other LLM providers)
openai.api_key = getattr(settings, 'OPENAI_API_KEY', os.environ.get('OPENAI_API_KEY'))

def process_resume(pdf_file) -> Dict[str, Any]:
    """
    Process a PDF resume file and extract structured data using LLM.
    
    Args:
        pdf_file: The uploaded PDF file
        
    Returns:
        Dict containing extracted resume data
    """
    try:
        # Step 1: Convert PDF to text
        text_content = extract_text_from_pdf(pdf_file)
        
        if not text_content.strip():
            raise Exception("Could not extract text from PDF file")
        
        # Step 2: Use LLM to extract structured data
        extracted_data = extract_data_with_llm(text_content)
        
        return extracted_data
        
    except Exception as e:
        raise Exception(f"Error processing resume: {str(e)}")


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text content from PDF file.
    
    Args:
        pdf_file: The uploaded PDF file
        
    Returns:
        str: Extracted text content
    """
    try:
        # Reset file pointer to beginning
        pdf_file.seek(0)
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text_content = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"
        
        return text_content.strip()
        
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_data_with_llm(text_content: str) -> Dict[str, Any]:
    """
    Use LLM to extract structured data from resume text.
    
    Args:
        text_content: The extracted text from PDF
        
    Returns:
        Dict containing structured candidate data
    """
    try:
        # Create prompt for LLM
        prompt = create_extraction_prompt(text_content)
        
        # Call OpenAI API (you can replace this with other LLM providers)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a resume parsing assistant. Extract candidate information and return it as valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        # Parse LLM response
        llm_response = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        extracted_data = parse_llm_response(llm_response)
        
        # Validate and normalize the data
        normalized_data = normalize_extracted_data(extracted_data)
        
        return normalized_data
        
    except Exception as e:
        # Fallback to rule-based extraction if LLM fails
        print(f"LLM extraction failed: {str(e)}, falling back to rule-based extraction")
        return fallback_extraction(text_content)


def create_extraction_prompt(text_content: str) -> str:
    """
    Create a prompt for LLM to extract candidate information.
    
    Args:
        text_content: The resume text content
        
    Returns:
        str: Formatted prompt for LLM
    """
    prompt = f"""
    Please analyze the following resume text and extract candidate information. Return the data as valid JSON with the following structure:

    {{
        "name": "candidate's full name",
        "skills": ["list", "of", "technical", "skills"],
        "seniority": "junior|mid|senior|lead|principal",
        "qualifications": "high_school|bachelors|masters|phd|diploma|certification"
    }}

    Guidelines:
    1. For seniority: Determine based on job titles, years of experience, and responsibilities
    2. For qualifications: Extract the highest educational qualification
    3. For skills: Focus on technical skills, programming languages, frameworks, tools
    4. Return ONLY the JSON object, no additional text

    Resume text:
    {text_content}
    """
    return prompt


def parse_llm_response(llm_response: str) -> Dict[str, Any]:
    """
    Parse the LLM response and extract JSON data.
    
    Args:
        llm_response: Raw response from LLM
        
    Returns:
        Dict containing parsed data
    """
    try:
        # Try to find JSON in the response
        json_start = llm_response.find('{')
        json_end = llm_response.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = llm_response[json_start:json_end]
            return json.loads(json_str)
        else:
            raise Exception("No valid JSON found in LLM response")
            
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON from LLM response: {str(e)}")


def normalize_extracted_data(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and validate the extracted data.
    
    Args:
        extracted_data: Raw extracted data from LLM
        
    Returns:
        Dict containing normalized data
    """
    # Valid choices
    valid_seniorities = ['junior', 'mid', 'senior', 'lead', 'principal']
    valid_qualifications = ['high_school', 'bachelors', 'masters', 'phd', 'diploma', 'certification']
    
    # Normalize name
    name = extracted_data.get('name', 'Unknown').strip()
    if not name or name.lower() == 'unknown':
        name = 'Unknown'
    
    # Normalize skills
    skills = extracted_data.get('skills', [])
    if not isinstance(skills, list):
        skills = []
    skills = [skill.strip() for skill in skills if skill.strip()]
    
    # Normalize seniority
    seniority = extracted_data.get('seniority', 'mid').lower().strip()
    if seniority not in valid_seniorities:
        seniority = 'mid'  # Default fallback
    
    # Normalize qualifications
    qualifications = extracted_data.get('qualifications', 'bachelors').lower().strip()
    if qualifications not in valid_qualifications:
        qualifications = 'bachelors'  # Default fallback
    
    # Calculate scores based on skills and seniority
    fe_score = calculate_fe_score_from_data(skills, seniority)
    be_score = calculate_be_score_from_data(skills, seniority)
    
    return {
        'name': name,
        'skills': skills,
        'fe_score': fe_score,
        'be_score': be_score,
        'seniority': seniority,
        'qualifications': qualifications
    }


def calculate_fe_score_from_data(skills: List[str], seniority: str) -> int:
    """Calculate frontend score based on skills and seniority."""
    fe_skills = [
        'react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css',
        'frontend', 'front-end', 'ui', 'ux', 'responsive', 'bootstrap', 'sass',
        'webpack', 'babel', 'npm', 'yarn', 'redux', 'mobx', 'jquery', 'next.js',
        'nuxt.js', 'svelte', 'ember', 'backbone', 'material-ui', 'tailwind'
    ]
    
    score = 0
    skills_lower = [skill.lower() for skill in skills]
    
    # Score based on skills
    for skill in fe_skills:
        if any(skill in s for s in skills_lower):
            score += 10
    
    # Bonus for seniority
    seniority_bonus = {
        'junior': 5,
        'mid': 10,
        'senior': 20,
        'lead': 30,
        'principal': 30
    }
    score += seniority_bonus.get(seniority, 10)
    
    return min(score, 100)


def calculate_be_score_from_data(skills: List[str], seniority: str) -> int:
    """Calculate backend score based on skills and seniority."""
    be_skills = [
        'python', 'django', 'flask', 'fastapi', 'node.js', 'express', 'java',
        'spring', 'c#', '.net', 'ruby', 'rails', 'php', 'laravel', 'go',
        'rust', 'backend', 'back-end', 'api', 'database', 'sql', 'mongodb',
        'postgresql', 'mysql', 'redis', 'elasticsearch', 'microservices',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'serverless', 'graphql',
        'rest', 'grpc', 'kafka', 'rabbitmq', 'nginx', 'apache'
    ]
    
    score = 0
    skills_lower = [skill.lower() for skill in skills]
    
    # Score based on skills
    for skill in be_skills:
        if any(skill in s for s in skills_lower):
            score += 10
    
    # Bonus for seniority
    seniority_bonus = {
        'junior': 5,
        'mid': 10,
        'senior': 20,
        'lead': 30,
        'principal': 30
    }
    score += seniority_bonus.get(seniority, 10)
    
    return min(score, 100)


def fallback_extraction(text_content: str) -> Dict[str, Any]:
    """
    Fallback rule-based extraction if LLM fails.
    
    Args:
        text_content: The resume text content
        
    Returns:
        Dict containing extracted data using rule-based approach
    """
    return {
        'name': _extract_name_fallback(text_content),
        'skills': _extract_skills_fallback(text_content),
        'fe_score': _calculate_fe_score_fallback(text_content),
        'be_score': _calculate_be_score_fallback(text_content),
        'seniority': _extract_seniority_fallback(text_content),
        'qualifications': _extract_qualifications_fallback(text_content)
    }


def _extract_name_fallback(text: str) -> str:
    """Extract name using rule-based approach."""
    lines = text.strip().split('\n')
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if line and not '@' in line and not '+' in line and len(line) < 50:
            # Simple name validation
            words = line.split()
            if 2 <= len(words) <= 4 and all(word.isalpha() or word.replace('.', '').isalpha() for word in words):
                return line
    return "Unknown"


def _extract_skills_fallback(text: str) -> List[str]:
    """Extract skills using rule-based approach."""
    common_skills = [
        'Python', 'JavaScript', 'React', 'Django', 'Node.js', 'Java', 'C++', 'C#',
        'AWS', 'Docker', 'Kubernetes', 'Machine Learning', 'SQL', 'MongoDB',
        'Git', 'Linux', 'HTML', 'CSS', 'TypeScript', 'Vue.js', 'Angular',
        'Flask', 'FastAPI', 'PostgreSQL', 'Redis', 'GraphQL', 'REST API'
    ]
    
    found_skills = []
    text_upper = text.upper()
    
    for skill in common_skills:
        if skill.upper() in text_upper:
            found_skills.append(skill)
    
    return found_skills


def _calculate_fe_score_fallback(text: str) -> int:
    """Calculate frontend score using rule-based approach."""
    return calculate_fe_score_from_data(_extract_skills_fallback(text), _extract_seniority_fallback(text))


def _calculate_be_score_fallback(text: str) -> int:
    """Calculate backend score using rule-based approach."""
    return calculate_be_score_from_data(_extract_skills_fallback(text), _extract_seniority_fallback(text))


def _extract_seniority_fallback(text: str) -> str:
    """Extract seniority using rule-based approach."""
    text_lower = text.lower()
    
    if 'senior' in text_lower or 'sr.' in text_lower:
        return 'senior'
    elif 'principal' in text_lower or 'architect' in text_lower:
        return 'principal'
    elif 'lead' in text_lower:
        return 'lead'
    elif 'junior' in text_lower or 'entry' in text_lower or 'jr.' in text_lower:
        return 'junior'
    else:
        return 'mid'


def _extract_qualifications_fallback(text: str) -> str:
    """Extract qualifications using rule-based approach."""
    text_lower = text.lower()
    
    if 'phd' in text_lower or 'doctorate' in text_lower or 'ph.d' in text_lower:
        return 'phd'
    elif 'master' in text_lower or 'mba' in text_lower or 'm.s' in text_lower or 'm.a' in text_lower:
        return 'masters'
    elif 'bachelor' in text_lower or 'b.s' in text_lower or 'b.a' in text_lower or 'b.tech' in text_lower:
        return 'bachelors'
    elif 'diploma' in text_lower:
        return 'diploma'
    elif 'certificate' in text_lower or 'certification' in text_lower:
        return 'certification'
    else:
        return 'bachelors' 
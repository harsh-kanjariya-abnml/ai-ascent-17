"""
Resume parser service module.
This module provides functionality to parse PDF resumes and extract structured data.
"""

import re
from typing import Dict, Any, List

def process_resume(pdf_file) -> Dict[str, Any]:
    """
    Process a PDF resume file and extract structured data.
    
    Args:
        pdf_file: The uploaded PDF file
        
    Returns:
        Dict containing extracted resume data
    """
    # This is a mock implementation. In a real scenario, you would use
    # libraries like PyPDF2, pdfplumber, or AI services to extract text
    # and then parse it to extract structured information.
    
    try:
        # Mock extracted text (in real implementation, extract from PDF)
        mock_text = """
        John Doe
        
        Senior Software Engineer with 8 years of experience in Python, Django, React, JavaScript.
        Experience in cloud technologies and machine learning.
        Strong in both frontend and backend development.
        
        Education:
        Bachelor's Degree in Computer Science
        
        Skills:
        Python, Django, React, JavaScript, AWS, Docker, Machine Learning
        """
        
        # Extract structured data (this would be more sophisticated in real implementation)
        extracted_data = {
            'name': _extract_name(mock_text),
            'skills': _extract_skills(mock_text),
            'fe_score': _calculate_fe_score(mock_text),
            'be_score': _calculate_be_score(mock_text),
            'seniority': _extract_seniority(mock_text),
            'qualifications': _extract_qualifications(mock_text)
        }
        
        return extracted_data
        
    except Exception as e:
        raise Exception(f"Error processing resume: {str(e)}")


def _extract_name(text: str) -> str:
    """Extract name from resume text."""
    lines = text.strip().split('\n')
    # Assume first non-empty line is the name
    for line in lines:
        line = line.strip()
        if line and not '@' in line and not '+' in line and len(line) < 50:
            return line
    return "Unknown"


def _extract_skills(text: str) -> List[str]:
    """Extract skills from resume text."""
    # Common tech skills - in real implementation, use NLP or predefined skill sets
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


def _calculate_fe_score(text: str) -> int:
    """Calculate frontend score based on skills and experience."""
    text_lower = text.lower()
    fe_skills = [
        'react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css',
        'frontend', 'front-end', 'ui', 'ux', 'responsive', 'bootstrap', 'sass',
        'webpack', 'babel', 'npm', 'yarn', 'redux', 'mobx', 'jquery'
    ]
    
    score = 0
    for skill in fe_skills:
        if skill in text_lower:
            score += 10
    
    # Bonus for experience level
    if 'senior' in text_lower:
        score += 20
    elif 'lead' in text_lower or 'principal' in text_lower:
        score += 30
    elif 'junior' in text_lower:
        score += 5
    else:
        score += 10
    
    # Cap at 100
    return min(score, 100)


def _calculate_be_score(text: str) -> int:
    """Calculate backend score based on skills and experience."""
    text_lower = text.lower()
    be_skills = [
        'python', 'django', 'flask', 'fastapi', 'node.js', 'express', 'java',
        'spring', 'c#', '.net', 'ruby', 'rails', 'php', 'laravel', 'go',
        'rust', 'backend', 'back-end', 'api', 'database', 'sql', 'mongodb',
        'postgresql', 'mysql', 'redis', 'elasticsearch', 'microservices',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'serverless'
    ]
    
    score = 0
    for skill in be_skills:
        if skill in text_lower:
            score += 10
    
    # Bonus for experience level
    if 'senior' in text_lower:
        score += 20
    elif 'lead' in text_lower or 'principal' in text_lower:
        score += 30
    elif 'junior' in text_lower:
        score += 5
    else:
        score += 10
    
    # Cap at 100
    return min(score, 100)


def _extract_seniority(text: str) -> str:
    """Extract seniority level from resume text."""
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


def _extract_qualifications(text: str) -> str:
    """Extract highest qualification from resume text."""
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
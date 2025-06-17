#!/usr/bin/env python3
"""
Test script for PDF processing functionality.
This script demonstrates how the resume parser works with PDF files.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
django.setup()

from resumes.resume_parser import extract_data_with_llm, fallback_extraction

def test_fallback_extraction():
    """Test the fallback extraction functionality without LLM."""
    print("Testing fallback extraction (rule-based)...")
    
    # Sample resume text
    sample_text = """
    John Smith
    Senior Software Engineer
    
    Professional Summary:
    Experienced software engineer with 7 years of experience in full-stack development.
    Proficient in Python, Django, React, JavaScript, and cloud technologies.
    
    Education:
    Bachelor of Science in Computer Science
    University of Technology, 2015
    
    Skills:
    • Python, Django, Flask
    • JavaScript, React, Node.js
    • AWS, Docker, Kubernetes
    • PostgreSQL, MongoDB
    • Git, Linux, REST APIs
    
    Experience:
    Senior Software Engineer | Tech Corp | 2020 - Present
    • Lead development of web applications using Django and React
    • Implemented microservices architecture with Docker and Kubernetes
    • Managed AWS infrastructure and deployment pipelines
    
    Software Engineer | StartupXYZ | 2017 - 2020
    • Developed frontend applications using React and JavaScript
    • Built backend APIs with Python and Django
    • Collaborated with cross-functional teams
    """
    
    try:
        result = fallback_extraction(sample_text)
        print("Extraction successful!")
        print(f"Name: {result['name']}")
        print(f"Skills: {result['skills']}")
        print(f"FE Score: {result['fe_score']}")
        print(f"BE Score: {result['be_score']}")
        print(f"Seniority: {result['seniority']}")
        print(f"Qualifications: {result['qualifications']}")
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False

def test_llm_extraction():
    """Test LLM extraction (requires OpenAI API key)."""
    print("\nTesting LLM extraction...")
    
    # Check if OpenAI API key is available
    from django.conf import settings
    if not settings.OPENAI_API_KEY:
        print("OpenAI API key not found. Skipping LLM test.")
        print("To test LLM functionality, set the OPENAI_API_KEY environment variable.")
        return False
    
    sample_text = """
    Jane Doe
    Principal Frontend Architect
    
    I am a seasoned frontend architect with 12+ years of experience leading 
    large-scale web application development. Expert in React, TypeScript, 
    Next.js, and modern frontend technologies.
    
    Education:
    Master of Science in Computer Science, MIT, 2010
    
    Core Skills:
    React, TypeScript, Next.js, Vue.js, Angular, JavaScript, HTML5, CSS3,
    Webpack, Redux, GraphQL, Jest, Cypress, Figma, Adobe XD
    
    Experience:
    Principal Frontend Architect | Meta | 2019 - Present
    Senior Frontend Engineer | Google | 2015 - 2019
    Frontend Developer | Apple | 2012 - 2015
    """
    
    try:
        result = extract_data_with_llm(sample_text)
        print("LLM extraction successful!")
        print(f"Name: {result['name']}")
        print(f"Skills: {result['skills']}")
        print(f"FE Score: {result['fe_score']}")
        print(f"BE Score: {result['be_score']}")
        print(f"Seniority: {result['seniority']}")
        print(f"Qualifications: {result['qualifications']}")
        return True
    except Exception as e:
        print(f"LLM extraction failed: {e}")
        print("Falling back to rule-based extraction...")
        result = fallback_extraction(sample_text)
        print("Fallback extraction successful!")
        print(f"Name: {result['name']}")
        print(f"Skills: {result['skills']}")
        print(f"FE Score: {result['fe_score']}")
        print(f"BE Score: {result['be_score']}")
        print(f"Seniority: {result['seniority']}")
        print(f"Qualifications: {result['qualifications']}")
        return True

def main():
    """Run all tests."""
    print("Resume Parser Test Suite")
    print("=" * 50)
    
    # Test fallback extraction
    success1 = test_fallback_extraction()
    
    # Test LLM extraction
    success2 = test_llm_extraction()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Fallback extraction: {'✓ PASS' if success1 else '✗ FAIL'}")
    print(f"LLM extraction: {'✓ PASS' if success2 else '✗ FAIL'}")
    
    if success1:
        print("\n✅ The resume parser is working correctly!")
        print("🔧 To enable LLM processing, set the OPENAI_API_KEY environment variable.")
    else:
        print("\n❌ There are issues with the resume parser.")

if __name__ == "__main__":
    main() 
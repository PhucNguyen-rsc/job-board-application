import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv(dotenv_path='../../.env')

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_suggestions(self, job, applicant):
        prompt = f"""
        Analyze this job application match and provide tailored suggestions:
        
        Job Details:
        - Title: {job['title']}
        - Company: {job['company']}
        - Location: {job['location']}
        - Industry: {job['industry']}
        - Required Experience: {job['seniority']} years
        
        Applicant Details:
        - Name: {applicant['first']} {applicant['last']}
        - Expertise: {applicant['expertise']}
        - Experience: {applicant['years']} years
        
        Provide:
        1. A match score percentage (0-100%)
        2. 3-5 specific improvement suggestions
        3. Key strengths to highlight
        
        Format your response as JSON with:
        {{
            "matchScore": number,
            "analysis": string,
            "suggestions": [string],
            "strengths": [string]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse the response text into JSON
            return self._parse_response(response.text)
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            return {
                "matchScore": 0,
                "analysis": "Could not generate analysis",
                "suggestions": [],
                "strengths": []
            }
    
    def _parse_response(self, response_text):
        # Gemini returns markdown with ```json ``` wrappers
        if '```json' in response_text:
            json_part = response_text.split('```json')[1].split('```')[0]
            return eval(json_part)
        return eval(response_text)
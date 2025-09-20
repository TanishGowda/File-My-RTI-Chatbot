#!/usr/bin/env python3
"""
Script to upload RTI PDFs with clean text extraction
This version fixes character encoding issues
"""

import asyncio
import sys
import os
import requests
from pathlib import Path

# Add the backend directory to Python path
sys.path.append('.')

# Backend URL
BACKEND_URL = "http://localhost:8000"

# PDF files with their details
PDF_FILES = [
    {
        "file_path": "../Dharani Telangana Land Related RTI Format.pdf",
        "title": "Dharani Telangana Land Related RTI Format",
        "description": "RTI application format for land-related queries in Telangana through Dharani portal",
        "rti_category": "land_records",
        "rti_department": "Telangana Revenue Department"
    },
    {
        "file_path": "../Passport Delay.pdf",
        "title": "Passport Delay RTI Format",
        "description": "RTI application format for passport delay queries",
        "rti_category": "passport",
        "rti_department": "Ministry of External Affairs"
    },
    {
        "file_path": "../Examination Verification.pdf",
        "title": "Examination Verification RTI Format",
        "description": "RTI application format for examination result verification",
        "rti_category": "education",
        "rti_department": "Education Board/University"
    },
    {
        "file_path": "../Employment Verification.pdf",
        "title": "Employment Verification RTI Format",
        "description": "RTI application format for employment verification queries",
        "rti_category": "employment",
        "rti_department": "Department of Personnel and Training"
    },
    {
        "file_path": "../Pension Related.pdf",
        "title": "Pension Related RTI Format",
        "description": "RTI application format for pension-related queries",
        "rti_category": "pension",
        "rti_department": "Department of Pension and Pensioners' Welfare"
    },
    {
        "file_path": "../Property Tax.pdf",
        "title": "Property Tax RTI Format",
        "description": "RTI application format for property tax queries",
        "rti_category": "municipal",
        "rti_department": "Municipal Corporation"
    },
    {
        "file_path": "../Income Tax.pdf",
        "title": "Income Tax RTI Format",
        "description": "RTI application format for income tax queries",
        "rti_category": "taxation",
        "rti_department": "Income Tax Department"
    },
    {
        "file_path": "../Police Complaint.pdf",
        "title": "Police Complaint RTI Format",
        "description": "RTI application format for police complaint queries",
        "rti_category": "police",
        "rti_department": "Police Department"
    },
    {
        "file_path": "../Court Case Status.pdf",
        "title": "Court Case Status RTI Format",
        "description": "RTI application format for court case status queries",
        "rti_category": "judiciary",
        "rti_department": "High Court/District Court"
    },
    {
        "file_path": "../Aadhaar Related.pdf",
        "title": "Aadhaar Related RTI Format",
        "description": "RTI application format for Aadhaar-related queries",
        "rti_category": "identity",
        "rti_department": "Unique Identification Authority of India (UIDAI)"
    },
    {
        "file_path": "../Banking Related.pdf",
        "title": "Banking Related RTI Format",
        "description": "RTI application format for banking-related queries",
        "rti_category": "banking",
        "rti_department": "Reserve Bank of India"
    },
    {
        "file_path": "../Healthcare Related.pdf",
        "title": "Healthcare Related RTI Format",
        "description": "RTI application format for healthcare-related queries",
        "rti_category": "healthcare",
        "rti_department": "Ministry of Health and Family Welfare"
    },
    {
        "file_path": "../Transport Related.pdf",
        "title": "Transport Related RTI Format",
        "description": "RTI application format for transport-related queries",
        "rti_category": "transport",
        "rti_department": "Ministry of Road Transport and Highways"
    },
    {
        "file_path": "../Environment Related.pdf",
        "title": "Environment Related RTI Format",
        "description": "RTI application format for environment-related queries",
        "rti_category": "environment",
        "rti_department": "Ministry of Environment, Forest and Climate Change"
    },
    {
        "file_path": "../Social Welfare.pdf",
        "title": "Social Welfare RTI Format",
        "description": "RTI application format for social welfare queries",
        "rti_category": "social_welfare",
        "rti_department": "Ministry of Social Justice and Empowerment"
    },
    {
        "file_path": "../Rural Development.pdf",
        "title": "Rural Development RTI Format",
        "description": "RTI application format for rural development queries",
        "rti_category": "rural_development",
        "rti_department": "Ministry of Rural Development"
    },
    {
        "file_path": "../Urban Development.pdf",
        "title": "Urban Development RTI Format",
        "description": "RTI application format for urban development queries",
        "rti_category": "urban_development",
        "rti_department": "Ministry of Housing and Urban Affairs"
    },
    {
        "file_path": "../Women and Child Development.pdf",
        "title": "Women and Child Development RTI Format",
        "description": "RTI application format for women and child development queries",
        "rti_category": "women_child",
        "rti_department": "Ministry of Women and Child Development"
    },
    {
        "file_path": "../Labour and Employment.pdf",
        "title": "Labour and Employment RTI Format",
        "description": "RTI application format for labour and employment queries",
        "rti_category": "labour",
        "rti_department": "Ministry of Labour and Employment"
    },
    {
        "file_path": "../Agriculture Related.pdf",
        "title": "Agriculture Related RTI Format",
        "description": "RTI application format for agriculture-related queries",
        "rti_category": "agriculture",
        "rti_department": "Ministry of Agriculture and Farmers Welfare"
    },
    {
        "file_path": "../Food and Civil Supplies.pdf",
        "title": "Food and Civil Supplies RTI Format",
        "description": "RTI application format for food and civil supplies queries",
        "rti_category": "food_supplies",
        "rti_department": "Ministry of Consumer Affairs, Food and Public Distribution"
    },
    {
        "file_path": "../Water Resources.pdf",
        "title": "Water Resources RTI Format",
        "description": "RTI application format for water resources queries",
        "rti_category": "water_resources",
        "rti_department": "Ministry of Jal Shakti"
    },
    {
        "file_path": "../Power and Energy.pdf",
        "title": "Power and Energy RTI Format",
        "description": "RTI application format for power and energy queries",
        "rti_category": "power_energy",
        "rti_department": "Ministry of Power"
    },
    {
        "file_path": "../Telecommunications.pdf",
        "title": "Telecommunications RTI Format",
        "description": "RTI application format for telecommunications queries",
        "rti_category": "telecom",
        "rti_department": "Ministry of Communications"
    },
    {
        "file_path": "../Science and Technology.pdf",
        "title": "Science and Technology RTI Format",
        "description": "RTI application format for science and technology queries",
        "rti_category": "science_tech",
        "rti_department": "Ministry of Science and Technology"
    },
    {
        "file_path": "../Defence Related.pdf",
        "title": "Defence Related RTI Format",
        "description": "RTI application format for defence-related queries",
        "rti_category": "defence",
        "rti_department": "Ministry of Defence"
    },
    {
        "file_path": "../Home Affairs.pdf",
        "title": "Home Affairs RTI Format",
        "description": "RTI application format for home affairs queries",
        "rti_category": "home_affairs",
        "rti_department": "Ministry of Home Affairs"
    },
    {
        "file_path": "../External Affairs.pdf",
        "title": "External Affairs RTI Format",
        "description": "RTI application format for external affairs queries",
        "rti_category": "external_affairs",
        "rti_department": "Ministry of External Affairs"
    },
    {
        "file_path": "../Finance Related.pdf",
        "title": "Finance Related RTI Format",
        "description": "RTI application format for finance-related queries",
        "rti_category": "finance",
        "rti_department": "Ministry of Finance"
    },
    {
        "file_path": "../Commerce and Industry.pdf",
        "title": "Commerce and Industry RTI Format",
        "description": "RTI application format for commerce and industry queries",
        "rti_category": "commerce_industry",
        "rti_department": "Ministry of Commerce and Industry"
    },
    {
        "file_path": "../Railways.pdf",
        "title": "Railways RTI Format",
        "description": "RTI application format for railways queries",
        "rti_category": "railways",
        "rti_department": "Ministry of Railways"
    },
    {
        "file_path": "../Civil Aviation.pdf",
        "title": "Civil Aviation RTI Format",
        "description": "RTI application format for civil aviation queries",
        "rti_category": "civil_aviation",
        "rti_department": "Ministry of Civil Aviation"
    }
]

async def upload_pdf(pdf_info):
    """Upload a single PDF with clean text extraction"""
    try:
        file_path = Path(pdf_info["file_path"])
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"📤 Uploading: {pdf_info['title']}")
        
        # Prepare the file and form data
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'application/pdf')}
            data = {
                'title': pdf_info['title'],
                'description': pdf_info['description'],
                'rti_category': pdf_info['rti_category'],
                'rti_department': pdf_info['rti_department']
            }
            headers = {'Authorization': 'Bearer test-token'}
            
            # Upload the file
            response = requests.post(
                f"{BACKEND_URL}/api/v1/chat/upload-pdf",
                files=files,
                data=data,
                headers=headers,
                timeout=60
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Success: {pdf_info['title']}")
                return True
            else:
                print(f"❌ Upload failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading {pdf_info['title']}: {e}")
        return False

async def main():
    print("🚀 Starting clean PDF upload process...")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/chat/conversations", 
                              headers={'Authorization': 'Bearer test-token'}, 
                              timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not running. Please start it first:")
            print("   cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Please make sure the backend is running on http://localhost:8000")
        return
    
    print("✅ Backend is running")
    print()
    
    # Upload PDFs
    success_count = 0
    total_count = len(PDF_FILES)
    
    for i, pdf_info in enumerate(PDF_FILES, 1):
        print(f"[{i}/{total_count}] ", end="")
        success = await upload_pdf(pdf_info)
        if success:
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 Upload Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {total_count - success_count}")
    print(f"   📈 Success Rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count > 0:
        print("\n🎉 PDFs uploaded successfully with clean text extraction!")
        print("   The character encoding issues should now be fixed.")
        print("   You can test the chatbot to see clean RTI applications.")

if __name__ == "__main__":
    asyncio.run(main())

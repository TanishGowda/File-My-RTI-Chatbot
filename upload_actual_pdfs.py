#!/usr/bin/env python3
"""
Script to upload actual RTI PDFs with clean text extraction
This version uses the actual PDF files found in the directory
"""

import asyncio
import sys
import os
import requests
from pathlib import Path

# Add the backend directory to Python path
sys.path.append('backend')

# Change to backend directory for imports
os.chdir('backend')

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Actual PDF files with their details (matching the files found)
PDF_FILES = [
    {
        "file_path": "Certified documents from government offices or departments.pdf",
        "title": "Certified Documents from Government Offices RTI Format",
        "description": "RTI application format for obtaining certified documents from government offices",
        "rti_category": "government_documents",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Citizen Charter of Government offices.pdf",
        "title": "Citizen Charter RTI Format",
        "description": "RTI application format for citizen charter related queries",
        "rti_category": "citizen_services",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Complaint Tracking.pdf",
        "title": "Complaint Tracking RTI Format",
        "description": "RTI application format for complaint tracking queries",
        "rti_category": "complaints",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Custom Request.pdf",
        "title": "Custom Request RTI Format",
        "description": "RTI application format for custom requests",
        "rti_category": "custom_requests",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Dharani Telangana Land related issues.pdf",
        "title": "Dharani Telangana Land Related RTI Format",
        "description": "RTI application format for land-related queries in Telangana through Dharani portal",
        "rti_category": "land_records",
        "rti_department": "Telangana Revenue Department"
    },
    {
        "file_path": "Encumberance Certificate.pdf",
        "title": "Encumbrance Certificate RTI Format",
        "description": "RTI application format for encumbrance certificate queries",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    {
        "file_path": "EPF Status.pdf",
        "title": "EPF Status RTI Format",
        "description": "RTI application format for EPF status queries",
        "rti_category": "employment",
        "rti_department": "Employees' Provident Fund Organisation"
    },
    {
        "file_path": "FIR Copy.pdf",
        "title": "FIR Copy RTI Format",
        "description": "RTI application format for obtaining FIR copies",
        "rti_category": "police",
        "rti_department": "Police Department"
    },
    {
        "file_path": "First Appeal Template.pdf",
        "title": "First Appeal RTI Format",
        "description": "RTI application format for first appeal",
        "rti_category": "appeals",
        "rti_department": "First Appellate Authority"
    },
    {
        "file_path": "Fund Utilization.pdf",
        "title": "Fund Utilization RTI Format",
        "description": "RTI application format for fund utilization queries",
        "rti_category": "finance",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Gram Panchayath Inquiry.pdf",
        "title": "Gram Panchayat Inquiry RTI Format",
        "description": "RTI application format for gram panchayat related queries",
        "rti_category": "rural_development",
        "rti_department": "Gram Panchayat"
    },
    {
        "file_path": "Income Tax Refund.pdf",
        "title": "Income Tax Refund RTI Format",
        "description": "RTI application format for income tax refund queries",
        "rti_category": "taxation",
        "rti_department": "Income Tax Department"
    },
    {
        "file_path": "IRCTC Refund issues.pdf",
        "title": "IRCTC Refund RTI Format",
        "description": "RTI application format for IRCTC refund issues",
        "rti_category": "railways",
        "rti_department": "Indian Railway Catering and Tourism Corporation"
    },
    {
        "file_path": "Khasra Pahani Records.pdf",
        "title": "Khasra Pahani Records RTI Format",
        "description": "RTI application format for khasra pahani records",
        "rti_category": "land_records",
        "rti_department": "Revenue Department"
    },
    {
        "file_path": "Land Survey related rti.pdf",
        "title": "Land Survey RTI Format",
        "description": "RTI application format for land survey related queries",
        "rti_category": "land_records",
        "rti_department": "Survey Department"
    },
    {
        "file_path": "Link document realted rti.pdf",
        "title": "Link Document RTI Format",
        "description": "RTI application format for link document related queries",
        "rti_category": "documentation",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Marksheet Verification.pdf",
        "title": "Marksheet Verification RTI Format",
        "description": "RTI application format for marksheet verification",
        "rti_category": "education",
        "rti_department": "Education Board/University"
    },
    {
        "file_path": "Meebhoomi Andhra pradesh land related rti.pdf",
        "title": "Meebhoomi Andhra Pradesh Land Related RTI Format",
        "description": "RTI application format for land-related queries in Andhra Pradesh through Meebhoomi",
        "rti_category": "land_records",
        "rti_department": "Andhra Pradesh Revenue Department"
    },
    {
        "file_path": "Minicipality related rti.pdf",
        "title": "Municipality Related RTI Format",
        "description": "RTI application format for municipality related queries",
        "rti_category": "municipal",
        "rti_department": "Municipal Corporation"
    },
    {
        "file_path": "MP MLA Fund utilization.pdf",
        "title": "MP MLA Fund Utilization RTI Format",
        "description": "RTI application format for MP/MLA fund utilization queries",
        "rti_category": "finance",
        "rti_department": "Ministry of Parliamentary Affairs"
    },
    {
        "file_path": "Mutation Realted RTI.pdf",
        "title": "Mutation Related RTI Format",
        "description": "RTI application format for mutation related queries",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    {
        "file_path": "Passport Delay.pdf",
        "title": "Passport Delay RTI Format",
        "description": "RTI application format for passport delay queries",
        "rti_category": "passport",
        "rti_department": "Ministry of External Affairs"
    },
    {
        "file_path": "Pension Inquiry tracking.pdf",
        "title": "Pension Inquiry Tracking RTI Format",
        "description": "RTI application format for pension inquiry tracking",
        "rti_category": "pension",
        "rti_department": "Department of Pension and Pensioners' Welfare"
    },
    {
        "file_path": "Public Transport Related RTI.pdf",
        "title": "Public Transport Related RTI Format",
        "description": "RTI application format for public transport related queries",
        "rti_category": "transport",
        "rti_department": "Ministry of Road Transport and Highways"
    },
    {
        "file_path": "Refund from Government offices or departments.pdf",
        "title": "Government Refund RTI Format",
        "description": "RTI application format for refunds from government offices",
        "rti_category": "finance",
        "rti_department": "Various Government Departments"
    },
    {
        "file_path": "Registration Refund Related RTI.pdf",
        "title": "Registration Refund RTI Format",
        "description": "RTI application format for registration refund queries",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    {
        "file_path": "Road Work Related RTI.pdf",
        "title": "Road Work Related RTI Format",
        "description": "RTI application format for road work related queries",
        "rti_category": "infrastructure",
        "rti_department": "Public Works Department"
    },
    {
        "file_path": "RTA Related Queries.pdf",
        "title": "RTA Related Queries RTI Format",
        "description": "RTI application format for RTA related queries",
        "rti_category": "transport",
        "rti_department": "Regional Transport Authority"
    },
    {
        "file_path": "Sale deed copies.pdf",
        "title": "Sale Deed Copies RTI Format",
        "description": "RTI application format for sale deed copies",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    {
        "file_path": "Second Appeal Templae.pdf",
        "title": "Second Appeal RTI Format",
        "description": "RTI application format for second appeal",
        "rti_category": "appeals",
        "rti_department": "Second Appellate Authority"
    },
    {
        "file_path": "Street lights related rti.pdf",
        "title": "Street Lights Related RTI Format",
        "description": "RTI application format for street lights related queries",
        "rti_category": "municipal",
        "rti_department": "Municipal Corporation"
    },
    {
        "file_path": "Toll Collection related rti.pdf",
        "title": "Toll Collection Related RTI Format",
        "description": "RTI application format for toll collection related queries",
        "rti_category": "transport",
        "rti_department": "National Highways Authority of India"
    }
]

async def upload_pdf(pdf_info):
    """Upload a single PDF with clean text extraction"""
    try:
        file_path = Path(f"../{pdf_info['file_path']}")
        
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
    print("🚀 Starting clean PDF upload process with actual files...")
    print("=" * 70)
    
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
    
    print("=" * 70)
    print(f"📊 Upload Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {total_count - success_count}")
    print(f"   📈 Success Rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count > 0:
        print("\n🎉 PDFs uploaded successfully with clean text extraction!")
        print("   The character encoding issues should now be fixed.")
        print("   You can test the chatbot to see clean RTI applications.")
        print("\n💡 Test with queries like:")
        print("   - 'examination verification'")
        print("   - 'passport delay'")
        print("   - 'land records'")
        print("   - 'FIR copy'")

if __name__ == "__main__":
    asyncio.run(main())

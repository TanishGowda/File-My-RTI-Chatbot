import requests
import os

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1/chat"
SUPABASE_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InBiSjdjWHVNYWVYb2k1cmoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3luaGpqYm1ycWF1ZmZkcHl6dG9rLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4NTU4NzAyYy01NDM3LTQ3YjgtODdlMi1lNzA1NzZkMWM3N2QiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU4MDkzMTk1LCJpYXQiOjE3NTgwODk1OTUsImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoidGFuaXNoMjVnb3dkYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiVGFuaXNoIE5hdmVlbiBHb3dkYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiODU1ODcwMmMtNTQzNy00N2I4LTg3ZTItZTcwNTc2ZDFjNzdkIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTgwODk1OTV9XSwic2Vzc2lvbl9pZCI6ImQ2MDQwNGFjLTk5OWEtNDU3Ny05NTEyLTBlMGM0MGE2ZmE5NiIsImlzX2Fub255bW91cyI6ZmFsc2V9.lRCxHPwLhR2wxrqjt82MdFNIHGMnJYin96EkcZVaBXM"

# PDF files to upload
pdf_files = [
    # Land Records & Property Related
    {
        "file_path": "Dharani Telangana Land related issues.pdf",
        "title": "Dharani Telangana Land Related RTI Format",
        "description": "RTI format for land-related issues in Telangana Dharani system",
        "rti_category": "land_records",
        "rti_department": "Telangana Revenue Department"
    },
    {
        "file_path": "Land Survey related rti.pdf",
        "title": "Land Survey Related RTI Format",
        "description": "RTI format for land survey and measurement related queries",
        "rti_category": "land_records",
        "rti_department": "Survey Department"
    },
    {
        "file_path": "Khasra Pahani Records.pdf",
        "title": "Khasra Pahani Records RTI Format",
        "description": "RTI format for accessing Khasra and Pahani land records",
        "rti_category": "land_records",
        "rti_department": "Revenue Department"
    },
    {
        "file_path": "Meebhoomi Andhra pradesh land related rti.pdf",
        "title": "Meebhoomi Andhra Pradesh Land RTI Format",
        "description": "RTI format for land-related issues in Andhra Pradesh Meebhoomi system",
        "rti_category": "land_records",
        "rti_department": "Andhra Pradesh Revenue Department"
    },
    {
        "file_path": "Encumberance Certificate.pdf",
        "title": "Encumbrance Certificate RTI Format",
        "description": "RTI format for obtaining encumbrance certificates",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    {
        "file_path": "Mutation Realted RTI.pdf",
        "title": "Mutation Related RTI Format",
        "description": "RTI format for land mutation and transfer related queries",
        "rti_category": "land_records",
        "rti_department": "Revenue Department"
    },
    {
        "file_path": "Sale deed copies.pdf",
        "title": "Sale Deed Copies RTI Format",
        "description": "RTI format for obtaining copies of sale deeds",
        "rti_category": "land_records",
        "rti_department": "Sub Registrar Office"
    },
    
    # Employment & Pension Related
    {
        "file_path": "EPF Status.pdf",
        "title": "EPF Status RTI Format",
        "description": "RTI format for EPF status and related queries",
        "rti_category": "employment",
        "rti_department": "Employees Provident Fund Organization"
    },
    {
        "file_path": "Pension Inquiry tracking.pdf",
        "title": "Pension Inquiry Tracking RTI Format",
        "description": "RTI format for pension inquiry and tracking",
        "rti_category": "employment",
        "rti_department": "Pension Department"
    },
    
    # Education Related
    {
        "file_path": "Marksheet Verification.pdf",
        "title": "Marksheet Verification RTI Format",
        "description": "RTI format for marksheet verification and related queries",
        "rti_category": "education",
        "rti_department": "Education Department"
    },
    
    # Legal & Police Related
    {
        "file_path": "FIR Copy.pdf",
        "title": "FIR Copy RTI Format",
        "description": "RTI format for obtaining copies of FIRs",
        "rti_category": "legal",
        "rti_department": "Police Department"
    },
    {
        "file_path": "First Appeal Template.pdf",
        "title": "First Appeal Template RTI Format",
        "description": "RTI format for filing first appeals",
        "rti_category": "legal",
        "rti_department": "First Appellate Authority"
    },
    {
        "file_path": "Second Appeal Templae.pdf",
        "title": "Second Appeal Template RTI Format",
        "description": "RTI format for filing second appeals",
        "rti_category": "legal",
        "rti_department": "Information Commission"
    },
    
    # Finance & Tax Related
    {
        "file_path": "Income Tax Refund.pdf",
        "title": "Income Tax Refund RTI Format",
        "description": "RTI format for income tax refund related queries",
        "rti_category": "finance",
        "rti_department": "Income Tax Department"
    },
    {
        "file_path": "Refund from Government offices or departments.pdf",
        "title": "Government Refund RTI Format",
        "description": "RTI format for refunds from government offices",
        "rti_category": "finance",
        "rti_department": "General Administration"
    },
    {
        "file_path": "Registration Refund Related RTI.pdf",
        "title": "Registration Refund RTI Format",
        "description": "RTI format for registration refund related queries",
        "rti_category": "finance",
        "rti_department": "Registration Department"
    },
    {
        "file_path": "Fund Utilization.pdf",
        "title": "Fund Utilization RTI Format",
        "description": "RTI format for fund utilization and expenditure queries",
        "rti_category": "finance",
        "rti_department": "Finance Department"
    },
    {
        "file_path": "MP MLA Fund utilization.pdf",
        "title": "MP MLA Fund Utilization RTI Format",
        "description": "RTI format for MP/MLA fund utilization queries",
        "rti_category": "finance",
        "rti_department": "MP/MLA Fund Department"
    },
    
    # Transport Related
    {
        "file_path": "IRCTC Refund issues.pdf",
        "title": "IRCTC Refund Issues RTI Format",
        "description": "RTI format for IRCTC refund related issues",
        "rti_category": "transport",
        "rti_department": "Indian Railways"
    },
    {
        "file_path": "Public Transport Related RTI.pdf",
        "title": "Public Transport RTI Format",
        "description": "RTI format for public transport related queries",
        "rti_category": "transport",
        "rti_department": "Transport Department"
    },
    {
        "file_path": "RTA Related Queries.pdf",
        "title": "RTA Related Queries RTI Format",
        "description": "RTI format for Regional Transport Authority related queries",
        "rti_category": "transport",
        "rti_department": "Regional Transport Authority"
    },
    {
        "file_path": "Toll Collection related rti.pdf",
        "title": "Toll Collection RTI Format",
        "description": "RTI format for toll collection related queries",
        "rti_category": "transport",
        "rti_department": "Highways Department"
    },
    
    # Infrastructure & Development
    {
        "file_path": "Road Work Related RTI.pdf",
        "title": "Road Work Related RTI Format",
        "description": "RTI format for road work and infrastructure queries",
        "rti_category": "infrastructure",
        "rti_department": "Public Works Department"
    },
    {
        "file_path": "Street lights related rti.pdf",
        "title": "Street Lights RTI Format",
        "description": "RTI format for street lights related queries",
        "rti_category": "infrastructure",
        "rti_department": "Municipal Corporation"
    },
    
    # Municipal & Local Government
    {
        "file_path": "Minicipality related rti.pdf",
        "title": "Municipality Related RTI Format",
        "description": "RTI format for municipality related queries",
        "rti_category": "municipal",
        "rti_department": "Municipal Corporation"
    },
    {
        "file_path": "Gram Panchayath Inquiry.pdf",
        "title": "Gram Panchayat Inquiry RTI Format",
        "description": "RTI format for gram panchayat related inquiries",
        "rti_category": "municipal",
        "rti_department": "Gram Panchayat"
    },
    
    # General & Administrative
    {
        "file_path": "Certified documents from government offices or departments.pdf",
        "title": "Certified Documents RTI Format",
        "description": "RTI format for obtaining certified documents from government offices",
        "rti_category": "general",
        "rti_department": "General Administration"
    },
    {
        "file_path": "Citizen Charter of Government offices.pdf",
        "title": "Citizen Charter RTI Format",
        "description": "RTI format for citizen charter related queries",
        "rti_category": "general",
        "rti_department": "General Administration"
    },
    {
        "file_path": "Complaint Tracking.pdf",
        "title": "Complaint Tracking RTI Format",
        "description": "RTI format for complaint tracking and status",
        "rti_category": "general",
        "rti_department": "Grievance Cell"
    },
    {
        "file_path": "Custom Request.pdf",
        "title": "Custom Request RTI Format",
        "description": "RTI format for custom and specific requests",
        "rti_category": "general",
        "rti_department": "General Administration"
    },
    {
        "file_path": "Link document realted rti.pdf",
        "title": "Link Document Related RTI Format",
        "description": "RTI format for link document related queries",
        "rti_category": "general",
        "rti_department": "General Administration"
    },
    {
        "file_path": "Passport Delay.pdf",
        "title": "Passport Delay RTI Format",
        "description": "RTI format for passport delay related queries",
        "rti_category": "general",
        "rti_department": "Passport Office"
    }
]

def upload_pdf(file_info):
    """Upload a single PDF file"""
    url = f"{API_BASE_URL}/upload-pdf"
    headers = {
        "Authorization": f"Bearer {SUPABASE_TOKEN}"
    }
    
    # Check if file exists
    if not os.path.exists(file_info["file_path"]):
        print(f"❌ File not found: {file_info['file_path']}")
        return False
    
    # Prepare form data
    files = {
        'file': open(file_info["file_path"], 'rb')
    }
    
    data = {
        'title': file_info["title"],
        'description': file_info["description"],
        'rti_category': file_info["rti_category"],
        'rti_department': file_info["rti_department"]
    }
    
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully uploaded: {file_info['title']}")
            print(f"   Document ID: {result['data']['document_id']}")
            return True
        else:
            print(f"❌ Failed to upload {file_info['title']}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading {file_info['title']}: {str(e)}")
        return False
    finally:
        files['file'].close()

# Upload all PDFs
print("🚀 Starting PDF upload process...")
success_count = 0

for pdf_info in pdf_files:
    if upload_pdf(pdf_info):
        success_count += 1

print(f"\n📊 Upload Summary: {success_count}/{len(pdf_files)} PDFs uploaded successfully")
import os
import mimetypes

def check_pdf_files():
    """Check if PDF files are valid and readable"""
    pdf_files = [
        "Dharani Telangana Land related issues.pdf",
        "Land Survey related rti.pdf",
        "Khasra Pahani Records.pdf",
        "Meebhoomi Andhra pradesh land related rti.pdf",
        "Encumberance Certificate.pdf",
        "Mutation Realted RTI.pdf",
        "Sale deed copies.pdf",
        "EPF Status.pdf",
        "Pension Inquiry tracking.pdf",
        "Marksheet Verification.pdf",
        "FIR Copy.pdf",
        "First Appeal Template.pdf",
        "Second Appeal Templae.pdf",
        "Income Tax Refund.pdf",
        "Refund from Government offices or departments.pdf",
        "Registration Refund Related RTI.pdf",
        "Fund Utilization.pdf",
        "MP MLA Fund utilization.pdf",
        "IRCTC Refund issues.pdf",
        "Public Transport Related RTI.pdf",
        "RTA Related Queries.pdf",
        "Toll Collection related rti.pdf",
        "Road Work Related RTI.pdf",
        "Street lights related rti.pdf",
        "Minicipality related rti.pdf",
        "Gram Panchayath Inquiry.pdf",
        "Certified documents from government offices or departments.pdf",
        "Citizen Charter of Government offices.pdf",
        "Complaint Tracking.pdf",
        "Custom Request.pdf",
        "Link document realted rti.pdf",
        "Passport Delay.pdf"
    ]
    
    print("🔍 Checking PDF files...")
    print("=" * 50)
    
    valid_files = []
    invalid_files = []
    
    for file_path in pdf_files:
        if os.path.exists(file_path):
            # Check file size
            file_size = os.path.getsize(file_path)
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            
            # Try to read first few bytes to check PDF signature
            try:
                with open(file_path, 'rb') as f:
                    first_bytes = f.read(4)
                    is_pdf = first_bytes == b'%PDF'
            except:
                is_pdf = False
            
            print(f"📄 {file_path}")
            print(f"   Size: {file_size} bytes")
            print(f"   MIME Type: {mime_type}")
            print(f"   PDF Signature: {'✅' if is_pdf else '❌'}")
            print(f"   Status: {'✅ Valid' if is_pdf and file_size > 0 else '❌ Invalid'}")
            print()
            
            if is_pdf and file_size > 0:
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        else:
            print(f"❌ File not found: {file_path}")
            invalid_files.append(file_path)
    
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"✅ Valid PDFs: {len(valid_files)}")
    print(f"❌ Invalid/Missing: {len(invalid_files)}")
    
    if invalid_files:
        print(f"\n❌ Invalid files:")
        for file in invalid_files:
            print(f"   - {file}")
    
    return valid_files, invalid_files

if __name__ == "__main__":
    valid_files, invalid_files = check_pdf_files()

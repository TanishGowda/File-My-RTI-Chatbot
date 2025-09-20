import PyPDF2
import io
import os

def test_pdf_extraction():
    """Test PDF text extraction on your files"""
    print("🔍 Testing PDF text extraction...")
    
    test_files = [
        "Dharani Telangana Land related issues.pdf",
        "Land Survey related rti.pdf",
        "Khasra Pahani Records.pdf"
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"\n📄 Testing: {file_path}")
        print("-" * 50)
        
        try:
            with open(file_path, 'rb') as file:
                # Try to read the PDF
                pdf_reader = PyPDF2.PdfReader(file)
                
                print(f"📊 Number of pages: {len(pdf_reader.pages)}")
                
                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    print("🔒 PDF is encrypted/password protected")
                    continue
                
                # Try to extract text from first page
                try:
                    first_page = pdf_reader.pages[0]
                    text = first_page.extract_text()
                    
                    print(f"📝 Text length: {len(text)} characters")
                    print(f"📝 First 200 characters: {text[:200]}...")
                    
                    if len(text.strip()) == 0:
                        print("⚠️  No text extracted - PDF might be scanned images")
                    else:
                        print("✅ Text extraction successful")
                        
                except Exception as e:
                    print(f"❌ Error extracting text from page: {e}")
                    
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Summary:")
    print("If no text is extracted, your PDFs are likely scanned images")
    print("If text is extracted, the issue is in the backend code")

if __name__ == "__main__":
    test_pdf_extraction()

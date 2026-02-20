import pdfplumber
import os

#Extract PDF and return as Dictionary

def extract_text_from_pdf(pdf_name: str) -> dict:  
    result = {"text": "",
            "pages": 0,
            "extraction_method": "pdfplumber",
            "success": False 
        }
    
    try:
        with pdfplumber.open(pdf_name) as pdf:
            result["pages"] = len(pdf.pages)
            all_text = []

            for page in pdf.pages:
                text = page.extract_text()
                
                if text is not None:
                    all_text.append(text)
                else:
                    print("No Text Extracted")
            
            result["text"] = "\n".join(all_text)

            if len(result["text"]) < 100:
                result["extraction_method"] = "ocr_needed"
            else:
                result["success"] = True
    except Exception as e:
        result["error"] = str(e)
        

    
    return result


        
        




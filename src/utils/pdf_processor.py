from pypdf import PdfReader 

def extract_text_from_pdf(pdf_path:str) -> str:
    try:
        reader=PdfReader(pdf_path)
        full_text=[]

        for page in reader.pages:
            text=page.extract_text()
            if text:
                full_text.append(text)
        return "\n".join(full_text)
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return " "
    except Exception as e:
        print(f"An error Occurred while extracting text:{e} ")
        return " " 
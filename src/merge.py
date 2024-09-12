import os
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def create_title_page(output_path, category):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    story.append(Paragraph(f"{category} News Articles", styles['Title']))
    story.append(PageBreak())
    
    doc.build(story)
    return output_path

def merge_pdfs(category_dir):
    merger = PdfMerger()
    
    # Create a title page
    title_page_path = os.path.join(category_dir, "title_page.pdf")
    create_title_page(title_page_path, os.path.basename(category_dir))
    merger.append(title_page_path)

    # Merge all PDFs in the directory
    for filename in os.listdir(category_dir):
        if filename.endswith(".pdf") and filename != "title_page.pdf" and filename != "Merged.pdf":
            file_path = os.path.join(category_dir, filename)
            merger.append(file_path)
    
    # Write the merged PDF
    output_path = os.path.join(category_dir, "Merged.pdf")
    merger.write(output_path)
    merger.close()
    
    # Clean up the title page
    os.remove(title_page_path)
    
    print(f"Merged PDF created for {os.path.basename(category_dir)}: {output_path}")

def main():
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    
    if not os.path.exists(downloads_dir):
        print(f"Error: The directory {downloads_dir} does not exist.")
        return

    for category in os.listdir(downloads_dir):
        category_dir = os.path.join(downloads_dir, category)
        if os.path.isdir(category_dir):
            merge_pdfs(category_dir)

if __name__ == "__main__":
    main()
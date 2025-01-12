from PyPDF2 import PdfReader

def extract_pdf_pages(filepath):
    reader = PdfReader(filepath)
    pages = [page.extract_text() for page in reader.pages]
    return pages

def schedule_tasks(pages, frequency):
    tasks = []
    total_pages = len(pages)
    pages_per_week = frequency
    weeks = (total_pages + pages_per_week - 1) // pages_per_week

    for week in range(weeks):
        start = week * pages_per_week
        end = min(start + pages_per_week, total_pages)
        tasks.append(pages[start:end])
    
    return tasks

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def create_resume_pdf(text, output_path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    story = []

    for line in text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    return output_path
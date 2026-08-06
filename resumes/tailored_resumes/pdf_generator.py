from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def txt_to_pdf(txt_file, pdf_file):

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    with open(txt_file, "r", encoding="utf-8") as file:
        content = file.read()

    lines = content.split("\n")

    for line in lines:
        if line.strip():
            story.append(
                Paragraph(line, styles["Normal"])
            )
            story.append(Spacer(1, 12))

    doc.build(story)

    print(f"PDF created: {pdf_file}")


def convert_all_resumes():

    folder = "tailored_resumes"

    for file in os.listdir(folder):

        if file.endswith(".txt"):

            txt_path = os.path.join(folder, file)

            pdf_name = file.replace(".txt", ".pdf")

            pdf_path = os.path.join(folder, pdf_name)

            txt_to_pdf(
                txt_path,
                pdf_path
            )


if __name__ == "__main__":
    convert_all_resumes()
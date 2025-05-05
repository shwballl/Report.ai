import logging
import markdown
from pathlib import Path

def generate_html_report(sections: list[tuple[str, str]], output_file: str = "report.html"):
    """
    Преобразует список Markdown-секций в стилизованный HTML-файл.
    
    Args:
        sections (list[tuple[str, str]]): Список секций (название, markdown-контент).
        output_file (str): Имя итогового HTML-файла.
    """

    # Базовая структура HTML с CSS стилями
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Project Review Report</title>
    <style>
        body {{
            font-family: "Segoe UI", sans-serif;
            background-color: #FDFFCE;
            color: #333;
            line-height: 1.6;
            padding: 2rem;
            max-width: 960px;
            margin: auto;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        pre {{
            background-color: #404040;
            padding: 1em;
            overflow-x: auto;
            border-radius: 4px;
            border-left: 4px solid #2c3e50;
        }}
        code {{
            background-color: #404040;
            color: #fff;
            padding: 2px 4px;
            border-radius: 4px;
            family-font: "Courier New", monospace;
        }}
        section {{
            margin-bottom: 3rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""

    md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
    content_html = ""
    for title, markdown_text in sections:
        section_html = md.convert(markdown_text)
        content_html += f"<section>{section_html}</section>\n"
        md.reset()  # Reset between documents

    full_html = html_template.format(content=content_html)

    Path(output_file).write_text(full_html, encoding="utf-8")
    logging.info(f"[✓] Report saved to {output_file}")

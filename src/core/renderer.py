from pathlib import Path
from jinja2 import Template
from weasyprint import HTML



class Renderer:
    @staticmethod
    def render(template: str, data: dict):
        jinja_template = Template(template)
        html_content = jinja_template.render(**data)

        base_dir = Path(__file__).resolve().parent
        static_dir = base_dir / 'src' / 'templates'
        base_url_uri = static_dir.as_uri()

        html_doc = HTML(string=html_content, base_url=base_url_uri)
        output_path = base_dir / 'certificate.pdf'
        html_doc.write_pdf(str(output_path))


"""
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('SocialFoundationCertificate.html') 
        data['logo_path'] = 'logo.png' 

        html_content = template.render(**data.model_dump())

        base_dir = Path(__file__).resolve().parent
        template_dir = base_dir / 'src' / 'templates'

        base_url_uri = template_dir.as_uri()

        html_doc = HTML(string=html_content, base_url=base_url_uri)

        output_filename = base_dir / 'certificate.pdf'
        html_doc.write_pdf(str(output_filename))
"""
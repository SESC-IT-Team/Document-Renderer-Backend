from src.core.renderer import Renderer


def main():
    html_template = ""
    info = ""
    filename = ""
    renderer = Renderer()
    renderer.render(html_template, info, filename)


if __name__ == "__main__":
    main()
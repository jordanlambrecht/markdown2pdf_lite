# Standard library imports
import configparser
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import re
# Third-party imports
import frontmatter
import markdown
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS




# Define styling for console outputs
class style:
    RED = '\033[31m'
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    CYAN = '\033[96m'
    WARNING = '\033[93m'
    RESET = '\033[0m'
    YELLOW =' \033[31m'
    BLINK = '\033[5m'  # Slow Blink
    FRAMED = '\033[32;51;35m'
    ABORT = '\033[97;101;5;1m'

# pygments_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')

link_patterns = [
    (re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+)', re.IGNORECASE), r'<a href="\1">\1</a>')
]

def load_css(css_file):
    """Load CSS from a file."""
    with open(css_file, 'r') as file:
        return file.read()
    
dracula_css = load_css('dracula.css')
base_css = """
@font-face {
    font-family: 'Arial';
    src: url('./fonts/arial.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}
@font-face {
    font-family: 'Arial';
    src: url('./fonts/arial-bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
}
@font-face {
    font-family: 'Arial';
    src: url('./fonts/arial-italic.ttf') format('truetype');
    font-weight: normal;
    font-style: italic;
}
@font-face {
    font-family: 'Arial';
    src: url('./fonts/arial-bold-italic.ttf') format('truetype');
    font-weight: bold;
    font-style: italic;
}
@font-face {
    font-family: 'DejaVu Sans Mono';
    src: url('./fonts/DejaVuSansMono.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}
@font-face {
    font-family: 'DejaVu Sans Mono';
    src: url('./fonts/DejaVuSansMono-Bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
}
@font-face {
    font-family: 'DejaVu Sans Mono';
    src: url('./fonts/DejaVuSansMono-Oblique.ttf') format('truetype');
    font-weight: normal;
    font-style: oblique;
}
@font-face {
    font-family: 'DejaVu Sans Mono';
    src: url('./fonts/DejaVuSansMono-BoldOblique.ttf') format('truetype');
    font-weight: bold;
    font-style: oblique;
}
body {
    font-family: 'Arial', sans-serif;
    font-size: 16px;;
    line-height: 1.6;
    color: #333333;
}
h1 {
    font-size: 2.488em; /* 2.488em ≈ 1.2^5, as per the minor third scale */
    margin-top: 0em;
    margin-bottom: 0.5em;
    color: #3d3d3d;
}
[role="doc-subtitle"]{
    font-size: 1.2em; /* Slightly larger than paragraph text */
    color: #585858; /* Unique color to differentiate from headers and body */
    margin-top: -1em;
    margin-bottom: 1em;
    line-height: 1.3;
    font-weight: bold;
    font-style: italic; 
}

h2 {
    font-size: 2.074em; /* 2.074em ≈ 1.2^4 */
    margin-top: .5em;
    margin-bottom: 0.25em;
    color: #3d3d3d;
}

h3 {
    font-size: 1.728em; /* 1.728em ≈ 1.2^3 */
    margin-top: 1.35em;
    margin-bottom: 0.75em;
    color: #4e4e4e;
}

p {
    font-size: 1em; 
    line-height: 1.75; /* Increased line height to accommodate inline code background */
    margin-top: 1em;
    margin-bottom: 1em;
    color: #333333;
}
blockquote {
    background: #f9f9f9;
    border-left: 10px solid #44475a;
    margin: 2em 0em;
    width: 100%;
    overflow: hidden;
    border-radius: 0.5em;
    padding: 1.25em 3em;
}
blockquote:before {
    color: #ccc;
    line-height: 0.1em;
    margin-right: 0.25em;
    vertical-align: -0.4em;
}
blockquote p {
    font-size: 1.125em;
    font-style: italic;
    display: inline;
    line-height: 0.5em;
}

/* For Tables */
table {
    width: 100%;
    border-collapse: collapse; /* Merges borders between cells */
    background-color: #44475a; /* Lighter background for the whole table */
    color: #f8f8f2; /* Foreground color for text */
    border-radius: .5em; 
    overflow: hidden !important; 
    margin-top: 20px;
    margin-bottom: 20px;
    padding-left: 20px;
    padding-right: 20px;
    
}

th, td {
    padding-left: 1em;
    padding-right: 1em
    # border-bottom: 1px solid #282a36; /* Dark border for subtle contrast */
    text-align: left; /* Align text to the left; adjust as needed */
}

th, th code {
    padding-top: 1em;
    padding-bottom: 1em;

    font-family: 'Arial', sans-serif !important; /* Ensures Arial is used */
    background-color: #282a36; 
    font-weight: bold;
    color: ##8be9fd; 
    font-size: 1.24em !important;
}
tr{
    padding-top: .5em;
    padding-bottom: .5em;
}
tr:nth-child(even) {
    background-color: #3a3c4e; /* Even lighter background for even rows */
}

th:first-child {
    border-top-left-radius: 0.5rem; /* Applies radius to the top-left header */
}

th:last-child {
    border-top-right-radius: 0.5rem; /* Applies radius to the top-right header */
}

td:first-child {
    border-bottom-left-radius: 0.5rem; /* Applies radius to bottom-left cell of each row */
}

td:last-child {
    border-bottom-right-radius: 0.5rem; /* Applies radius to bottom-right cell of each row */
}
td code, th code {
    background: none !important;
    padding: 0; 
    color: inherit !important;
    font-size: 100% !important;
}

/* For Code Blocks */
pre{
    width: 100%;
    background-color: #282a36;
    border-radius: 0.5em;
    overflow: hidden !important; 
    padding: 20px;
    margin-top: 2em;
    margin-bottom: 2em;
    margin-left: 20px;
    margin-right: 20px;
}

pre code {
    font-family: 'DejaVu Sans Mono', monospace;
    background-color: none !important;
    padding: 0;
    text-decoration: none;
    overflow: hidden !important;
    white-space: pre-wrap; /* CSS for soft wrapping */
    word-wrap: break-word; /* Ensures words break to prevent overflow */
    border-radius: 0.5em;
}
:not(pre) > code {
    background-color: #f4f4f4;
    padding: 2px 4px;
    margin: 0px 2px;
    border-radius: 1px;
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 90%;
    color: #FF79C6;
}
li code, li > code {
    margin-bottom: 0px;
    margin-top: 0px;
}
"""
# full_css = base_css + pygments_css
full_css = base_css + dracula_css
# full_css =  dracula_css


# Set up directories and logging
input_dir = 'input'
output_base_dir = 'output'
logs_dir = 'logs'
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_base_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

log_filename = os.path.join(logs_dir, 'mdx_to_pdf.log')
logger = logging.getLogger('MDXtoPDFLogger')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuration file handling
config_file = 'config.ini'
config = configparser.ConfigParser()
if not os.path.exists(config_file):
    config['DEFAULT'] = {'ProjectName': 'DefaultProject'}
    with open(config_file, 'w') as conf:
        config.write(conf)
config.read(config_file)

def preprocess_markdown(content):
    """
    Ensure that triple backticks for code blocks are on their own lines.
    This helps to ensure proper parsing of fenced code blocks in Markdown.
    """
    # Correcting backticks not on their own lines
    content = re.sub(r'([^\n])```', r'\1\n```', content)
    content = re.sub(r'```([^\n])', r'```\n\1', content)
    return content

# Functions for project name and recursive search
def prompt_for_project_name():
    project_name = input(f"{style.CYAN}Enter your project name (default {config['DEFAULT']['ProjectName']}): {style.RESET}")
    if project_name:
        config.set('DEFAULT', 'ProjectName', project_name)
        with open(config_file, 'w') as conf:
            config.write(conf)
    return project_name if project_name else config['DEFAULT']['ProjectName']

def prompt_recursive_search():
    return input(f"{style.CYAN}Should the search include subfolders recursively? (y/n): {style.RESET}").lower() == 'y'


# def convert_to_pdf(input_file, output_file):
#     
    
#     try:
#         if not os.path.exists(input_file):
#             logger.error(f"⛔️ File not found: {input_file}")
#             print(f"{style.RED}⛔️ File not found: {input_file}{style.RESET}")
#             return

#         with open(input_file, 'r', encoding='utf-8') as file:
#             markdown_text = file.read()

        
#         # Parse the front matter
#         parsed = frontmatter.loads(markdown_text)
#         title = parsed.metadata.get('title', 'No Title')
#         description = parsed.metadata.get('description', '')
        
#         if not markdown_text.strip():
#             logger.warning(f"⚠️ No content to process in the file: {input_file}")
#             print(f"{style.YELLOW}⚠️ No content to process in the file: {input_file}{style.RESET}")
#             return
        
#         # Create HTML content with title and description as headers
#         html_content = f"<h1>{title}</h1><div role='doc-subtitle'>{description}</div>\n"
        
#         html_content += markdown2.markdown(parsed.content, extras=["fenced-code-blocks", "tables", "link-patterns"], link_patterns=link_patterns)

#         stylesheets = [CSS(string=full_css)]
#         HTML(string=html_content).write_pdf(output_file, stylesheets=stylesheets)

#         logger.info(f"✅ Successfully converted {input_file} to PDF.")
#         print(f"{style.GREEN}✅ Successfully converted {input_file} to PDF{style.RESET}")
#     except Exception as e:
#         logger.error(f"{style.RED}⛔️ Failed to convert {input_file} to PDF: {e}{style.RESET}")
#         print(f"{style.RED}⛔️ Error converting file {input_file} to PDF: {e}{style.RESET}")   


def convert_to_pdf(input_file, output_file):
    

    try:
        if not os.path.exists(input_file):
            logger.error(f"⛔️ File not found: {input_file}")
            print(f"{style.RED}⛔️ File not found: {input_file}{style.RESET}")
            return

        with open(input_file, 'r', encoding='utf-8') as file:
            markdown_text = file.read()
            
        preprocessed_markdown = preprocess_markdown(markdown_text)
        # Parse the front matter
        parsed = frontmatter.loads(preprocessed_markdown)
        title = parsed.metadata.get('title', 'No Title')
        description = parsed.metadata.get('description', '')
        
        content_html = markdown.markdown(parsed.content, extensions=[
            'fenced_code', 'tables', 'toc', CodeHiliteExtension(css_class='codehilite', guess_lang=True, linenums=False)
        ])
            
        html_content = f"<h1>{title}</h1><div role='doc-subtitle'>{description}</div>\n{content_html}"

            
        # if not markdown_text.strip():
        #     logger.warning(f"⚠️ No content to process in the file: {input_file}")
        #     print(f"{style.YELLOW}⚠️ No content to process in the file: {input_file}{style.RESET}")
        #     return
        
       
        # html_content += markdown.markdown(parsed.content, extensions=['fenced_code', 'tables', CodeHiliteExtension(linenums=False, css_class='highlight', guess_lang=True)])
        
        # html_content += markdown.markdown(preprocessed_markdown, extensions=extensions + [CodeHiliteExtension()], extension_configs=extension_configs)
    

        # Convert HTML to PDF using WeasyPrint with CSS for Arial and DejaVu Sans Mono
        stylesheets = [CSS(string=full_css)] 
        HTML(string=html_content).write_pdf(output_file, stylesheets=stylesheets)

        logger.info(f"✅ Successfully converted {input_file} to PDF.")
        print(f"{style.GREEN}✅ Successfully converted {input_file} to PDF{style.RESET}")
    except Exception as e:
        logger.error(f"{style.RED}⛔️ Failed to convert {input_file} to PDF: {e}{style.RESET}")
        print(f"{style.RED}⛔️ Error converting file {input_file} to PDF: {e}{style.RESET}")   

# Main file processing function
def process_files(recursive=False):
    project_name = prompt_for_project_name()
    output_dir = os.path.join(output_base_dir, project_name)
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(input_dir, topdown=True):
        if not recursive:
            dirs[:] = []  # Prevent descending into subdirectories if not recursive
        for filename in files:
            if filename.endswith('.mdx'):
                input_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_dir)
                prefix = relative_path.replace('/', '-') if relative_path != '.' else ''
                output_filename = f"{prefix}-{filename}" if prefix else filename
                output_path = os.path.join(output_dir, output_filename.replace('.mdx', '.pdf'))
                
                logger.debug(f"Processing file: {input_path}")
                logger.debug(f"Output will be saved to: {output_path}")
                
                convert_to_pdf(input_path, output_path)

# Script execution
if __name__ == '__main__':
    try:
        recursive = prompt_recursive_search()
        process_files(recursive=recursive)
        while input(f"{style.CYAN}Do you want to run it again? (y/n): {style.RESET}").lower() == 'y':
            print("Here we go again")
            recursive = prompt_recursive_search()
            process_files(recursive=recursive)
        print(f"{style.CYAN}----------------------------------------------------------------------------")
        print(f"Thanks for using MDX-to-PDF Converter! Have a blessed day! 👋{style.RESET}")
        print(f"{style.CYAN}----------------------------------------------------------------------------")
        print(f" ")
    except KeyboardInterrupt:
        print(f"{style.ABORT}Script terminated by user. Goodbye!{style.RESET}")

# MDX-to-PDF Converter (Lite)

## Description

This Python script automatically converts files from MDX format to PDF. It's designed to be run from the command line and provides a simple, interactive user experience. Perfect for archiving or sharing your MDX documents in a more accessible format or uploading documentation to ChatGPT.

## Features

- **Interactive**: Prompts you for necessary inputs like project name.
- **Error Handling**: Includes comprehensive error handling to ensure smooth operation.
- **Logging**: Records operations in a log file to keep track of conversions.
- **Customizable**: Saves your last project name to make repeated uses easier and faster.

## Installation

Before running the script, make sure you have Python 3 installed on your Mac. This script uses `fpdf` to generate PDFs, so you will need to install this library.

1. Clone the repository

   ```bash
   git clone git@github.com:jordanlambrecht/markdown2pdf_lite.git
   cd markdown2pdf_lite
   ```

2. Set up a virtual environment (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Dependencies

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set the input directory: Open the script in a text editor and modify the input_dir variable to point to the directory containing your .mdx files.

2.Run the script:

     ```bash
     python3 mdx_to_pdf_converter.py
     ```

3.Follow the on-screen prompts to enter the project name and other options.

## Output

The PDF files will be saved in the `/output/projectname` directory, where `projectname` is the name you provide when prompted.

## Contributing

IDK wtf I'm doing, so any help is great! Feel free to fork this project, make improvements, and submit a pull request. I'm always looking to learn more and improve this script.

## ToDo

- Add support for more complex MDX elements.
- Improve error handling and user feedback.
- Enhance the PDF formatting options.
- Figure out how to switch to markdown2 for pygments and code highlighting

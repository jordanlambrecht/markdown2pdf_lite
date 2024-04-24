# MDX-to-PDF Converter

## Description

This Python script automatically converts files from MDX format to PDF. It's designed to be run from the command line and provides a simple, interactive user experience. Perfect for archiving or sharing your MDX documents in a more accessible format!

## Features

- **Interactive**: Prompts you for necessary inputs like project name.
- **Error Handling**: Includes comprehensive error handling to ensure smooth operation.
- **Logging**: Records operations in a log file to keep track of conversions.
- **Customizable**: Saves your last project name to make repeated uses easier and faster.

## Installation

Before running the script, make sure you have Python 3 installed on your Mac. This script uses `fpdf` to generate PDFs, so you will need to install this library.

1; Clone the repository

```bash
#!/bin/bash
git clone <repository-url>
cd path-to-repository
```

2; Set up a virtual environment (optional but recommended)

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
```

3; Install Dependencies

`pip install -r requirements.txt`

## Usage

1; Set the input directory: Open the script in a text editor and modify the input_dir variable to point to the directory containing your .mdx files.

2; Run the script:

`python3 mdx_to_pdf_converter.py`

3; Follow the on-screen prompts to enter the project name and other options.

## Output

The PDF files will be saved in the `/output/projectname` directory, where `projectname` is the name you provide when prompted.

## Contributing

IDK wtf I'm doing, so any help is great! Feel free to fork this project, make improvements, and submit a pull request. I'm always looking to learn more and improve this script.

## ToDo

- Add support for more complex MDX elements.
- Improve error handling and user feedback.
- Enhance the PDF formatting options.

## Additional Information

- Make sure to replace `<repository-url>` with the actual URL of your GitHub repository where the script is hosted.
- It assumes that you are familiar with the basic Git operations necessary to clone and contribute to repositories.

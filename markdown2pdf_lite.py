#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Welcome to our MDX-to-PDF Converter.
--------------------------------------------------------------------------------
You might wonder what dark magic turns text into PDFs... 
Well, it's not magic, just some lines of code! Enjoy 📄🔮
--------------------------------------------------------------------------------
"""

import os
import subprocess
import configparser
import logging
from fpdf import FPDF

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

# Set up directories
input_dir = '/path/to/input'
output_base_dir = '/output'

# Set up logging
logging.basicConfig(filename='/logs/mdx_to_pdf.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create or load configuration file
config_file = 'config.ini'
config = configparser.ConfigParser()

if not os.path.exists(config_file):
    config['DEFAULT'] = {'ProjectName': 'DefaultProject'}
    with open(config_file, 'w') as conf:
        config.write(conf)
config.read(config_file)

def prompt_for_project_name():
    project_name = input(f"{style.CYAN}Enter your project name (default {config['DEFAULT']['ProjectName']}): {style.RESET}")
    if project_name:
        config.set('DEFAULT', 'ProjectName', project_name)
        with open(config_file, 'w') as conf:
            config.write(conf)
    else:
        project_name = config['DEFAULT']['ProjectName']
    return project_name

def convert_to_pdf(input_file, output_file):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(input_file, 'r') as file:
            for line in file:
                pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(output_file)
        logging.info(f"Successfully converted {input_file} to PDF.")
    except Exception as e:
        logging.error(f"Failed to convert {input_file} to PDF: {e}")
        print(f"{style.RED}Error converting file {input_file} to PDF: {e}{style.RESET}")

def process_files():
    project_name = prompt_for_project_name()
    output_dir = os.path.join(output_base_dir, project_name)
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.mdx'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.mdx', '.pdf'))
            convert_to_pdf(input_path, output_path)

    print(f"{style.GREEN}All files processed. PDFs are saved under {output_dir}.{style.RESET}")

if __name__ == '__main__':
    try:
        process_files()
        while input(f"{style.CYAN}Do you want to run it again? (y/n): {style.RESET}").lower() == 'y':
            print("Here we go again")
            process_files()
        print(f"{style.CYAN}----------------------------------------------------------------------------")
        print(f"Thanks for using MDX-to-PDF Converter! Have a blessed day! 👋{style.RESET}")
        print(f"{style.CYAN}----------------------------------------------------------------------------")
        print(f" ")
    except KeyboardInterrupt:
        print(f"{style.ABORT}Script terminated by user. Goodbye!{style.RESET}")

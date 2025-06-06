import os
import fitz 
import json
from langdetect import detect
import re
import argparse
from art import tprint

from tqdm import tqdm

# Command-line argument parsing
version = "1.0.0"
prog_name = os.path.basename(__file__).replace(".py", "").replace("_", " ").capitalize()
# Capitalize first letter of each word of prog_name
prog_name = " ".join(word.capitalize() for word in prog_name.split())


# Argument parsing
parser = argparse.ArgumentParser(description="Extract and clean text from PDF files, and save to JSON.")
parser.add_argument("pdf_dir", type=str, help="Directory containing PDF files.")
parser.add_argument("output_json", type=str, help="Output JSON file path.")
parser.add_argument("-v", "--version", action="version", version=f"{prog_name} {version}")
args = parser.parse_args()
pdf_dir = args.pdf_dir
output_json = args.output_json

# Print the program name and version
tprint(prog_name, font="chunky")
print(f"\33[1mVersion: {version}\33[0m\n")


# Check if the directory exists and has PDF files
if not os.path.exists(pdf_dir):
    raise FileNotFoundError(f"The directory does not exist.")
if not any(filename.endswith(".pdf") for filename in os.listdir(pdf_dir)):
    raise FileNotFoundError(f"No PDF files found in the directory.")

# Function to clean OCR noise and normalize text
def clean_text(text):
    text = re.sub(r"[\“\”\"“”]", '"', text)  # normalize quotes
    text = re.sub(r"[\‘\’']", "'", text)  # normalize apostrophes
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # remove non-ASCII chars
    text = re.sub(r"[-=]{2,}", "", text)  # remove lines of dashes or equals
    text = re.sub(r"\s+", " ", text)  # collapse multiple whitespace
    text = re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).capitalize(), text)  # normalize SHOUTY words

    # Additional OCR fixes
    text = re.sub(r"\bv/e\b", "we", text)
    text = re.sub(r"\bwhic\.h\b", "which", text)
    text = re.sub(r"\bcarp\b", "camp", text)
    text = re.sub(r"\bIid a\b", "Lida", text)
    text = re.sub(r"\bbods?\b", "beds", text)
    text = re.sub(r"\bexpou- dituro\b", "expenditure", text)
    text = re.sub(r"\bLiniater\b", "Minister", text)
    text = re.sub(r"GE1\s*Ev\s*A", "Geneva", text)

    # Filter French-like chunks (too many accented characters)
    if len(re.findall(r"[éèàùêâîôûëïüç]", text)) > 5:
        return ""
    return text.strip()

# Function to extract and clean text
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        text = page.get_text()
        full_text += text + "\n"
    doc.close()
    return full_text.replace("\n", " ").strip()

# Function to split text into chunks (~200 words)
def chunk_text(text, chunk_size=200):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# List only PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

# Collect all text chunks with metadata
data = []
processed_files = 0
chunks_created = 0
for filename in tqdm (pdf_files, desc="Processing PDFs...", bar_format='{desc}: {bar:30} {percentage:3.0f}%'):

    file_path = os.path.join(pdf_dir, filename)
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    for chunk in chunks:
            if len(chunk) > 100:  # Skip tiny chunks
                if detect(chunk) == "en":
                    try :
                        # Only include English text chunks
                        data.append({
                            "title": filename,
                            "chunk": clean_text(chunk)
                        })
                        chunks_created += 1 
                    except Exception as e:
                        print(f"Error processing chunk: {e}")
    processed_files += 1
        

# Print number of chunks created and files processed
print("\33[1mExtraction and chunking complete.\33[0m")
print(f"{processed_files} / {len(pdf_files)} files processed.")
print(f"{chunks_created} chunks created.\n")


# If output file already exists, ask for confirmation to overwrite
if os.path.exists(output_json):
    overwrite = input(f"\33[1m{output_json} already exists. Overwrite? (y/N): \33[0m\n> ")
    if overwrite.lower() != 'y':
        print("\33[1mOperation cancelled.\33[0m")
        exit()

# Save to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\33[1m\33[92mData saved to {output_json}.\33[0m")
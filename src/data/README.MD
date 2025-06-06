# Data Files

> This directory contains the data files used in the project.

- `docs/` : Contains the original PDF documents from the League of Nations.

- `requirements.txt` : Contains the list of required Python packages for the data extraction script.

- `text_extract.py` : Python script for extracting and cleaning text from the PDF documents.

- `typhus_docs.json` : Example output file containing the cleaned text chunks in JSON format.

- `typhus_index.faiss` : Example FAISS index file for storing the text chunks.

# PDF Text Extraction & Cleaning

This script extracts text from League of Nations PDF documents, cleans it for OCR and language artifacts, and saves it in a structured JSON format for use in downstream tasks (like RAG pipelines).

## 📦 Requirements

- Python 3.8 or higher
- `PyMuPDF` for PDF text extraction
- `langdetect` for language detection and filtering
- `tqdm` for progress bars
- `art` for CLI formatting and printing

Install dependencies with:

```bash
pip install -r requirements.txt
```

Or  individually:

```bash
pip install [package_name]
```

## ▶️ How to Run

To run the script, use the following command:

```bash
python src/data/text_extract.py <pdf_directory> <output_json_path>
```

### Example:

```bash
python src/data/text_extract.py ./docs ./data/typhus_docs.json
```	

## 🧾 Output
A .json file containing structured and cleaned English-only text chunks.

Each chunk includes:

- `"title"`: the source PDF filename

- `"chunk"`: the cleaned text block (approx. 200 words)

### Example Output:

```json
   [
     {"title": "Epidemic Report 1921", "chunk": "Typhus outbreaks occurred..."},
     {"title": "Epidemic Report 1921", "chunk": "International aid was sent..."}
   ]
```

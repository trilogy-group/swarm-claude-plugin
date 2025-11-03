---
name: pdf-processor
version: 1.0.0
description: PDF processing skill for extraction, analysis, and manipulation of PDF documents
author: DevOps Team
tags: [pdf, document-processing, ocr, text-extraction, reporting]
dependencies:
  - pdfjs
  - pypdf2
  - tesseract-ocr
  - ghostscript
capabilities:
  - text_extraction
  - ocr_processing
  - metadata_extraction
  - form_filling
  - pdf_generation
  - pdf_merging
  - pdf_splitting
  - watermarking
---

# PDF Processor Skill

## Overview
The PDF Processor skill provides comprehensive PDF document handling capabilities including extraction, analysis, manipulation, and generation of PDF files for documentation, reporting, and compliance purposes.

## Features

### 1. Text Extraction
- Extract plain text from PDFs
- Preserve formatting and structure
- Extract tables and structured data
- Multi-language support
- Handle encrypted PDFs

### 2. OCR Processing
- Convert scanned documents to text
- Support for 100+ languages
- Image preprocessing for better accuracy
- Handwriting recognition
- Layout analysis

### 3. Metadata Operations
- Extract document properties
- Read/write custom metadata
- Extract embedded files
- Digital signature verification
- Creation/modification date tracking

### 4. PDF Manipulation
- Merge multiple PDFs
- Split PDFs by pages or bookmarks
- Rotate pages
- Crop and resize
- Add watermarks and stamps

### 5. Form Processing
- Extract form fields
- Fill PDF forms programmatically
- Validate form data
- Create fillable forms
- Export form data to JSON/CSV

### 6. Report Generation
- Generate PDFs from templates
- Create reports from data
- Add charts and graphs
- Include images and logos
- Apply corporate branding

## Configuration

```json
{
  "pdf_processor": {
    "enabled": true,
    "ocr": {
      "enabled": true,
      "languages": ["eng", "fra", "deu", "spa"],
      "dpi": 300,
      "preprocessing": true
    },
    "extraction": {
      "preserve_formatting": true,
      "extract_images": true,
      "extract_tables": true,
      "extract_metadata": true
    },
    "security": {
      "allow_encrypted": true,
      "max_file_size_mb": 100,
      "sandbox_mode": true
    },
    "output": {
      "formats": ["text", "json", "html", "markdown"],
      "compression": true,
      "optimization": true
    },
    "performance": {
      "parallel_processing": true,
      "max_workers": 4,
      "cache_enabled": true
    }
  }
}
```

## Usage Examples

### Text Extraction
```python
# Extract text from a PDF
from pdf_processor import PDFExtractor

extractor = PDFExtractor()
text = extractor.extract_text('document.pdf')

# Extract with formatting preserved
formatted_text = extractor.extract_text(
    'document.pdf',
    preserve_formatting=True
)

# Extract specific pages
page_text = extractor.extract_pages(
    'document.pdf',
    pages=[1, 3, 5]
)
```

### OCR Processing
```python
# Process scanned PDF with OCR
from pdf_processor import OCRProcessor

ocr = OCRProcessor(languages=['eng', 'spa'])
text = ocr.process_scanned_pdf('scanned.pdf')

# With preprocessing for better accuracy
text = ocr.process_scanned_pdf(
    'scanned.pdf',
    preprocess=True,
    deskew=True,
    denoise=True
)
```

### Table Extraction
```python
# Extract tables from PDF
from pdf_processor import TableExtractor

extractor = TableExtractor()
tables = extractor.extract_tables('report.pdf')

for idx, table in enumerate(tables):
    # Convert to pandas DataFrame
    df = table.to_dataframe()
    # Export to CSV
    df.to_csv(f'table_{idx}.csv')
```

### PDF Generation
```python
# Generate PDF report from template
from pdf_processor import ReportGenerator

generator = ReportGenerator()

data = {
    'title': 'Monthly DevOps Report',
    'date': '2024-01-15',
    'metrics': {
        'uptime': '99.9%',
        'deployments': 47,
        'incidents': 2
    },
    'charts': ['uptime_chart.png', 'deployment_trend.png']
}

generator.create_report(
    template='monthly_report_template.html',
    data=data,
    output='monthly_report.pdf'
)
```

### Form Processing
```python
# Extract and fill PDF forms
from pdf_processor import FormProcessor

processor = FormProcessor()

# Extract form fields
fields = processor.extract_fields('form.pdf')
print(f"Found {len(fields)} form fields")

# Fill form with data
form_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'department': 'Engineering'
}

processor.fill_form(
    'form.pdf',
    form_data,
    output='filled_form.pdf'
)
```

### PDF Manipulation
```python
# Merge multiple PDFs
from pdf_processor import PDFManipulator

manipulator = PDFManipulator()

# Merge PDFs
manipulator.merge_pdfs(
    ['doc1.pdf', 'doc2.pdf', 'doc3.pdf'],
    output='merged.pdf'
)

# Split PDF by pages
manipulator.split_pdf(
    'large_document.pdf',
    pages_per_file=10,
    output_dir='split_docs/'
)

# Add watermark
manipulator.add_watermark(
    'document.pdf',
    watermark='CONFIDENTIAL',
    output='watermarked.pdf',
    opacity=0.3
)
```

## Integration Examples

### Compliance Report Generation
```python
# Generate compliance reports from audit data
def generate_compliance_report(audit_data):
    generator = ReportGenerator()
    
    # Create PDF with audit findings
    report = generator.create_report(
        template='compliance_template.pdf',
        data={
            'audit_date': audit_data['date'],
            'findings': audit_data['findings'],
            'recommendations': audit_data['recommendations'],
            'compliance_score': audit_data['score']
        }
    )
    
    # Add digital signature
    report.sign(
        certificate='company_cert.p12',
        password='cert_password'
    )
    
    return report
```

### Documentation Processing Pipeline
```python
# Process technical documentation
class DocProcessor:
    def process_documentation(self, pdf_path):
        # Extract text and metadata
        text = self.extract_text(pdf_path)
        metadata = self.extract_metadata(pdf_path)
        
        # Extract code snippets
        code_blocks = self.extract_code_blocks(text)
        
        # Extract diagrams and charts
        images = self.extract_images(pdf_path)
        
        # Generate searchable index
        index = self.create_search_index(text)
        
        # Convert to multiple formats
        self.export_to_markdown(text, 'docs.md')
        self.export_to_html(text, 'docs.html')
        
        return {
            'text': text,
            'metadata': metadata,
            'code_blocks': code_blocks,
            'images': images,
            'index': index
        }
```

## Advanced Features

### Batch Processing
```python
# Process multiple PDFs in parallel
from pdf_processor import BatchProcessor

processor = BatchProcessor(max_workers=4)

# Define processing pipeline
pipeline = [
    ('extract_text', {}),
    ('extract_tables', {}),
    ('extract_metadata', {})
]

# Process all PDFs in directory
results = processor.process_directory(
    'documents/',
    pipeline=pipeline,
    output_format='json'
)
```

### Intelligent Data Extraction
```python
# Extract specific data using patterns
from pdf_processor import IntelligentExtractor

extractor = IntelligentExtractor()

# Define extraction patterns
patterns = {
    'invoice_number': r'Invoice #: (\d+)',
    'total_amount': r'Total: \$([\d,]+\.\d{2})',
    'date': r'Date: (\d{2}/\d{2}/\d{4})'
}

# Extract structured data
data = extractor.extract_by_patterns(
    'invoice.pdf',
    patterns=patterns
)
```

## Performance Optimization

### Caching Strategy
```python
# Enable caching for repeated operations
from pdf_processor import CachedProcessor

processor = CachedProcessor(
    cache_dir='/tmp/pdf_cache',
    ttl=3600  # Cache for 1 hour
)

# Subsequent calls use cache
text1 = processor.extract_text('large_doc.pdf')  # Slow
text2 = processor.extract_text('large_doc.pdf')  # Fast (cached)
```

### Memory Management
```python
# Stream processing for large PDFs
from pdf_processor import StreamProcessor

processor = StreamProcessor()

# Process large PDF in chunks
for chunk in processor.stream_pages('huge_document.pdf', chunk_size=10):
    # Process 10 pages at a time
    process_chunk(chunk)
```

## Error Handling

```python
# Robust error handling
from pdf_processor import PDFProcessor, PDFError

try:
    processor = PDFProcessor()
    result = processor.process('document.pdf')
except PDFError.CorruptedFile as e:
    print(f"PDF is corrupted: {e}")
    # Attempt repair
    repaired = processor.repair_pdf('document.pdf')
except PDFError.PasswordProtected as e:
    print(f"PDF is password protected")
    # Request password
    password = input("Enter PDF password: ")
    result = processor.process('document.pdf', password=password)
except PDFError.UnsupportedFormat as e:
    print(f"Unsupported PDF format: {e}")
```

## Scripts Directory

The PDF processor includes utility scripts in the `scripts/` directory:

### pdf-extract.py
```python
#!/usr/bin/env python3
# Extract text from PDFs via command line

import argparse
from pdf_processor import PDFExtractor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input PDF file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--format', choices=['text', 'json', 'html'],
                       default='text')
    args = parser.parse_args()
    
    extractor = PDFExtractor()
    result = extractor.extract(args.input, format=args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
    else:
        print(result)

if __name__ == '__main__':
    main()
```

### pdf-merge.sh
```bash
#!/bin/bash
# Merge multiple PDFs

if [ $# -lt 2 ]; then
    echo "Usage: $0 output.pdf input1.pdf input2.pdf ..."
    exit 1
fi

OUTPUT=$1
shift

python3 -c "
from pdf_processor import PDFManipulator
m = PDFManipulator()
m.merge_pdfs(['$@'], '$OUTPUT')
print(f'Merged {len(['$@'])} PDFs into $OUTPUT')
"
```

## Troubleshooting

### Common Issues

1. **OCR Accuracy Issues**
   - Solution: Increase DPI, enable preprocessing
   - Check language settings

2. **Memory Issues with Large PDFs**
   - Solution: Use streaming mode
   - Process in chunks

3. **Corrupted PDF Files**
   - Solution: Use repair function
   - Try alternative extraction methods

4. **Missing Dependencies**
   - Install: `pip install pypdf2 pdfplumber pytesseract`
   - Install system deps: `apt-get install tesseract-ocr poppler-utils`

## Best Practices

1. **Always validate input PDFs**
2. **Use appropriate error handling**
3. **Enable caching for repeated operations**
4. **Stream large files instead of loading into memory**
5. **Sanitize user-uploaded PDFs**
6. **Respect PDF permissions and DRM**
7. **Optimize PDFs after manipulation**
8. **Use async processing for web applications**

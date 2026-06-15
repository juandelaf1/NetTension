"""
NetTension — Extract key data from downloaded PDFs.

Sources: ETNO, GSMA, BEREC, Sandvine
"""
import fitz  # PyMuPDF
from pathlib import Path

RAW_DIR = Path(__file__).parents[2] / "data" / "raw"
OUT_DIR = Path(__file__).parents[2] / "data" / "processed"


def extract_text_pages(pdf_path, max_pages=30):
    """Extract text from first N pages of a PDF."""
    doc = fitz.open(str(pdf_path))
    text = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text.append(f"\n=== PAGE {i+1} ===\n{page.get_text()}")
    doc.close()
    return "\n".join(text)


def find_numbers(text, keywords):
    """Find numbers near keywords in text."""
    lines = text.split("\n")
    results = []
    for kw in keywords:
        for i, line in enumerate(lines):
            if kw.lower() in line.lower():
                # Get context: current + next 3 lines
                context = "\n".join(lines[max(0, i - 1):min(len(lines), i + 4)])
                results.append({"keyword": kw, "context": context.strip()})
    return results


# 1. ETNO State of Digital Communications 2025
print("=" * 60)
print("ETNO State of Digital Communications 2025")
print("=" * 60)

etno_path = RAW_DIR / "ETNO_State_Digital_Comms_2025.pdf"
if etno_path.exists():
    text = extract_text_pages(etno_path, 40)
    # Save full text
    with open(OUT_DIR / "etno_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters")

    # Find key numbers
    etno_keywords = [
        "CAPEX", "investment", "revenue", "ARPU", "ROCE",
        "per capita", "fibre", "FTTH", "5G", "EUR",
        "traffic", "data", "growth", "margin",
    ]
    results = find_numbers(text, etno_keywords)
    print(f"\nKey findings ({len(results)} hits):")
    for r in results:
        print(f"\n  [{r['keyword']}]")
        print(f"  {r['context'][:200]}")
else:
    print("File not found")


# 2. GSMA Mobile Economy Europe 2025
print("\n" + "=" * 60)
print("GSMA Mobile Economy Europe 2025")
print("=" * 60)

gsma_path = RAW_DIR / "GSMA_Mobile_Economy_Europe_2025.pdf"
if gsma_path.exists():
    text = extract_text_pages(gsma_path, 30)
    with open(OUT_DIR / "gsma_europe_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters")

    gsma_keywords = [
        "5G", "GDP", "subscriber", "penetration", "revenue",
        "ARPU", "investment", "spectrum", "operator",
        "Spain", "Germany", "France", "Italy", "UK",
        "coverage", "Huawei", "Ericsson", "Nokia",
    ]
    results = find_numbers(text, gsma_keywords)
    print(f"\nKey findings ({len(results)} hits):")
    for r in results:
        print(f"\n  [{r['keyword']}]")
        print(f"  {r['context'][:200]}")
else:
    print("File not found")


# 3. BEREC IP Interconnection Report 2025
print("\n" + "=" * 60)
print("BEREC IP Interconnection Report 2025")
print("=" * 60)

berec_path = RAW_DIR / "BEREC_IP_Interconnection_2025.pdf"
if berec_path.exists():
    text = extract_text_pages(berec_path, 20)
    with open(OUT_DIR / "berec_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters")

    berec_keywords = [
        "fair share", "SPNP", "net neutrality", "traffic",
        "cost", "investment", "CAP", "OTT", "interconnection",
        "market failure", "regulation", "contribution",
    ]
    results = find_numbers(text, berec_keywords)
    print(f"\nKey findings ({len(results)} hits):")
    for r in results:
        print(f"\n  [{r['keyword']}]")
        print(f"  {r['context'][:200]}")
else:
    print("File not found")


# 4. Sandvine GIPR 2024
print("\n" + "=" * 60)
print("Sandvine Global Internet Phenomena Report 2024")
print("=" * 60)

sandvine_path = RAW_DIR / "Sandvine_GIPR_2024.pdf"
if sandvine_path.exists():
    text = extract_text_pages(sandvine_path, 20)
    with open(OUT_DIR / "sandvine_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters")

    sandvine_keywords = [
        "video", "streaming", "Netflix", "YouTube", "TikTok",
        "traffic", "percentage", "downstream", "upstream",
        "mobile", "fixed", "social media", "gaming",
        "Europe", "content", "application",
    ]
    results = find_numbers(text, sandvine_keywords)
    print(f"\nKey findings ({len(results)} hits):")
    for r in results:
        print(f"\n  [{r['keyword']}]")
        print(f"  {r['context'][:200]}")
else:
    print("File not found")


# 5. GSMA Mobile Economy Global 2026 (summary)
print("\n" + "=" * 60)
print("GSMA Mobile Economy Global 2026")
print("=" * 60)

gsma_global_path = RAW_DIR / "GSMA_Mobile_Economy_Global_2026.pdf"
if gsma_global_path.exists():
    text = extract_text_pages(gsma_global_path, 20)
    with open(OUT_DIR / "gsma_global_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted {len(text)} characters")
else:
    print("File not found")

print("\nDone. Extracted text saved to data/processed/*_extracted.txt")

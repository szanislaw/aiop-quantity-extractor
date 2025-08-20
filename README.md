# aiop-quantity-extractor
# Quantity Extractor for Workaround for AIOP API Output

This project processes hotel call transcripts to automatically identify service items requested by guests and estimate their requested quantity. It uses a canonical list of service items, a variant list of guest phrases, and transcript test data.

---

## 📂 Project Structure

```
data/
├── service-items.csv            # Canonical service items list (UUID ↔ Name)
├── job-items.txt                # Tab-separated list of variants (UUID ↔ Phrase)
├── test-tham.xlsx               # Example input transcript
├── test-mock-gen.xlsx           # Example input transcript
└── service-item-quantity-*.csv  # Generated outputs
script.py                        # Main processing script
```

---

## ⚙️ How It Works

1. **Input Files**
   - **Transcript Excel**: Contains guest–concierge dialogues, specifically the column `FCS1 "Remarks"`.
   - **Service Items CSV**: The master list of service items, with `service item uuid` and `service item name`.
   - **Job Items TXT**: A tab-separated variant list linking alternative guest phrases to service item UUIDs.

2. **Processing Flow**
   - Extract guest utterances from the transcript.
   - Match utterances to service items using the variant list.
   - Fall back to the original `FCS1 Service Item Created` column if no match is found.
   - Detect and convert quantities (e.g., "two", "3", "five") into numeric values.
   - Save results in a structured CSV.

3. **Output**
   - For each row in the transcript:
     - `row_id` — index of the input row  
     - `service_item` — matched or fallback service item name  
     - `quantity` — numeric quantity (default `1` if none specified)  
     - `used_fallback` — `True` if no variant match was found  

---

## 🚀 Usage

### 1. Install dependencies
```bash
pip install pandas openpyxl
```

### 2. Run the script
Edit the script to point to your input file:
```python
input_file = "data/test-tham.xlsx"
```

Run it:
```bash
python script.py
```

### 3. Output
The output filename is generated automatically:
- Input: `test-tham.xlsx` → Output: `service-item-quantity-tham.csv`  
- Input: `test-mock-gen.xlsx` → Output: `service-item-quantity-mock-gen.csv`  

All output files are written to the `data/` folder.

---

## 🔍 Example

Input (transcript snippet in Excel):
```
FCS1 "Remarks": "**guest** I need two extra towels please **concierge** ..."
```

Output (CSV):
```csv
row_id,service_item,quantity,used_fallback
0,Towel,2,False
```

---

## 📝 Notes

- Variant phrases in `job-items.txt` are **case-insensitive**.
- If no numeric quantity is found, the script defaults to **1**.
- You can add new synonyms/phrases to `job-items.txt` to improve matching.

---

## 📌 Next Steps

- Extend number parsing beyond 20.
- Add multi-file batch processing support (all `test-*.xlsx` in `data/`).
- Improve fuzzy matching (e.g., `fuzzywuzzy` or `rapidfuzz`) to catch typos.

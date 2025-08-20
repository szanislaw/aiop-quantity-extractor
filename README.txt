README - Service Item Quantity Extractor
========================================

Overview
--------
This script processes hotel concierge transcripts and automatically extracts the requested service items and quantities. 

It uses:
- Guest utterances from transcripts (Excel file)
- Canonical service item definitions (CSV)
- Phrase variants mapped to UUIDs (job-items.txt)

The output is a CSV file that contains the detected service item, quantity, and whether a fallback was used.

Input Files
-----------
1. Transcript Excel file (e.g. test-tham.xlsx, test-mock-gen.xlsx)
   - Must contain the column: FCS1 "Remarks"
   - Should also contain: FCS1 Service Item Created (used for fallback)

2. Service items CSV (service-items.csv)
   - Must contain columns:
     - service item uuid
     - service item name

3. Job items phrase file (job-items.txt)
   - Tab-delimited
   - Format: <uuid> <TAB> <phrase>

Usage
-----
1. Place your transcript Excel file into the "data" folder.
   Example: data/test-tham.xlsx

2. Set the input filename in the script:
   input_file = "data/test-tham.xlsx"

3. Run the script:
   python script.py

4. The script automatically names the output CSV based on the input file:
   - For input: data/test-tham.xlsx
     Output: data/service-item-quantity-tham.csv
   - For input: data/test-mock-gen.xlsx
     Output: data/service-item-quantity-mock-gen.csv

Output Format
-------------
The output CSV will contain the following columns:
- row_id        : Row number from the input transcript
- service_item  : The detected service item name
- quantity      : Quantity extracted from the guest utterance
- used_fallback : True if fallback was used, False otherwise

Example Output Row:
row_id,service_item,quantity,used_fallback
0,Bottled Water,2,False

Notes
-----
- Quantities are extracted from either digits (e.g. "2") or words
  (e.g. "two", "ten").
- If no phrase is matched, the script falls back to the "FCS1 Service Item Created" column.
- Output is always written to the "/output" folder.
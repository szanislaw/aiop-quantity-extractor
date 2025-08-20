import os
import pandas as pd
import re

# ---------- Load input files ----------
input_file = "data/test-tham.xlsx"   # change this to whichever Excel you want
df = pd.read_excel(input_file)

# Service items canonical list
services = pd.read_csv("data/service-items.csv")

# Clean headers
services.columns = services.columns.str.strip().str.lower()

# Build uuid -> service item name map
if "service item uuid" in services.columns and "service item name" in services.columns:
    uuid_to_name = dict(zip(services["service item uuid"], services["service item name"]))
else:
    uuid_to_name = dict(zip(services.iloc[:, 0], services.iloc[:, 1]))

# ---------- Variant list from job_items 6.txt ----------
variants = {}
with open("data/job-items.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            uuid, phrase = parts
            phrase = phrase.lower().strip()
            variants[phrase] = uuid

# ---------- Quantity helper ----------
word2num = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20
}

def extract_quantity(text):
    m = re.search(r"\b(\d+)\b", text)
    if m:
        return int(m.group(1))
    for w, n in word2num.items():
        if re.search(rf"\b{w}\b", text):
            return n
    return 1

# ---------- Main processing ----------
results = []
for idx, row in df.iterrows():
    remark = str(row.get('FCS1 "Remarks"', "")).lower()
    fallback_item = str(row.get("FCS1 Service Item Created", ""))
    
    if "**guest**" in remark:
        guest_text = remark.split("**guest**", 1)[1].split("**concierge**", 1)[0].strip()
    else:
        guest_text = remark
    
    matched_uuid = None
    for phrase, uuid in variants.items():
        if phrase in guest_text:
            matched_uuid = uuid
            break
    
    if matched_uuid:
        service_item = uuid_to_name.get(matched_uuid, "UNKNOWN")
        used_fallback = False
    else:
        service_item = fallback_item
        used_fallback = True
    
    qty = extract_quantity(guest_text)
    
    results.append({
        "row_id": idx,
        "service_item": service_item,
        "quantity": qty,
        "used_fallback": used_fallback
    })

out_df = pd.DataFrame(results)

# ---------- Auto naming ----------
base_name = os.path.splitext(os.path.basename(input_file))[0]   # e.g. test-tham
out_name = f"service-item-quantity-{base_name.replace('test-','')}.csv"
out_path = os.path.join("data", out_name)

out_df.to_csv(out_path, index=False)
print(f"✅ Output written to {out_path}")

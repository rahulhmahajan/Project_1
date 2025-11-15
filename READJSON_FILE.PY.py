import json

CONFIG_FILE = "config.json"

def process_database(db_name, barren, orphan, rni, sdd_to_code, srs_to_code, top_to_bottom, bottom_to_top):
    """
    Replace this with your actual procedure.
    For now, just printing the values.
    """
    print("Processing database: {}".format(db_name))
    print("  Barren: {}".format(barren))
    print("  Orphan: {}".format(orphan))
    print("  RNI: {}".format(rni))
    print("  SDD_TO_CODE: {}".format(sdd_to_code))
    print("  SRS_TO_CODE: {}".format(srs_to_code))
    print("  TOP_TO_BOTTOM: {}".format(top_to_bottom))
    print("  BOTTOM_TO_TOP: {}".format(bottom_to_top))
    print("-" * 40)

# Load config
with open(CONFIG_FILE, "r") as f:
    config_data = json.load(f)

sets = config_data.get("sets", {})

# Iterate over all databases and call procedure
for db_name, db_data in sets.items():
    process_database(
        db_name,
        db_data.get("Barren", ""),
        db_data.get("orphan", ""),
        db_data.get("RNI", ""),
        db_data.get("SDD_TO_CODE", ""),
        db_data.get("SRS_TO_CODE", ""),
        db_data.get("TOP_TO_BOTTOM", ""),
        db_data.get("BOTTOM_TO_TOP", "")
    )

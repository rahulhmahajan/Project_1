import csv

# Define CSV file name
filename = "practice_10x50.csv"

# Prepare header (Column1, Column2, ...)
header = [f"Column{i}" for i in range(1, 51)]

# Prepare 10 rows of data
rows = []
for row_num in range(1, 11):
    row = [f"R{row_num}C{col_num}" for col_num in range(1, 51)]
    rows.append(row)

# Write to CSV
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)   # Write header
    writer.writerows(rows)    # Write data

print(f"{filename} created successfully!")

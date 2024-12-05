# Import
import os
import csv

def saveToCSV(data, answerAndAnalysis, rows, outputDirectory):
    """
    Save data along with suitability analysis to a CSV file.

    Parameters:
    - data: Original data (list of lists or tuples).
    - answerAndAnalysis: List of suitability analysis (e.g., ["Yes", "High Confidence", "Keyword"]).
    - rows: Number of rows to process.
    - outputDirectory: Directory where the CSV file will be saved.
    """
    # Create Header and New Data List
    newData = [["Index", "Authors", "Article Title", "Publication Year", "Abstract", "Suitability", "Confidence", "Keyword"]]

    # Append Suitability, Confidence, and Keyword to Each Row
    for i in range(rows):
        try:
            newRow = [
                data[i][0],  # Index
                data[i][1],  # Authors
                data[i][2],  # Article Title
                data[i][3],  # Publication Year
                data[i][4],  # Abstract
                answerAndAnalysis[i][0] if i < len(answerAndAnalysis) else "N/A",  # Suitability
                answerAndAnalysis[i][1] if i < len(answerAndAnalysis) else "N/A",  # Confidence
                answerAndAnalysis[i][2] if i < len(answerAndAnalysis) else "N/A"   # Keyword
            ]
            newData.append(newRow)
        except IndexError:
            print(f"Warning: Missing data at row {i}. Skipping.")
            continue

    # Sort Data Based on Suitability
    order = {"yes": 0, "maybe": 1, "no": 2, "error": 3}
    newData = [newData[0]] + sorted(newData[1:], key=lambda row: order.get(row[5].lower(), 3))

    # Write to CSV File
    path = os.path.join(outputDirectory, 'data.csv')
    with open(path, mode='w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerows(newData)

    print(f"Data successfully saved to {path}")
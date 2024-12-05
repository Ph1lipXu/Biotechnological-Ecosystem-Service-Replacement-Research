# Import
import os
import csv

def saveToCSV(data, answerAndAnalysis, rows, outputDirectory):
    # Create Header and New Data List
    newData = [["Index", "Article Title", "Authors", "Publication Year", "Suitability", "Confidence", "Keyword"]]

    # Append Suitability, Confidence, and Keyword to Each Row
    for i in range(0, rows):
        authors = data[i][2] + " et al."
        newRow = [
            data[i][0],  # Index
            data[i][1],  # Article Title
            authors,     # Authors
            data[i][3],  # Publication Year
            answerAndAnalysis[i][0],  # Suitability (Yes/Maybe/No)
            answerAndAnalysis[i][1],  # Confidence
            answerAndAnalysis[i][2]   # Keyword
        ]
        newData.append(newRow)

    # Sort Data Based on Suitability
    order = {"yes": 0, "maybe": 1, "no": 2, "error": 3}
    newData = [newData[0]] + sorted(newData[1:], key=lambda row: order.get(row[4].lower(), 3))

    # Writing to CSV File
    path = os.path.join(outputDirectory, 'data.csv')
    with open(path, mode='w', encoding='utf-8', newline='') as file:
        csv.writer(file).writerows(newData)

    print(f"Data successfully saved to {path}")
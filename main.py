# Import
import os
import sys
import time
import g4f
from utilities.retrieve import getData
from utilities.gpt import askGPT
from utilities.export import saveToCSV
from utilities.words import getWords
from utilities.words import countWords
from utilities.graphs import createTfidfMatrix
from utilities.graphs import createDendrogram
from utilities.graphs import createSimilarityMatrix

# Supress Warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Curlm already closed!")

# Variables
directory = "data/"
files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
GPT = True
NUM = 0

# Text-Based Menu UI
print("\nSelect File to Analyze:\n")
for i, file in enumerate(files, 1):
    print(f"{i}: {file}")
choice = int(input("\nEnter Corresponding Number: ")) - 1
print("\n")
filename = os.path.join(directory, files[choice])
outputDirectory = os.path.join("output", os.path.splitext(files[choice])[0])
os.makedirs(outputDirectory, exist_ok = True)

# Get Data
data = getData(filename)

# Iterate Entire Dataset
if NUM == 0:
    NUM = len(data)

# Fetch GPT Response
answerAndAnalysis = []
if(GPT):
    for i in range(0, NUM):
        try:
            # Ask GPT and Parse Response
            response = askGPT(data[i][4])
            parsedResponse = response.split("\n")

            # Safely Extract Suitability, Confidence, and Keyword
            if len(parsedResponse) >= 3:
                suitability = parsedResponse[0].strip()  # Extract the first part (Yes/Maybe/No)
                confidence = parsedResponse[1].strip()   # Extract the second part (0-1 confidence score)
                keyword = parsedResponse[2].strip()      # Extract the third part (Keyword or phrase)
                print(f"Processed Abstract {i+1}: Suitability={suitability}, Confidence={confidence}, Keyword={keyword}")
            else:
                # Default values for unexpected response formats
                suitability = "Error"
                confidence = "0.0"
                keyword = "Failed to parse GPT response"

            # Ensure Suitability is not an Error Message
            if "too many messages in a row" in suitability or "ip:" in suitability:
                answerAndAnalysis.append(["Error", "0.0", "Failed to Retrieve Analysis"])
            else:
                answerAndAnalysis.append([suitability, confidence, keyword])

            time.sleep(2)  # Delay for 2 second

        except Exception as e:
            print(f"Error Processing Abstract {i+1}: {str(e)}")
            answerAndAnalysis.append(["Error", "Failed to Retrieve Analysis"])
        
        # Calculate Progress
        progress = round(((i + 1) / NUM) * 100)
        bar = 50
        fill = int(bar * progress // 100)
        bar = '█' * fill + '-' * (bar - fill)

        print(f'Processing: |{bar}| {progress}% Complete')

    print("Processing Complete!\n")

    # Save Data to CSV File
    saveToCSV(data, answerAndAnalysis, NUM, outputDirectory)

keywords = [item[2] for item in answerAndAnalysis[:NUM]]
suitability_labels = [item[0] for item in answerAndAnalysis[:NUM]]

def shorten_labels(keywords, max_length=50):
    return [keyword[:max_length] + "..." if len(keyword) > max_length else keyword for keyword in keywords]

# Shorten labels for better visualization
shortened_keywords = shorten_labels(keywords)

if NUM > 1:
    # Create TF-IDF Matrix
    tfidf_matrix = createTfidfMatrix(keywords)
        
    # Create Similarity Matrix
    similarityMatrix = createSimilarityMatrix(tfidf_matrix, shortened_keywords)
        
    # Create Dendrogram
    createDendrogram(data, similarityMatrix, shortened_keywords, suitability_labels, outputDirectory)
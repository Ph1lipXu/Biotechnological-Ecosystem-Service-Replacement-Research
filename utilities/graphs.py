# Imports
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity


def createTfidfMatrix(keywords):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(keywords).toarray()
    return tfidf_matrix

# Function to create Similarity Matrix based on Cosine Similarity
def createSimilarityMatrix(tfidf_matrix, keywords):
    # Calculate Cosine Similarity between each pair of abstracts
    semantic_similarity = cosine_similarity(tfidf_matrix)

    # Plot Similarity Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(semantic_similarity, annot=True, cmap="YlGnBu", xticklabels=keywords, yticklabels=keywords)
    plt.title("TF-IDF Semantic Similarity Matrix")

    return semantic_similarity

def createDendrogram(similarityMatrix, keywords, suitability_labels, outputDirectory):
    """
    Create a dendrogram based on semantic similarity of abstracts.

    Parameters:
    - similarityMatrix: A matrix representing the cosine similarity between TF-IDF embeddings.
    - keywords: List of keywords (or titles) corresponding to the abstracts, used for labeling the dendrogram.
    - suitability_labels: The suitability responses (e.g., 'Yes', 'Maybe', 'No') corresponding to the abstracts.
    - outputDirectory: Directory where the generated dendrogram will be saved.
    """
    # Perform Hierarchical Clustering
    linkage_matrix = linkage(similarityMatrix, method='ward')
    
    # Create labels with suitability information
    labeled_keywords = [f"{keyword} ({label})" for keyword, label in zip(keywords, suitability_labels)]
    
    # Create Dendrogram Plot
    plt.figure(figsize=(12, 8))
    dendrogram(linkage_matrix, labels=labeled_keywords)
    
    # Customize the plot
    plt.title("Dendrogram of Abstracts with Suitability Labels")
    plt.xlabel("Abstracts")
    plt.ylabel("Distance")
    
    # Save the Dendrogram Plot
    path = os.path.join(outputDirectory, "dendrogram_with_labels.png")
    plt.savefig(path)
    plt.close()
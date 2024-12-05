# Imports
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer

def createOccupancyMatrix(keywords):
    # Use CountVectorizer to convert summaries to a document-term matrix (DTM)
    vectorizer = CountVectorizer()
    occupancyMatrix = vectorizer.fit_transform(keywords).toarray()
    return occupancyMatrix

def createSimilarityMatrix(embeddings, keywords):
    """
    Create a semantic similarity matrix based on cosine similarity of embeddings.

    Parameters:
    - embeddings: A list or array of sentence embeddings (e.g., from a transformer model).
    - keywords: List of keywords (or titles) corresponding to the embeddings, for labeling the matrix.
    - outputDirectory: Directory where the generated plot will be saved.

    Returns:
    - semantic_similarity: A matrix representing the cosine similarity between the embeddings.
    """
    # Calculate Cosine Distance and Convert to Similarity
    semantic_similarity = 1 - pairwise_distances(embeddings, metric='cosine')

    # Create Similarity Matrix Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(semantic_similarity, annot=False, cmap="YlGnBu", xticklabels=keywords, yticklabels=keywords)
    plt.title("Semantic Similarity Matrix")

    return semantic_similarity

def createDendrogram(semantic_similarity, keywords, suitability_labels, outputDirectory):
    """
    Create a dendrogram based on semantic similarity of abstracts.

    Parameters:
    - semantic_similarity: A matrix representing the cosine similarity between sentence embeddings.
    - keywords: List of keywords (or titles) corresponding to the abstracts, used for labeling the dendrogram.
    - suitability_labels: The suitability responses (e.g., "Yes", "Maybe", "No") corresponding to the abstracts.
    - outputDirectory: Directory where the generated dendrogram will be saved.
    """
    # Perform Hierarchical Clustering
    linkage_matrix = linkage(semantic_similarity, method='ward')
    
    # Create Dendrogram Plot
    plt.figure(figsize=(12, 8))
    dendrogram(linkage_matrix, labels=[f"{keyword} ({answer})" for keyword, answer in zip(keywords, suitability_labels)])
    
    # Customize the plot
    plt.title("Dendrogram of Abstracts Based on Semantic Similarity")
    plt.xlabel("Abstracts")
    plt.ylabel("Distance")
    
    # Save the Dendrogram Plot
    path = os.path.join(outputDirectory, "dendrogram_updated.png")
    plt.savefig(path)
    plt.close()
def precision_at_k(retrieved, relevant):
    return len(set(retrieved) & set(relevant)) / len(retrieved)


def recall_at_k(retrieved, relevant):
    return len(set(retrieved) & set(relevant)) / len(relevant)
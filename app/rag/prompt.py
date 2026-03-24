def build_prompt(query, contexts):
    ctx_text = ""
    for i, ctx in enumerate(contexts):
        ctx_text += f"[Source: {ctx['source']}]\n{ctx['text']}\n\n"
        
    return f"""You are a helpful assistant. Use ONLY the provided context to answer the question.
If the answer is not in the context, say "I don't know."

Context:
{ctx_text}

Question: {query}
Answer:"""

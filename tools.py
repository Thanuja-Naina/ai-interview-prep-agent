import re

BANK = {
 "python": {
  "beginner": ["What is the difference between a list and a tuple?","What is a dictionary?","Why do we use functions?","What is the difference between == and is?","How does a for loop work?"],
  "intermediate": ["What are list comprehensions?","Explain mutable and immutable objects.","What is a generator?","How does exception handling work?"],
  "advanced": ["Explain the Global Interpreter Lock.","How do decorators work?","Compare multiprocessing and asynchronous I/O."]
 },
 "sql": {
  "beginner": ["What is a primary key?","Difference between WHERE and HAVING?","Difference between INNER JOIN and LEFT JOIN?","What does GROUP BY do?"],
  "intermediate": ["What is a window function?","How do you find the second-highest salary?","Difference between UNION and UNION ALL?"],
  "advanced": ["How do you investigate a slow SQL query?","Explain recursive CTEs."]
 },
 "machine learning": {
  "beginner": ["Supervised vs unsupervised learning?","What is overfitting?","Why split data into train and test sets?","Classification vs regression?"],
  "intermediate": ["Explain bias-variance trade-off.","Why can accuracy mislead on imbalanced data?","Compare precision, recall, and F1-score."],
  "advanced": ["How do you detect data leakage?","How would you choose a metric for rare-event classification?"]
 },
 "rag": {
  "beginner": ["What is Retrieval-Augmented Generation?","What is an embedding?","Why retrieve documents before generating an answer?"],
  "intermediate": ["How does chunk size affect retrieval?","Keyword search vs vector search?","How would you evaluate RAG retrieval?"],
  "advanced": ["When would you use hybrid search or reranking?","How can you reduce hallucinations in RAG?"]
 }
}

def search_question_bank(topic, difficulty="beginner", count=5):
    t = topic.lower()
    if "python" in t: key = "python"
    elif "sql" in t or "database" in t: key = "sql"
    elif "machine learning" in t or t.strip() in ("ml","ai/ml","ai ml"): key = "machine learning"
    elif "rag" in t or "retrieval" in t or "genai" in t: key = "rag"
    else: return {"topic":topic,"questions":[],"message":"Topic is not in the local bank yet. Add it to BANK in tools.py."}
    level = difficulty.lower() if difficulty.lower() in BANK[key] else "beginner"
    count = max(1, min(int(count), 10))
    qs = BANK[key][level][:count]
    return {"topic":key,"difficulty":level,"questions":qs,"returned":len(qs)}

def evaluate_answer_structure(question, answer):
    words = re.findall(r"\b[\w'-]+\b", answer.strip())
    text = answer.lower()
    signals = {
      "definition_or_explanation": any(x in text for x in (" is "," means "," refers to "," defined as ")),
      "example": any(x in text for x in ("example","for instance","such as","e.g.")),
      "reason_or_use_case": any(x in text for x in ("because","therefore","when ","useful","helps")),
      "limitation_or_tradeoff": any(x in text for x in ("however","limitation","trade-off","drawback","depends"))
    }
    if not words: feedback = "No answer was provided."
    elif len(words) < 25: feedback = "Very short; consider adding a definition, explanation, and example."
    elif len(words) <= 180: feedback = "Reasonable practice-answer length for many interview questions."
    else: feedback = "Long answer; consider making it more focused."
    return {"question":question,"word_count":len(words),"length_feedback":feedback,"structure_signals":signals,
            "important_note":"This is a simple keyword-based checklist. It does not verify technical correctness or provide a reliable interview score."}

def find_resume_matches(resume_text, keywords):
    text = resume_text.lower()
    matched = [k for k in keywords if k.lower() in text]
    missing = [k for k in keywords if k.lower() not in text]
    return {"matched_keywords":matched,"not_found_keywords":missing,
            "note":"Literal keyword matching only; this does not measure skill level and may miss wording variations."}

# AI Interview Preparation Agent — Tool-Based

A beginner-friendly project using Python, Streamlit, and Groq tool calling.

## Tools
1. `search_question_bank`: retrieves questions from a small local bank for Python, SQL, Machine Learning, and RAG.
2. `evaluate_answer_structure`: checks word count and basic structure signals. It does **not** verify technical correctness.
3. `find_resume_matches`: finds requested keywords in resume text pasted by the user.

## Agent flow
User -> Streamlit -> LLM -> (answer directly OR request a tool) -> Python tool -> tool result back to LLM -> final response.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-real-key"
```
Or set `$env:GROQ_API_KEY = "your-real-key"` in PowerShell. Never commit the real key to GitHub.

Then run:
```powershell
streamlit run app.py
```

## Example prompts
- Give me 4 beginner Python interview questions.
- Give me 3 intermediate SQL questions.
- Question: What is overfitting? My answer: Overfitting is ... Please review the answer structure.
- Resume text: [paste text]. Check whether it mentions Python, SQL, RAG, and FastAPI.


## Notes
The default model is `openai/gpt-oss-20b`; if it is unavailable or lacks tool calling, choose a currently supported model in Groq's model documentation. API calls and deployment must be tested with your own API key. The resume checker requires pasted text and does not parse PDF/DOCX files.

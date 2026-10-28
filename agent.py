import json
from tools import search_question_bank, evaluate_answer_structure, find_resume_matches

SYSTEM = """You are a friendly beginner-level interview preparation coach.
Use search_question_bank for requests for interview questions.
Use evaluate_answer_structure when the user asks for feedback on an answer; pass the question and answer.
Use find_resume_matches only when resume text has been supplied; otherwise ask the user to paste it.
Explain tool results clearly. The answer checker is only a heuristic checklist, not a technical correctness grade.
If no tool is needed, answer directly. Never claim a tool was used unless it was called."""

TOOLS = [
 {"type":"function","function":{"name":"search_question_bank","description":"Search a built-in interview question bank by topic and difficulty.","parameters":{"type":"object","properties":{"topic":{"type":"string"},"difficulty":{"type":"string","enum":["beginner","intermediate","advanced"]},"count":{"type":"integer"}},"required":["topic","difficulty","count"],"additionalProperties":False}}},
 {"type":"function","function":{"name":"evaluate_answer_structure","description":"Review answer length and structure signals. Does not verify technical correctness.","parameters":{"type":"object","properties":{"question":{"type":"string"},"answer":{"type":"string"}},"required":["question","answer"],"additionalProperties":False}}},
 {"type":"function","function":{"name":"find_resume_matches","description":"Find requested keywords in resume text supplied by the user.","parameters":{"type":"object","properties":{"resume_text":{"type":"string"},"keywords":{"type":"array","items":{"type":"string"}}},"required":["resume_text","keywords"],"additionalProperties":False}}}
]
FUNCTIONS = {
 "search_question_bank": search_question_bank,
 "evaluate_answer_structure": evaluate_answer_structure,
 "find_resume_matches": find_resume_matches,
}

def run_agent(client, user_message, history=None, model="openai/gpt-oss-20b", max_rounds=4):
    messages = [{"role":"system","content":SYSTEM}]
    for item in (history or [])[-8:]:
        if item.get("role") in ("user","assistant") and item.get("content"):
            messages.append({"role":item["role"],"content":item["content"]})
    messages.append({"role":"user","content":user_message})
    activity = []
    for _ in range(max_rounds):
        response = client.chat.completions.create(model=model, messages=messages, tools=TOOLS, tool_choice="auto", temperature=0.2)
        msg = response.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content or "Please try asking in a different way.", activity
        for call in msg.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments or "{}")
                result = FUNCTIONS[name](**args) if name in FUNCTIONS else {"error":"Unknown tool"}
                result_text = json.dumps(result, ensure_ascii=False)
                activity.append(f"Called {name} with {json.dumps(args, ensure_ascii=False)}")
            except Exception as exc:
                result_text = json.dumps({"error":str(exc)})
                activity.append(f"{name} returned an error.")
            messages.append({"role":"tool","tool_call_id":call.id,"content":result_text})
    response = client.chat.completions.create(model=model, messages=messages, tool_choice="none", temperature=0.2)
    return response.choices[0].message.content or "Tool-call limit reached. Try a simpler request.", activity

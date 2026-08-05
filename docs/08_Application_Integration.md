# Project Tattva Documentation

**Document:** 08 — Application Integration  
**Version:** 1.1  
**Status:** Completed

---

# 1. Purpose

This document describes how the Retriever, PromptBuilder, LLMClient, Chatbot, and command-line interface are integrated into one end-to-end application.

---

# 2. Integration Objectives

The application layer was designed to:

- Keep orchestration simple.
- Hide Ollama-specific response details.
- Reuse initialized components.
- Support repeated questions in one process.
- Keep the CLI free of business logic.
- Allow future replacement of the interface or model client.

---

# 3. LLMClient

The `LLMClient` class isolates Ollama communication.

Current configuration:

```text
Model: phi3:mini
Runtime: Ollama
API: ollama.chat()
```

The client sends one user message containing the complete RAG prompt.

```python
response = ollama.chat(
    model=self.model,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
```

Only the generated text is returned:

```python
return response["message"]["content"]
```

---

# 4. Chatbot Orchestrator

The `Chatbot` class owns three components:

- Retriever
- PromptBuilder
- LLMClient

The `chat()` method performs the application workflow.

```python
def chat(self, user_query):
    retrieved_documents = self.retriever.retrieve(user_query)

    prompt = self.prompt_builder.build_prompt(
        user_query,
        retrieved_documents
    )

    response = self.llm_client.generate_response(prompt)

    return response
```

The method contains orchestration only.

---

# 5. Command-Line Interface

The CLI creates one Chatbot instance and keeps it alive inside a loop.

```text
Start application
      │
      ▼
Initialize Chatbot once
      │
      ▼
Read user query
      │
      ├── exit / quit → stop
      │
      ▼
Chatbot.chat(query)
      │
      ▼
Print response
      │
      └── repeat
```

The user input is normalized with `.strip()` and compared in lowercase for exit commands.

---

# 6. End-to-End Workflow

```text
User enters question
        │
        ▼
CLI calls Chatbot.chat()
        │
        ▼
Retriever embeds and searches
        │
        ▼
PromptBuilder creates prompt
        │
        ▼
LLMClient calls Ollama
        │
        ▼
Chatbot returns generated text
        │
        ▼
CLI prints response
```

---

# 7. Why Components Are Initialized Once

The application creates one instance of each major component because:

- Loading the embedding model is expensive.
- The system prompt does not need to be read for every query.
- Vector-store connections can be reused.
- Model configuration remains unchanged during one session.

---

# 8. Error Resolution During Integration

## Import Path Error

Problem:

```text
ModuleNotFoundError: No module named 'knowledge_base'
```

Resolution:

Use absolute project imports beginning with `src`.

---

## Missing Chatbot Attribute

Problem:

The Chatbot used an attribute name that was not initialized.

Resolution:

Use one consistent LLM client attribute name.

---

## None Response

Problem:

The Chatbot called the LLM Client but did not return its result.

Resolution:

Add:

```python
return response
```

---

## Method Name Mismatch

Problem:

The Chatbot and LLM Client used different method names.

Resolution:

Keep the call consistent with `generate_response()`.

---

# 9. Current Interface Limitations

- CLI only
- No streaming output
- No request validation layer
- No conversation memory
- No API authentication
- No concurrent users
- No structured response schema

---

# 10. Planned API Layer

A future FastAPI layer can call the existing Chatbot without changing retrieval or generation logic.

Planned endpoint:

```text
POST /chat
```

Example request:

```json
{
    "query": "What is Karma Yoga?"
}
```

Example response:

```json
{
    "answer": "..."
}
```

The current modular design allows the CLI to be replaced or supplemented by an API.

---

# 11. Summary

Project Tattva integrates retrieval, prompt construction, and local LLM generation through a small Chatbot orchestrator.

The command-line interface remains intentionally simple, while the application logic stays inside reusable components. This makes the current MVP easy to demonstrate and prepares the project for future API and frontend integration.

---

**Next Document:** `09_Evaluation.md`

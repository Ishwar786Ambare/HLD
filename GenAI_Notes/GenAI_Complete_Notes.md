<!-- ============================================================
     GENERATIVE AI — COMPLETE STUDY NOTES
     Compiled by: Ishwar Ambare
     LinkedIn:    https://www.linkedin.com/in/ishwar-ambare/
     Source:      Scalar GenAI Basics Module (Classes 1–4)
     Instructor:  Shivank (Head of Data Science, Scale | Ex-Microsoft, Oracle)
     ============================================================ -->

# 🤖 Generative AI — Complete Study Notes

> 📝 **Compiled by:** [Ishwar Ambare](https://www.linkedin.com/in/ishwar-ambare/)
> 🎓 **Source:** Scalar GenAI Basics Module — Classes 1 to 4
> 👨‍🏫 **Instructor:** Shivank (Head of Data Science, Scale | Ex-Microsoft, Oracle)

---

## 📑 Full Table of Contents

### 🗂️ Part 1 — GenAI Introduction & Landscape (Class 1)
1. [Why Generative AI? The Buzz](#1-why-generative-ai-the-buzz)
2. [What is Generative AI?](#2-what-is-generative-ai)
3. [GenAI Technology Stack](#3-genai-technology-stack)
4. [Timeline / Journey of GenAI](#4-timeline--journey-of-genai)
5. [AI Hierarchy](#5-ai-hierarchy)
6. [Industry Applications](#6-industry-applications)
7. [Market Reports & Economic Impact](#7-market-reports--economic-impact)
8. [Key Takeaways — Class 1](#8-key-takeaways--class-1)

### 🗂️ Part 2 — Prerequisites & API Basics (Class 2)
9. [Python Libraries — The "Why"](#9-python-libraries--the-why)
10. [Machine Learning — Predictions on Table Data](#10-machine-learning--predictions-on-table-data)
11. [Deep Learning — Predictions on Images/Audio/Video](#11-deep-learning--predictions-on-imagesaudiovideo)
12. [NLP — Predictions on Text](#12-nlp--predictions-on-text)
13. [The Godfather Paper: "Attention is All You Need"](#13-the-godfather-paper-attention-is-all-you-need)
14. [OpenAI API Setup](#14-openai-api-setup)
15. [Pricing Model & Tokens](#15-pricing-model--tokens)
16. [Hands-On: First API Calls](#16-hands-on-first-api-calls)
17. [Key Parameters Explained](#17-key-parameters-explained)
18. [Key Takeaways — Class 2](#18-key-takeaways--class-2)

### 🗂️ Part 3 — Prompt Engineering (Classes 3 & 4)
19. [Dynamic Prompt Templates with `.format()`](#19-dynamic-prompt-templates-with-format)
20. [Case Study 1 — Financial Document Q&A (Asian Paints)](#20-case-study-1--financial-document-qa-asian-paints)
21. [Case Study 2 — Few-Shot Prompting & Conversational AI (Math Tutor)](#21-case-study-2--few-shot-prompting--conversational-ai-math-tutor)
22. [Case Study 3 — Structured Data Extraction & Classification (Laptops)](#22-case-study-3--structured-data-extraction--classification-laptops)
23. [The 3-Step Prompt Engineering Framework](#23-the-3-step-prompt-engineering-framework)
24. [Homework — Wikipedia Q&A Bot](#24-homework--wikipedia-qa-bot)
25. [Rate Limiting & Exponential Backoff](#25-rate-limiting--exponential-backoff)
26. [Open-Source LLMs via Hugging Face (LLaMA)](#26-open-source-llms-via-hugging-face-llama)
27. [Key Takeaways — Classes 3 & 4](#27-key-takeaways--classes-3--4)

---

# 🗂️ PART 1 — GenAI Introduction & Landscape
> **Class 1** | Source: [YouTube Transcript](https://youtu.be/Pz9pUmfDQjU)

---

## 1. Why Generative AI? The Buzz

### 🚀 ChatGPT vs Other Platforms — Time to 1 Million Users
| Platform | Time to 1M Users |
|---|---|
| ChatGPT | **5 Days** 🔥 |
| Instagram | 2.5 Months |
| Spotify | 5 Months |
| Dropbox | 7 Months |
| Facebook | 10 Months |
| Netflix | ~49 Weeks |

> **Insight:** ChatGPT hit 1M users faster than any platform in history, with **1.8 billion total visits** and an avg. session of **7 min 51 sec**.

### 💰 Startup Funding in GenAI (as of 2023)
Even relatively unknown GenAI startups are securing:
- **$5M–$15M** in early rounds
- **$16M–$40M** in mid rounds
- **$41M–$100M** in later rounds

> Happening **during a low job market** — investors are betting big on GenAI.

### The WWW Analogy
> *"GenAI is the new WWW."*
> Just like the internet created an entire IT industry, GenAI will spawn a new wave of industries and jobs. Being early = massive advantage.

---

## 2. What is Generative AI?

### Simple Definition
> **Generative AI** = A system that takes an **input** (text, image, audio) and **generates new content** (text, image, audio, video, code) as output.

### Examples
| Input | Tool | Output |
|---|---|---|
| Text question | ChatGPT | Text answer |
| Text prompt ("horse on chessboard") | Midjourney | 4 generated images |
| Existing image | Adobe Firefly | Background-replaced image |
| Code comments | GitHub Copilot | Full code blocks |

### Formal Stack
```
Input Prompt  ──►  [LLM / GenAI Model]  ──►  Generated Output
```

---

## 3. GenAI Technology Stack

### Layer 1: Models & APIs

#### 🔒 Closed LLMs (Paid / Not Open Source)
| Model | By |
|---|---|
| GPT-3.5, GPT-4 | OpenAI |
| PaLM 2 | Google |
| Claude | Anthropic |
| Cohere | Cohere AI |
| Llama (original) | Meta |

#### 🔓 Open LLMs (Free / Open Source)
| Model | By |
|---|---|
| Hugging Chat | Hugging Face |
| Open LLaMA | OpenLM Research |
| Dolly | Databricks |
| Stable LM | Stability AI |

> **Key difference:** Closed = fast, paid. Open = slower, free.

#### 🎨 Image Models
| Tool | Notes |
|---|---|
| Midjourney | Paid, works via Discord |
| DALL·E 2 | OpenAI product |
| Stable Diffusion | Open source |
| Runway | Video generation |

#### 🎵 Music Models
| Tool | By |
|---|---|
| MusicLM | Google |
| MusicGen | Meta / Facebook |

---

### Layer 2: Vector Databases

#### Why Vector DBs?
- Text data is converted to **numerical vectors** (e.g., via embeddings)
- Words/phrases with **similar meaning** → **similar vectors** (small angle between them)
- Enables **extremely fast similarity search**

#### Intuition: Word → Vector Space
```
king   →  [1.2, 0.8, ...]   ──┐
prince →  [1.1, 0.9, ...]   ──┴──  Close together (similar meaning)

McDonald's → [8.3, 0.1, ...]  ──── Far apart from "king"
```

#### Popular Vector Databases
| DB | Notes |
|---|---|
| **Pinecone** | Managed, popular in production |
| **Chroma** | Open source, easy to use |
| **Qdrant** | High performance |

> Used by companies like **Grammarly** to enable fast semantic searches.

---

### Layer 3: LLM Frameworks

Used when you have a **chain of LLM tasks** (one output feeds the next):

| Framework | Purpose |
|---|---|
| **LangChain** | Most popular; chains LLM calls, integrates tools |
| **LlamaIndex** | Data indexing + LLM query pipelines |
| **AutoGPT / Others** | Autonomous agent frameworks |

---

### Layer 4: Deployment

| Tool | Notes |
|---|---|
| **Hugging Face Hub** | Model hosting + deployment |
| **Docker** | Containerize LLM apps |
| **Azure OpenAI Services** | Full enterprise suite |
| **Vertex AI (Google)** | Cloud-based ML deployment |

---

## 4. Timeline / Journey of GenAI

```
1642  ──  Machine Learning concepts begin
2014  ──  GAN Networks introduced (Ian Goodfellow) — image generation
2017  ──  Transformers paper published ("Attention is All You Need") — NLP breakthrough
2018  ──  GPT-1 released (OpenAI) — largely unnoticed
2019  ──  GPT-2 released
2020  ──  GPT-3 released
2021  ──  DALL·E released (image generation from text)
2022  ──  DALL·E 2, ChatGPT 3.5 launches — goes viral
2023  ──  GPT-4 released (limited access)
2024+ ──  GPT-5 expected; explosive growth across all verticals
```

> **Key insight:** We are at the **very beginning** of the GenAI era. By 2030, the transformation will be remarkable.

---

## 5. AI Hierarchy

```
┌────────────────────────────────────────────┐
│                   AI                        │
│  ┌──────────────────────────────────────┐  │
│  │          Machine Learning            │  │
│  │  ┌────────────────────────────────┐  │  │
│  │  │        Deep Learning           │  │  │
│  │  │  ┌──────────────────────────┐  │  │  │
│  │  │  │    NLP / Transformers    │  │  │  │
│  │  │  │  ┌────────────────────┐  │  │  │  │
│  │  │  │  │   Generative AI    │  │  │  │  │
│  │  │  │  └────────────────────┘  │  │  │  │
│  │  │  └──────────────────────────┘  │  │  │
│  │  └────────────────────────────────┘  │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

> GenAI sits at the **deepest layer** but **leverages all parent concepts** — ML, Deep Learning, NLP, Transformers.

**Key techniques inherited:**
- **RNN** (Recurrent Neural Networks) → basis for early NLP
- **Autoencoders** → used in Transformers
- **Transformers** → backbone of modern LLMs (GPT, BERT, etc.)

---

## 6. Industry Applications

### 👨‍💻 Software Engineering — GitHub Copilot
- Write a comment → Copilot generates full code
- Auto-suggests code completions (just press Tab)
- Generates unit tests automatically
- Creates components from natural language

> **Impact:** 1 tester can replace 4; 1 dev can write 10x more code.

### 🏥 Healthcare — Med-PaLM 2 (Google)
- Trained on medical knowledge
- Scored **87% on MBBS-equivalent exams**
- Outperforms many medical students
- Ask symptoms → get diagnostics

### 🎓 Education — Khanmigo (Khan Academy)
- AI tutor powered by ChatGPT
- Guides students through problems (doesn't just give answers)
- Can roleplay as a mentor

### 🎨 Marketing & Design
| Tool | Use Case |
|---|---|
| Midjourney | Generate ad images from text prompts |
| Adobe Firefly | Background replacement, image editing |
| Persado | Personalized marketing copy |
| Rephrase.ai | Synthetic celebrity spokesperson videos |

> **Real-world:** Microsoft ads now use GenAI to generate personalized images per user, in real-time.

### 💹 Finance — Bloomberg GPT
- Trained on **50 billion financial parameters**
- Answers: fundamental analysis, sentiment analysis of news
- Potential to replace portfolio managers

### 🛒 E-Commerce — MyFashionGPT
- Tell it your occasion → get outfit recommendations
- Virtual try-on: see how clothes look on a body similar to yours

### ⚖️ Legal
- Can analyze case law, draft documents
- Still in early stages but growing fast

---

## 7. Market Reports & Economic Impact

### McKinsey Report
| Area | Impact |
|---|---|
| New use cases enabled by GenAI | **$2.6T – $4.4T** additional value |
| Current ML/AI market | $11T – $17T |
| Productivity improvement | $6.1T – $7.9T |

> The **$2.6T–$4.4T** additional value ≈ **GDP of the United Kingdom** (6th largest economy)

**Most Impacted Sectors:**
1. 🏆 Software Engineering (highest impact)
2. 📊 Finance
3. 📣 Sales & Marketing

### Goldman Sachs Report
> *"GenAI could raise global GDP by **7%**."*

---

## 8. Key Takeaways — Class 1

### 🎯 Core Insights
- GenAI is **not a trend** — it's the next **foundational technology** (like the internet)
- Even non-tech professionals (sales, marketing, doctors, lawyers) **need basic GenAI literacy**
- People who master this will **create** job disruption, not suffer from it

### 🧠 The Darwin Principle
> *"You either adapt or get replaced. It's Darwin's theory — you need to survive."*

### 💡 Startup Opportunity
- Companies with **just an idea** are getting **$100M+ in funding**
- Open-source models (Stable Diffusion, etc.) let you build startups on top for **free**
- Early movers have **massive advantages**

### 🗺️ Learning Path
```
Python Basics
     │
     ▼
GenAI Fundamentals + Prompt Engineering
     │
     ▼
Machine Learning + NLP
     │
     ▼
LLM Fine-tuning, RAG, Vector DBs, Deployment
     │
     ▼
Build → Ship → Fund 🚀
```

### 📚 Resources — Class 1
| Resource | Link |
|---|---|
| ChatGPT | https://chat.openai.com |
| Gemini | https://gemini.google.com |
| Midjourney | Via Discord — paid |
| DALL·E 2 | https://openai.com/dall-e-2 |
| Hugging Chat | https://huggingface.co/chat |
| Adobe Firefly | https://firefly.adobe.com |
| Khanmigo | https://khanmigo.ai |
| Chroma DB | https://www.trychroma.com |
| Pinecone | https://www.pinecone.io |
| LangChain | https://www.langchain.com |
| McKinsey GenAI Report | Search "McKinsey generative AI economic potential" |
| Goldman Sachs GenAI Report | Search "Goldman Sachs generative AI GDP 7 percent" |

---

# 🗂️ PART 2 — Prerequisites & API Basics
> **Class 2** | Colab: [Class 2 Notebook](https://colab.research.google.com/drive/1UB0vlbFbZnqBhPlPRqbNDHW0uAlU6n1F?usp=sharing)

---

## 9. Python Libraries — The "Why"

### The Jungle Analogy

| Scenario | Description | Equivalent |
|---|---|---|
| 🏹 **5000-year-old Shivank** | Hunts a rabbit in the jungle (from scratch) | Writing raw Python code |
| 🍕 **Modern Shivank** | Orders from Swiggy (uses experts, fast) | Using Python Libraries |

> **Python Libraries** = Pre-written expert code so you don't reinvent the wheel.

### Key Libraries
| Library | Use |
|---|---|
| **NumPy** | Numerical operations; e.g., `np.sum([1,2,7,10,50])` |
| **Pandas** | Load & manipulate tabular data (CSV, Excel) into a **DataFrame** |
| **Matplotlib** | Visualization |

```python
# Raw Python (From Scratch)
total = 0
for num in [1, 2, 7, 10, 50]:
    total += num

# With NumPy (Library)
import numpy as np
total = np.sum([1, 2, 7, 10, 50])
```

```python
# Load CSV with Pandas
import pandas as pd
data = pd.read_csv("a.csv")
print(data)   # Stored as a DataFrame
```

> **DataFrame** = The variable that holds your loaded table data in Pandas.

---

## 10. Machine Learning — Predictions on Table Data

### The Astrologer Analogy
> Machine Learning works like an astrologer — it **predicts** the future based on **data**.

### Real-World Examples
- 🌦️ Weather forecast ("will it rain today?")
- 🔍 Google search autocomplete
- 🏏 IPL winning probability during a match

### How It Works — The Core Idea

**Example: Experience → Salary**

| Experience (Years) | Salary |
|---|---|
| 1 | ₹10,000 |
| 2 | ₹20,000 |
| 4 | ₹40,000 |
| 6 | ₹60,000 |
| 3 | ❓ (Predict) |

Your brain derived: `Salary = 10,000 × Experience`

This is exactly what ML does — **find the mathematical function (model) that fits the data**.

```
Goal of ML:
  Given data → Find a mathematical function (model)
             → Use that model to make predictions
             → Minimize the prediction error
```

> **Model** = A mathematical function derived from data, used for predictions.

### Reality Check
- Real-world data is never "perfect"
- Strong **maths foundation** (stats, probability, calculus) = ML becomes easier

---

## 11. Deep Learning — Predictions on Images/Audio/Video

### What's Different?
- ML → works on **structured/tabular data**
- Deep Learning → works on **unstructured data** (images, video, audio)
- Uses **Neural Networks** at its core

### Real-World Examples

#### 📸 Facebook Photo Tagging
- You upload a photo → FB automatically detects and tags faces

#### 🫁 Tuberculosis Detection (Real Project — Portus Hospital)
```
Problem:
  X-ray → Radiologist → 3 days → Result
  90% of cases → No TB (over-prescribed medicine → side effects)

Solution:
  X-ray Image → Deep Learning Model → TB / No TB (instantly)
  If model says NO TB → Immediate relief, no side effects
  If model says YES TB → Still send to radiologist

Result:
  Reduced over-prescription from 90% → 10-20% of patients
```

#### 🚗 Object Detection on Roads
- Cars, trucks, bikes, number plate recognition
- Used in advanced military applications

> **Neural Network** = The algorithm powering Deep Learning predictions.

---

## 12. NLP — Predictions on Text

### What is NLP?
> **Natural Language Processing (NLP)** = Making predictions / generating output based on **human text/language**.

### Examples
| Application | Description |
|---|---|
| Google Search Autocomplete | Predicts what you're typing |
| Alexa / Voice Assistants | Processes spoken language |
| Google Translate | Converts text across languages |
| Gmail Smart Reply | Suggests 3 reply options below an email |

### The Breakthrough: Transformers (2017)
- **Paper:** *"Attention is All You Need"* — Google, 2017
- This single paper made ChatGPT possible
- All authors eventually **left Google** to start their own companies or join OpenAI

> GenAI is simply an **extension of NLP + Transformers**.

---

## 13. The Godfather Paper: "Attention is All You Need"

```
Title:    Attention Is All You Need
Authors:  Vaswani et al. (Google Brain / Google Research)
Year:     2017
Impact:   Foundation of ALL modern LLMs (GPT, BERT, etc.)
```

📄 **[Read the paper](https://arxiv.org/abs/1706.03762)**

**Key concepts introduced:**
- **Transformer architecture** — replaces RNNs with attention mechanisms
- **Self-attention** — understands context of each word relative to others
- **Encoder-Decoder** — basis for translation, summarization, generation

> Without this paper, there is no ChatGPT.

---

## 14. OpenAI API Setup

### Step-by-Step Account Setup

```
1. Go to:  https://platform.openai.com
2. Create account (sign up)
3. Add credit card / debit card details
4. Navigate to:  API Keys → Create new secret key
5. COPY and SAVE the key immediately
   (You cannot view it again after closing the dialog)
6. DO NOT share your API key with anyone
```

> ⚠️ **Warning:** Sharing your secret key = others can rack up charges on your card.

### In Code

```python
import openai

openai.api_key = "sk-xxxxxxxxxxxx"
# Use environment variables in production — never hardcode in shared code
```

---

## 15. Pricing Model & Tokens

### What is a Token?

> **Token** ≈ 4–5 characters ≈ roughly 1 word (simplified rule of thumb)

```
Example: "Who won IPL 2023"
→ Approximately 6 tokens
```

**Two types of tokens:**
| Type | Description | Example |
|---|---|---|
| **Input Token** | Your prompt / question | "Who won IPL 2020?" |
| **Output Token** | ChatGPT's response | "Mumbai Indians won IPL 2020." |

> Both input AND output tokens are billed.

### Pricing Table (as of lecture date)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|---|---|---|---|
| **GPT-3.5 Turbo** | $0.50 | $1.50 | ✅ Recommended for learning |
| GPT-4 | $10 | $30 | ❌ Expensive |
| GPT-4 32K | $60 | $120 | ❌ Very expensive |
| GPT-4 Turbo | $10 | $30 | ❌ Expensive |

> 💡 Use `gpt-3.5-turbo-16k` for all practice.

### 🔍 Token Visualizer
> Try: [platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) — paste any text to see token count.

---

## 16. Hands-On: First API Calls

### Setup

```python
!pip install openai

from openai import OpenAI
client = OpenAI(api_key="YOUR_KEY")
```

### Concept: Message Roles

| Role | Who | Purpose |
|---|---|---|
| `"system"` | GPT / assistant | Tell GPT HOW to behave |
| `"user"` | You (the human) | The actual question/prompt |
| `"assistant"` | GPT's prior response | Used in few-shot prompting |

### Basic API Call

```python
messages = [
    {"role": "system", "content": "You are a very helpful assistant."},
    {"role": "user",   "content": "Who won IPL 2020?"}
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=messages
)

print(response.choices[0].message.content)
# Output: "Mumbai Indians won the IPL in 2020."
```

### Getting JSON Output

```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant designed to output JSON with the key 'answer'."
    },
    {
        "role": "user",
        "content": "Who won IPL 2020?"
    }
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=messages
)

import json
output = json.loads(response.choices[0].message.content)
result = output.get("answer", None)
print(result)
# Output: "Mumbai Indians"
```

> 💡 **Why JSON output?** In LangChain pipelines, the output of one LLM call becomes the input of the next.

### Personality Injection

```python
messages = [
    {"role": "system", "content": "You are a mean teenager assistant."},
    {"role": "user",   "content": "What is machine learning?"}
]
# GPT responded: "Go Google it yourself."
```

> GPT adopts **whatever personality you define** in the system role.

---

## 17. Key Parameters Explained

| Parameter | Values | Effect |
|---|---|---|
| `model` | `"gpt-3.5-turbo-16k"` | Which GPT version to use |
| `max_tokens` | e.g., `50`, `200`, `800` | Max output length; abruptly cuts at limit |
| `temperature` | `0.0` – `1.0` | `0` = deterministic; `1` = highly creative/random |
| `n` | `1` (default) | Number of responses to generate |
| `stop` | `None` or a string | Stops output when this word appears |
| `frequency_penalty` | `0.0` – `1.0` | Penalizes repeated words |
| `presence_penalty` | `0.0` – `1.0` | Penalizes already-mentioned topics |

### Temperature Intuition
```
temperature = 0   → Same answer every time (cold, rigid)
temperature = 0.5 → Some variation (balanced)
temperature = 1   → High creativity, different answer each run (hot, random)
```

### Stop Parameter
```python
stop=["deep learning"]
# GPT stops generating the moment "deep learning" appears
# Useful for: content filters, child-safe apps, staying on topic
```

### Penalty Intuition
```
frequency_penalty = 0  → Words can repeat freely
frequency_penalty = 1  → Penalizes every repeated word

Use high penalty:  long outputs where you want variety
Use low penalty:   technical terms MUST repeat (e.g., "gradient descent")
```

---

## 18. Key Takeaways — Class 2

### 🏗️ Prerequisites Summary
```
Python Basics
  └─► Python Libraries (NumPy, Pandas)
       └─► Machine Learning — predict on table data
            └─► Deep Learning — predict on images/audio
                 └─► NLP — predict on text data
                      └─► Transformers (2017) — the breakthrough
                           └─► Generative AI (ChatGPT, etc.)
```

### 💻 API vs ChatGPT Website

| | ChatGPT Website | OpenAI API (Code) |
|---|---|---|
| Cost | Free (limited) | Paid (per token) |
| Flexibility | Fixed UI only | Full control — build anything |
| Use case | Quick queries | Build products, pipelines, apps |
| Customization | None | System roles, parameters, JSON output |

### 📚 Resources — Class 2
| Resource | Link |
|---|---|
| OpenAI Platform | https://platform.openai.com |
| OpenAI API Docs | https://platform.openai.com/docs |
| Token Visualizer | https://platform.openai.com/tokenizer |
| "Attention is All You Need" | https://arxiv.org/abs/1706.03762 |
| Class 2 Colab Notebook | https://colab.research.google.com/drive/1UB0vlbFbZnqBhPlPRqbNDHW0uAlU6n1F |
| OpenAI Usage Dashboard | https://platform.openai.com/usage |

---

# 🗂️ PART 3 — Prompt Engineering
> **Classes 3 & 4**

---

## 19. Dynamic Prompt Templates with `.format()`

Instead of hardcoding values, use Python's `.format()` to inject values at runtime — like command-line arguments.

```python
base_prompt = """You are a helpful teaching assistant.
The topic is: {0}
Please explain it clearly with examples."""

topic_name = "Autoencoders"
final_prompt = base_prompt.format(topic_name)

print(final_prompt)
# → "You are a helpful teaching assistant.
#    The topic is: Autoencoders
#    Please explain it clearly with examples."
```

> **Why this matters:** In Case Study 3, each row of a dataset gets injected into the prompt one by one — making it scalable over thousands of rows.

---

## 20. Case Study 1 — Financial Document Q&A (Asian Paints)

### Problem Statement
- Company quarterly earnings calls are publicly available (screener.in)
- Reading a full PDF manually is time-consuming
- Goal: Ask GPT specific questions about the document and get precise answers

### Step 1: Mount Google Drive & Read the File

```python
from google.colab import drive
drive.mount('/content/drive')

file_path = "/content/drive/My Drive/genai/"
!ls {file_path}

transcript = ""
with open(file_path + "AsianPaints.txt", "r") as f:
    for line in f:
        transcript += line

print(len(transcript))  # e.g. 43146 characters
```

> **Note:** Convert PDF → TXT first. Libraries like `PyPDF2` also work directly.
> **Clarification:** `max_tokens=800` is the **output** limit, not input. Your 43k-char transcript goes in as input — that's fine.

### Step 2: Write the Base Instruction Prompt

```python
base_instruction = """You are a helpful assistant helping a financial analyst
retrieve relevant financial and business information from a document.

Given below is a question and the transcript of an earnings call of Asian Paints,
attended by the top management of the firm. Try to respond with specific numbers
and facts wherever possible. If you are not sure about the accuracy of the
information, just say: "I do not know."
"""
```

### Step 3: Ask a Question

```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_KEY")

question = "How much has Asian Paints' business grown?"

prompt = base_instruction + "\n\nQuestion: " + question + "\n\nTranscript:\n" + transcript

messages = [{"role": "user", "content": prompt}]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=messages,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Ask Different Questions (Same Structure)

```python
# Summarize financials
question = """Summarize the key financial metrics: revenue growth, 
profitability, cash flow, and debt."""

# Check for acquisitions
question = "Which company has Asian Paints acquired?"
# If info not in doc → GPT replies: "No specific information available."
```

### Key Insight

```
Without GenAI:  Read 40-page PDF manually → find answer
With GenAI:     Pass PDF text + question → get answer in seconds

Critical Rule:
  GPT's training data is pre-2021.
  For latest company data → pass it in the prompt.
  GPT then reasons over YOUR data, not its own training data.
```

### Real-World Applications
- Internal company FAQ chatbot (pass policy docs as context)
- Legal document analyzer
- Support ticket knowledge base

---

## 21. Case Study 2 — Few-Shot Prompting & Conversational AI (Math Tutor)

### What is Few-Shot Prompting?

> **Few-Shot Prompting** = Giving GPT example conversations so it learns *how* to behave, not just *what* to answer.

Three roles in the messages array:

| Role | Who | Purpose |
|---|---|---|
| `"system"` | GPT's personality | Define overall behavior |
| `"user"` | Human | What the human says |
| `"assistant"` | GPT's expected reply | **You write this** — trains GPT's behavior |

### Basic Few-Shot Example

```python
messages = [
    {
        "role": "system",
        "content": """You are an AI tutor that assists school students with math homework.
You never reveal the right answer to the student.
You ask probing questions to identify where the student needs help.
Provide hints and directional feedback. Do NOT reveal the correct answer."""
    },
    # Training examples
    {"role": "user",      "content": "Help me solve: 3x - 9 = 21"},
    {"role": "assistant", "content": "Try moving the -9 to the right side. What do you get?"},
    {"role": "user",      "content": "Is 3x = 12 correct?"},
    {"role": "assistant", "content": "There's a mistake. When you move -9, its sign changes. Try again."},
    {"role": "user",      "content": "3x = 30"},
    {"role": "assistant", "content": "Great! Now divide both sides by 3. What do you get?"},
    {"role": "user",      "content": "x = 10"},
    {"role": "assistant", "content": "Correct! Well done."},
    # New question
    {"role": "user",      "content": "Can you help me solve: 3x - 4 = 7?"}
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=messages
)
print(response.choices[0].message.content)
```

> **Why GPT is bad at math:** GPT was trained on text, not mathematical reasoning. Few-shot prompting helps but doesn't fully fix it. LangChain with calculator tools is the proper solution.

### Making It Conversational (While Loop)

The key problem: after one exchange, GPT forgets the context.
Solution: **keep appending** every message to the history.

```python
MAX_CONVERSATIONS = 20   # Stop after N turns (credit card protection)

message_history = [
    {"role": "system", "content": "You are an AI math tutor..."},
    # ... few-shot examples here ...
]

conversation_length = 0

while conversation_length < MAX_CONVERSATIONS:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Append user message
    message_history.append({"role": "user", "content": user_input})

    # Call GPT with full history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=message_history
    )

    gpt_reply = response.choices[0].message.content
    print(f"GPT: {gpt_reply}")

    # Append GPT's reply
    message_history.append({"role": "assistant", "content": gpt_reply})

    conversation_length += 1
```

### Tracking Token Usage

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo-16k",
    messages=message_history
)

total_tokens = response.usage.total_tokens
print(f"Tokens used this turn: {total_tokens}")

# Accumulate across turns
total_tokens_used += total_tokens
print(f"Total tokens used: {total_tokens_used}")
```

> **Why `MAX_CONVERSATIONS` matters:** Each turn sends the entire history to GPT. Without a limit, a student could run 1000 turns and drain your API credits.

---

## 22. Case Study 3 — Structured Data Extraction & Classification (Laptops)

### Problem Statement
Given a CSV of laptop descriptions, use GPT to:
1. **Classify** each laptop into a category (General / Business / Gamer / Programmer / Multimedia)
2. **Extract** structured attributes (brand, GPU, display, weight, processor, budget) as JSON

```python
import pandas as pd
df = pd.read_csv("/content/drive/My Drive/genai/laptop_descriptions.csv")
print(df.head())
```

### Task A — Classification

#### Step 1: GPT API Function

```python
def get_chat_response_mcq1(user_request):
    system_message = """You are a shopping assistant. The user will give you a
laptop description and some categories with their details.
Find out which category the laptop fits best according to the description.
Give ONLY ONE WORD output — the category name from the list only."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",   "content": user_request}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
    )
    return response.choices[0].message.content
```

#### Step 2: The Prompt with Placeholder

```python
MCQ1_prompt = """From the description of the laptop below, identify what role
the laptop serves. Refer to the key-value pair of categories:

- General: Light web browsing, editing documents.
- Business: Portability, battery backup, general use.
- Gamer: High-performance GPU, high refresh rate.
- Programmer: Strong CPU, high RAM, developer tools.
- Multimedia: Large screen, high-quality audio, video editing.

Laptop Description: {description}
"""
```

#### Step 3: Loop Through Dataset

```python
def tag_laptop(df):
    tagged_df = df.copy()
    laptop_dict = tagged_df.to_dict(orient="records")

    for i, record in enumerate(laptop_dict):
        prompt = MCQ1_prompt.format(description=record["laptop_description"])
        category = get_chat_response_mcq1(prompt)
        tagged_df.loc[i, "category"] = category

    return tagged_df

result_df = tag_laptop(df)
print(result_df.head())
```

### Task B — Structured JSON Extraction

#### Target Structure

```python
output_structure = {
    "brand": "",
    "model_name": "",
    "gpu_processor": "",
    "display_resolution": "",
    "weight": "",
    "processor_clock_speed": "",
    "budget": ""
}
```

#### The Extraction Prompt (Two Inputs)

```python
MCQ2_prompt = """From the laptop description below, extract values for:

{str_input}

Rules:
- Give quantitative, numerical output only (e.g., "2.4 GHz", NOT "very fast")
- Do NOT give qualitative answers or adjectives
- If a value is missing, write "N/A"
- Output in valid JSON format

Example: if processor speed is 2.4 GHz → write "2.4 GHz", NOT "fast"

Laptop Description: {description}
"""
```

#### Loop with Two Inputs

```python
def extract_laptop_info(df):
    result_df = df.copy()
    laptop_dict = result_df.to_dict(orient="records")

    for i, record in enumerate(laptop_dict):
        prompt = MCQ2_prompt.format(
            str_input=str(output_structure),
            description=record["laptop_description"]
        )
        raw_output = get_chat_response_mcq2(prompt)
        result_df.loc[i, "extracted_json"] = raw_output

    return result_df

final_df = extract_laptop_info(df)
print(final_df.head())
```

> **The `str_input` trick:** When you need to pass a Python dict *into* the prompt, use `str()` and `.format(str_input=...)`. Count of `{}` placeholders = number of `.format()` arguments.

---

## 23. The 3-Step Prompt Engineering Framework

This framework works for **any** prompt engineering problem — including interviews.

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Write the GPT API function                     │
│    def get_chat_response(user_request):                 │
│        system_message = "..."  ← changes per problem   │
│        messages = [system, user_request]                │
│        response = client.chat.completions.create(...)   │
│        return response.choices[0].message.content       │
├─────────────────────────────────────────────────────────┤
│  STEP 2: Write the prompt with placeholders             │
│    prompt = """...context...                            │
│    {description}   ← replaced per row at runtime       │
│    {str_input}     ← only if 2nd input needed          │
│    """                                                  │
├─────────────────────────────────────────────────────────┤
│  STEP 3: Loop through data & stitch it together         │
│    for record in data:                                  │
│        final_prompt = prompt.format(                    │
│            description=record["col"],                   │
│            str_input=structure                          │
│        )                                                │
│        result = get_chat_response(final_prompt)         │
│        store result                                     │
└─────────────────────────────────────────────────────────┘
```

> **Interview tip:** When given a dataset + task, this is the template to follow. Only the system message and prompt text change. The structure stays the same every time.

---

## 24. Homework — Wikipedia Q&A Bot

### Goal
Given a question, automatically:
1. Extract the search topic
2. Fetch the relevant Wikipedia page
3. Ask GPT to answer from that page's content

### Step 1: Install & Fetch a Wikipedia Page

```python
!pip install wikipedia-api
import wikipediaapi

def wiki_search(query_term):
    wiki = wikipediaapi.Wikipedia(
        user_agent="my-genai-project",
        language="en"
    )
    page = wiki.page(query_term)
    return page.text  # Full text of the Wikipedia article

context = wiki_search("India")
```

> **`user_agent`** = Like a return address — tells Wikipedia who is sending the request.

### Step 2: Extract Topic from Question (GPT Call #1)

```python
def get_wiki_query(user_request):
    system_message = """The user will ask you a question.
Extract the general topic as a single word or short phrase.

Examples:
- "What is the height of Narendra Modi?" → "Narendra Modi"
- "When was the Eiffel Tower built?" → "Eiffel Tower"
- "Where is the next FIFA World Cup?" → "FIFA World Cup"

Give only the noun/topic. No extra text."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",   "content": user_request}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k", messages=messages
    )
    return response.choices[0].message.content.strip()
```

### Step 3: Answer from Wikipedia (GPT Call #2)

```python
def answer_from_wiki(user_request, context):
    system_message = """You are a helpful assistant that responds to user queries
based on the provided context only.
If you do not find the information, say: "Information not found." """

    content = f"Context:\n{context}\n\nQuestion: {user_request}"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",   "content": content}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k", messages=messages, max_tokens=500
    )
    return response.choices[0].message.content
```

### Full Pipeline

```python
user_request = "Who is the current President of India?"

search_term = get_wiki_query(user_request)   # → "India"
context     = wiki_search(search_term)       # → Full Wikipedia page
answer      = answer_from_wiki(user_request, context)
print(answer)
```

```
Flow:
User Question
    │
    ▼
GPT Call #1: extracts topic → "India"
    │
    ▼
Wikipedia API: fetches full page text
    │
    ▼
GPT Call #2: answers from page context only
    │
    ▼
Final Answer
```

> **Important:** Do NOT load all of Wikipedia. Always fetch only the single relevant page per query.

---

## 25. Rate Limiting & Exponential Backoff

### The Problem
OpenAI limits requests per second. With many concurrent users you get:
```
Error: 429 Too Many Requests
```

### The Solution: Exponential Backoff
```
Attempt 1 → fail → wait 1s
Attempt 2 → fail → wait 2s
Attempt 3 → fail → wait 4s
Attempt 4 → fail → wait 8s
Attempt 5 → fail → wait 16s
Attempt 6 → stop
```

### Implementation with `tenacity`

```python
!pip install tenacity

from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=20),
    stop=stop_after_attempt(6)
)
def get_chat_response_with_backoff(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=messages
    )
    return response.choices[0].message.content
```

> **`@retry` is a Python decorator** — wraps the function and handles retries automatically.
> **When to use:** Not needed for personal learning. Critical for production chatbots with many concurrent users.

---

## 26. Open-Source LLMs via Hugging Face (LLaMA)

### What is Hugging Face?
> **Hugging Face** = The "scikit-learn" of LLM models.

| Analogy | Library |
|---|---|
| Numerical computing | NumPy |
| Classical ML | scikit-learn |
| LLM models | Hugging Face |

### Why Learn LLaMA?

| | OpenAI (GPT) | Meta LLaMA |
|---|---|---|
| Cost | Paid (per token) | Free |
| Speed | Fast (~2-5s) | Slow (2-8 min on T4 GPU) |
| Privacy | Data sent to OpenAI | Runs locally |
| Customization | Limited | Full access to model weights |

### 3 Steps to Access LLaMA

```
Step 1: Request access from Meta
   → https://llama.meta.com/
   → Fill in name, email, use case
   → Select models (LLaMA 2, 3, etc.)
   → Approval: ~15-20 minutes

Step 2: Request model permission on Hugging Face
   → https://huggingface.co/meta-llama/
   → Log in with SAME email as Step 1 ← CRITICAL
   → Click each model → Request Access → Submit

Step 3: Create a Hugging Face token
   → https://huggingface.co/settings/tokens
   → New Token → Choose "Read" → Copy & save
```

### Colab Setup: Switch to GPU

```
Runtime → Change runtime type → T4 GPU → Save
```

> LLaMA **will not run on CPU** in any reasonable time.

### Install & Load Model

```python
!pip install transformers accelerate

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

HF_TOKEN  = "hf_xxxxxxxxxxxx"
model_id  = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
# Downloads ~10 GB — takes a few minutes
```

### Inference Pipeline

```python
def run_llama(prompt_text):
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        token=HF_TOKEN
    )
    output = pipe(
        prompt_text,
        max_new_tokens=500,
        do_sample=True,
        top_k=50,
        eos_token_id=tokenizer.eos_token_id
    )
    return output[0]["generated_text"]
```

### LLaMA Prompt Template

LLaMA uses a specific format (different from OpenAI's messages list):

```python
def build_llama_prompt(system_message, user_message):
    return f"""<s>[INST] <<SYS>>
{system_message}
<</SYS>>

{user_message} [/INST]"""

# Example
system = "You are a helpful, respectful, and honest assistant."
user   = "I like Friends and Money Heist. Recommend similar shows to watch."

prompt = build_llama_prompt(system, user)
result = run_llama(prompt)
print(result)
```

### OpenAI vs LLaMA — Structural Comparison

| Aspect | OpenAI (GPT) | LLaMA (Hugging Face) |
|---|---|---|
| Auth | `openai.api_key` | `token=HF_TOKEN` |
| Message format | `[{"role": ..., "content": ...}]` | `[INST]`, `<<SYS>>` tags |
| Speed | ~2-5 seconds | 2-8 minutes (T4 GPU) |
| Cost | ~$0.50/1M input tokens | Free |
| Response extraction | `response.choices[0].message.content` | `output[0]["generated_text"]` |

---

## 27. Key Takeaways — Classes 3 & 4

### 🏗️ Prompt Engineering Core Principles

1. **Prompt writing takes time.** Even experienced engineers spend 20–30+ minutes per prompt. That's normal.
2. **Start with one example; add more if output is wrong.** More examples = better behavior.
3. **Be explicit about output format.** One word, JSON, numerical values — always state it.
4. **Tell GPT what NOT to do.** "Do not give qualitative answers", "If unknown, say I do not know."
5. **Use the 3-step framework** for any classification / extraction / Q&A problem.

### 🧠 When to Use Each Approach

| Scenario | Approach |
|---|---|
| Question on general knowledge | Plain GPT (no additional context) |
| Question on your own documents | Pass document as context in the prompt |
| Teach GPT a specific behavior | Few-shot prompting (assistant role examples) |
| Make a chatbot conversational | Append all messages to `message_history` |
| Classify/extract from many rows | 3-step framework + `.format()` loop |
| Free alternative to OpenAI | LLaMA via Hugging Face (slower, free) |
| Production with many users | Add exponential backoff with `tenacity` |

### 💡 The Real-World Pattern

```
GenAI chatbot = Your domain knowledge + GPT reasoning

Example:
  Instead of: employee reads 200-page policy manual
  You build:  pass policy PDF as context → chatbot answers questions

Same pattern applies to:
  - Support ticket classification   (Case Study 3)
  - Earnings call analysis          (Case Study 1)
  - Math tutoring                   (Case Study 2)
  - Medical document Q&A
  - Legal contract review
```

### 📚 Resources — Classes 3 & 4
| Resource | Link |
|---|---|
| Screener.in (company financials) | https://www.screener.in |
| Hugging Face | https://huggingface.co |
| LLaMA access form (Meta) | https://llama.meta.com |
| Hugging Face token page | https://huggingface.co/settings/tokens |
| Meta LLaMA 3 8B Instruct | https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct |
| Wikipedia API (Python) | https://pypi.org/project/Wikipedia-API |
| tenacity (retry library) | https://tenacity.readthedocs.io |
| OpenAI rate limits docs | https://platform.openai.com/docs/guides/rate-limits |

---

## 🔗 About the Author

> These notes were compiled by **Ishwar Ambare** as part of a personal learning journey through the Scalar GenAI Basics Module.
>
> 📌 **LinkedIn:** [linkedin.com/in/ishwar-ambare](https://www.linkedin.com/in/ishwar-ambare/)

---

*Generative AI Complete Notes — Classes 1 to 4 | Scalar GenAI Basics Module*

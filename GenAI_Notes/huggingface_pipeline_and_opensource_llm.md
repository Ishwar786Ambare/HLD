# 🤗 HuggingFace Pipeline & Open-Source LLMs
### GenAI Practical Session — Detailed Notes

> **Source:** Lecture Transcript + [Colab Notebook](https://colab.research.google.com/drive/1oogmpdKzzf3o8BpgWxpKz5Vp72jzsWaZ?usp=sharing) + [HuggingFace Pipeline Docs](https://huggingface.co/docs/transformers/pipeline_tutorial) + [HuggingFace Models](https://huggingface.co/models)

---

## 📋 Table of Contents

1. [Recap — What We've Covered So Far](#1-recap--what-weve-covered-so-far)
2. [Open-Source AI Market](#2-open-source-ai-market)
3. [Why NOT Train Your Own Model?](#3-why-not-train-your-own-model)
4. [Language Model vs Large Language Model](#4-language-model-vs-large-language-model)
5. [Benefits of Open-Source LLMs](#5-benefits-of-open-source-llms)
6. [Real-World Companies Using Open-Source LLMs](#6-real-world-companies-using-open-source-llms)
7. [Hugging Face Platform](#7-hugging-face-platform)
8. [Setup — Installation](#8-setup--installation)
9. [HuggingFace Pipeline — Core Concept](#9-huggingface-pipeline--core-concept)
10. [Pipeline Tasks with Code Examples](#10-pipeline-tasks-with-code-examples)
    - [Sentiment Analysis](#-sentiment-analysis)
    - [Summarization](#-summarization)
    - [Zero-Shot Classification](#-zero-shot-classification)
    - [Text Generation](#-text-generation)
    - [Named Entity Recognition (NER)](#-named-entity-recognition-ner)
    - [Automatic Speech Recognition (ASR)](#-automatic-speech-recognition-asr)
    - [Image Classification (Multimodal)](#-image-classification-multimodal)
11. [Advanced Pipeline Parameters](#11-advanced-pipeline-parameters)
12. [How to Find & Use Models from HuggingFace Hub](#12-how-to-find--use-models-from-huggingface-hub)
13. [Transformer Architecture — Recap](#13-transformer-architecture--recap)
14. [RAG — Retrieval Augmented Generation (Preview)](#14-rag--retrieval-augmented-generation-preview)
15. [Data Sources for AI/ML Projects](#15-data-sources-for-aiml-projects)
16. [Homework Assignment](#16-homework-assignment)
17. [Quick Reference Cheatsheet](#17-quick-reference-cheatsheet)

---

## 1. Recap — What We've Covered So Far

In previous sessions we covered the **fundamentals of NLP**:
- How computers interpret language
- How words in a sentence are related
- How machines understand sarcasm
- Tokenization, embeddings, attention mechanism
- Transformer architecture (Encoder–Decoder)

**Today's goal:** Move from theory → **practical application** using pre-existing open-source models.

---

## 2. Open-Source AI Market

### What is Open Source?
Open source software makes its **source code freely available** for anyone to use, modify, and distribute — no licensing fees for commercial use.

| Type | Example | Cost |
|---|---|---|
| Closed-source AI | ChatGPT (OpenAI) | Free for personal use; **paid API** for commercial |
| Freemium | NVIDIA NIM | Free credits initially, then pay-per-use |
| Fully Open Source | Meta Llama 3.1 (via HuggingFace) | **Free** |

> **Key Insight:** ChatGPT cannot be used commercially without an API key and billing. Open-source models like Llama can be used in your products for **free**.

---

## 3. Why NOT Train Your Own Model?

Three major barriers make training from scratch impractical for individuals and small teams:

| Barrier | Details |
|---|---|
| **Data (Corpus)** | Need billions of tokens of text data — individuals simply don't have this |
| **Compute** | GPUs/TPUs cost millions of dollars to rent for training |
| **Time** | Training can take months; you can't keep a laptop running continuously for a year |

> ✅ **Solution:** Use **pre-trained models** (LLMs) that have already invested in all three. We fine-tune or use them via API.

---

## 4. Language Model vs Large Language Model

| Feature | Language Model (LM) | Large Language Model (LLM) |
|---|---|---|
| **Nature** | Probabilistic | Probabilistic + Deep learning |
| **Capability** | Predict next **word** | Predict next sentence, paragraph, or document |
| **Scale** | Small | Billions of parameters |
| **Examples** | n-gram models | GPT-4, Llama 3.1, Gemma |

---

## 5. Benefits of Open-Source LLMs

### 1. 💰 Cost Effective
- Build production-grade AI products with **zero licensing costs**
- No per-API-call charges

### 2. 🔒 Data Ownership & Control
- Data stays **on your infrastructure** — no third-party data exposure
- You can set compliance rules, GDPR policies, access controls
- Contrast: When you send data to ChatGPT API, it leaves your control

### 3. 🔓 No Vendor Lock-in
- Not dependent on a single provider (e.g., if NVIDIA drops you, pivot to HuggingFace)
- Freedom to **modify** and **integrate** with any system

### 4. 🛡️ Security & Privacy via Community Scrutiny
- Open-source code is publicly visible (like pandas on GitHub)
- Community patches vulnerabilities quickly
- Companies like OpenAI hire **ethical hackers** to find vulnerabilities in closed models

### 5. 🛠️ Customization & Specialization
- Build domain-specific tools (e.g., Tableau voice extension, Excel formula generator)
- Fine-tune models on your own data for specialized tasks
- Example: Integrate Voice-to-Text → LLM → actions in one pipeline

---

## 6. Real-World Companies Using Open-Source LLMs

| Company | Usage |
|---|---|
| **VMware** | Open Language Model powered by **HuggingFace StarCoder** |
| **Brave Browser** | Chatbot assistant **Leo** — originally Llama 2, upgraded to **Mixtral (by Mistral AI)** |
| **IBM** | Watson orchestration platform — **Ask HR** use case |
| **Mastercard** | Internal chatbot for employee assistance |

---

## 7. Hugging Face Platform

**URL:** [huggingface.co](https://huggingface.co)

> "The platform where the ML community collaborates on models, datasets, and applications."

### What's Available

| Section | Description |
|---|---|
| **Models** | 100,000+ pre-trained models (text, image, audio, multimodal) |
| **Datasets** | Curated datasets for training/fine-tuning |
| **Spaces** | Hosted model demos (powered by Gradio/Streamlit) |

### Key Facts
- Use models **without even logging in** (for most models)
- Models hosted for **free** — no charges like NVIDIA
- Direct access to Meta's **Llama 3.1**, Stability AI's **Stable Diffusion 3**, OpenAI's **Whisper**, and more

---

## 8. Setup — Installation

```python
# Install in Google Colab or local environment
!pip install datasets transformers[sentencepiece]
```

> **Note:** PyTorch is a dependency of transformers but **gets installed automatically** — you don't need to install it separately in Colab.

---

## 9. HuggingFace Pipeline — Core Concept

### What is a Pipeline?

The `pipeline` object is the **simplest and most powerful** inference API in HuggingFace Transformers.

```
Pipeline = Model Download + Preprocessing + Forward Pass + Post-processing
```

Think of it like:
- **Streamlit** hides the complexity of web servers, sockets, HTML/CSS
- **Keras** hides the complexity of TensorFlow operations
- **Pipeline** hides all the complex ML code — tokenization, attention, decoding

### Basic Usage

```python
from transformers import pipeline

# Create a pipeline for a specific task
my_pipeline = pipeline("task-name")

# Run inference
result = my_pipeline("your input text")
```

### What Happens Under the Hood

```
Raw Text Input
     ↓
Convert to Embeddings (Numbers)
     ↓
Attention Mechanism (find important relationships)
     ↓
Logits (raw scores per class)
     ↓
Softmax → Prediction (label + confidence score)
```

### Default Model Selection

When you don't specify a model, pipeline selects a **default pre-trained model**:
- `"sentiment-analysis"` → defaults to `distilbert-base-uncased-finetuned-sst-2-english`
- `"summarization"` → defaults to `facebook/bart-large-cnn` (~1.22 GB)
- `"zero-shot-classification"` → defaults to `facebook/bart-large-mnli`

Models are **downloaded once and cached** locally — subsequent calls are fast.

---

## 10. Pipeline Tasks with Code Examples

### 📊 Sentiment Analysis

**Task:** Determine if text is positive or negative.

```python
from transformers import pipeline

# Initialize
classifier = pipeline("sentiment-analysis")

# Single sentence
result = classifier("Food is delicious!")
# Output: [{'label': 'POSITIVE', 'score': 0.9998}]

# Tricky sentences
classifier("I wish food was good")
# Output: [{'label': 'NEGATIVE', 'score': 0.7762}]
# Note: "I wish" implies something is currently NOT the case → NEGATIVE ✅

classifier("I wish food was good!")  # With exclamation mark
# Output: [{'label': 'POSITIVE', ...}]
# Note: Exclamation marks often appear in positive/excited sentences → model flips

# Mixed sentiment
classifier("I'm amazed by the speed of the processor but disappointed that it heats up quickly.")
# Output: [{'label': 'NEGATIVE', 'score': 0.9983}]
# Note: "disappointed" has more weight here

# Multiple sentences at once (pass a list)
classifier([
    "I've been waiting for a HuggingFace course my whole life.",
    "I hate this so much!"
])
# Output: [{'label': 'POSITIVE', 'score': 0.9598}, {'label': 'NEGATIVE', 'score': 0.9994}]
```

> **Key Insight:** Default models are NOT perfect — they need **fine-tuning** for production use. Exclamation marks influenced the model's sentiment because training data has exclamation marks more commonly in positive contexts.

---

### 📝 Summarization

**Task:** Condense long text into a shorter summary.

```python
from transformers import pipeline

summary = pipeline("summarization")

text = """
America has changed dramatically during recent years. Not only has the number of graduates
in traditional engineering disciplines declined, but in most of the premier American universities,
engineering curricula now concentrate on theoretical and analytical skills rather than the
design-and-build skills that industrial employers actually need. The result is a severe supply-demand
mismatch for engineering graduates. China and India, while continuing to invest in basic and
theoretical knowledge, are graduating six and eight times as many traditional engineers
as does the United States.
"""

result = summary(text)
# Output: [{'summary_text': 'America has changed dramatically during recent years. The number of
# graduates in traditional engineering disciplines has declined. China and India graduate six and
# eight times as many traditional engineers as the U.S.'}]
```

**How it works (Encoder-Decoder flow):**

```
Long Text Input
     ↓
ENCODER
  ├── Tokenizes text into words/subwords
  ├── Converts tokens to embeddings (numbers + positional encoding)
  └── Attention mechanism → builds rich contextual understanding
     ↓
State Representation (rich understanding of text)
     ↓
DECODER
  ├── Selects the most important information
  ├── Organizes it logically
  └── Generates concise output
     ↓
Summary Text Output
```

---

### 🏷️ Zero-Shot Classification

**Task:** Classify text into user-defined labels **without any training data**.

> **The Problem:** In real projects, you rarely have labeled training data. Labeling is:
> - Time-consuming
> - Expensive (needs smart annotators)
> - Resource-intensive

**Zero-shot classification solves this** — you define your own labels at runtime.

```python
from transformers import pipeline

zero_shot = pipeline("zero-shot-classification")

# Example: News classification for a media app
text = "India won 2 bronze medals in Pistol shooting"
candidate_labels = ["sports", "business", "education"]

result = zero_shot(text, candidate_labels=candidate_labels)
# Output: {'labels': ['sports', 'education', 'business'],
#           'scores': [0.9849, 0.0096, 0.0054]}
# → Correctly classified as "sports" with 98.5% confidence!
```

**Use Case:** News tagging for apps like **InShorts** — automatically categorize incoming news into Politics, Business, Sports, Education, etc. without a labeled training set.

> **Model Used:** `facebook/bart-large-mnli` (Multi-Genre Natural Language Inference)

---

### ✍️ Text Generation

**Task:** Auto-complete or extend given text.

```python
from transformers import pipeline

# Default model
generator = pipeline("text-generation")

result = generator("In this course, we're gonna learn how to")
# Output: [{'generated_text': 'In this course, we\'re gonna learn how to create a simple
# user-friendly interface...'}]

# Specifying a model with parameters
generator = pipeline("text-generation", model="distilgpt2")

result = generator(
    "I am designing a course in data science, its curriculum should include",
    max_length=100,        # Limit output length
    num_return_sequences=2  # Get 2 different responses
)
# Returns 2 different completions of 100 words each
```

**Parameters Explained:**

| Parameter | Description |
|---|---|
| `max_length` | Maximum number of tokens in the output |
| `num_return_sequences` | Number of different text completions to generate |
| `model` | Specify which model to use (overrides default) |

---

### 🏷️ Named Entity Recognition (NER)

**Task:** Identify and classify named entities (persons, organizations, locations) in text.

```python
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
# grouped_entities=True: groups multi-token entities (e.g., "Scaler Pvt Ltd" as one ORG)

text = "My name is Suraaj, I work with Scaler Pvt Ltd as a senior manager in Data Science located in Bangalore"

result = ner(text)
# Output:
# [{'entity_group': 'PER', 'word': 'Suraaj', 'score': 0.99},
#  {'entity_group': 'ORG', 'word': 'Scaler Pvt Ltd', 'score': 0.98},
#  {'entity_group': 'LOC', 'word': 'Bangalore', 'score': 0.99}]
```

**Entity Types:**

| Tag | Meaning | Example |
|---|---|---|
| `PER` | Person | Suraaj, Arjun |
| `ORG` | Organization | Scaler Pvt Ltd |
| `LOC` | Location | Bangalore |
| `MISC` | Miscellaneous | Data Science (sometimes) |

> **Limitation:** Default models aren't perfect — capitalization of words significantly affects detection. Fine-tuning improves results.

---

### 🎙️ Automatic Speech Recognition (ASR)

**Task:** Convert audio/speech into text.

```python
from transformers import pipeline

# Using OpenAI's Whisper model (one of the best ASR models)
transcriber = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-large-v3"
)

# From a URL (audio file)
result = transcriber("https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac")
# Output: {'text': ' I have a dream that one day this nation will rise up and live out the true meaning of its creed.'}

# With word-level timestamps
result = transcriber(
    audio="path/to/audio.flac",
    return_timestamp="word"
)
# Output includes: {'text': '...', 'chunks': [{'text': ' I', 'timestamp': (0.0, 1.1)}, ...]}
```

**Live Voice → Text Workflow:**

```
Live Microphone Input
     ↓
Voice capture library (e.g., pyaudio, streamlit audio)
     ↓
Save audio to temp file (WAV/MP3 format)
     ↓
Pass to Whisper Pipeline
     ↓
Transcribed Text Output
     ↓
Delete temp file
```

> **Whisper** by OpenAI is open-source and one of the most accurate speech recognition models available on HuggingFace.

---

### 🖼️ Image Classification (Multimodal)

**Task:** Classify images or extract information from images using text queries.

```python
from transformers import pipeline

# Visual Question Answering — multimodal (image + text → text)
vqa_pipeline = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa"
)

result = vqa_pipeline(
    image="path/to/invoice.jpg",
    question="What is the invoice number?"
)
# Model reads the invoice image and returns the invoice number
```

**What "Multimodal" Means:**

```
Image Input → Computer Vision Model → Extract text/features
                                              ↓
                           Text Query → NLP Understanding → Answer
                                              ↓
                                      Final Text Output
```

> **Gradio Integration:** HuggingFace pipelines work directly with Gradio — you can build a UI without writing any frontend code:
> ```python
> import gradio as gr
> gr.Interface.from_pipeline(pipeline).launch()
> ```

---

## 11. Advanced Pipeline Parameters

### Specifying a Different Model

```python
# Override default model
pipeline = pipeline("text-classification", model="roberta-base")
```

### Hardware Configuration

```python
# CPU (default)
pipeline = pipeline("text-generation", model="gpt2", device=-1)

# GPU (CUDA device 0)
pipeline = pipeline("text-generation", model="gpt2", device=0)

# Auto distribute across devices (with Accelerate)
from accelerate import Accelerator
pipeline = pipeline("text-generation", model="google/gemma-2-2b", device_map="auto")
```

### Batch Inference

```python
# Process multiple inputs at once (useful for large datasets)
pipeline = pipeline("text-generation", model="gpt2", device=0, batch_size=8)

# Pass all inputs as a list
pipeline(["text1", "text2", "text3", "text4"])
```

**Batch Inference Rules of Thumb:**

| Scenario | Use Batch? |
|---|---|
| Live/real-time inference | ❌ No — adds latency |
| Using CPU | ❌ No — little benefit |
| Large GPU with big dataset | ✅ Yes — significant speedup |
| Unknown sequence lengths | ❌ No — OOM risk |

### Large Datasets — Streaming

```python
from transformers.pipelines.pt_utils import KeyDataset
from datasets import load_dataset

dataset = load_dataset("imdb", split="test")
pipeline = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Stream results without loading entire dataset into memory
for out in pipeline(KeyDataset(dataset, "text"), batch_size=8):
    print(out)
```

### Memory Optimization — Half Precision

```python
import torch

# Use bfloat16 for faster inference with less memory
pipeline = pipeline("text-generation", model="google/gemma-2-2b", 
                    dtype=torch.bfloat16, device_map="auto")
```

### Memory Optimization — Quantization

```python
from transformers import BitsAndBytesConfig
import torch

pipeline = pipeline(
    model="google/gemma-7b",
    dtype=torch.bfloat16,
    device_map="auto",
    model_kwargs={"quantization_config": BitsAndBytesConfig(load_in_8bit=True)}
)
```

---

## 12. How to Find & Use Models from HuggingFace Hub

### Step-by-Step Process

1. **Go to** [huggingface.co/models](https://huggingface.co/models)
2. **Filter by task** — select the task (e.g., Text Classification, Text-to-Image)
3. **Sort by:** Downloads (most stable, community-supported) or Trending
4. **Click on a model** — read the model card (what it can do, training data, benchmarks)
5. **Click "Use this model"** → Select `Transformers`
6. **Copy the code snippet** → paste into your notebook/script

### Finding Models for Specific Tasks

| Your Task | HuggingFace Task Category |
|---|---|
| English → SQL | Text Generation / Question Answering |
| News categorization | Zero-Shot Classification / Text Classification |
| Image captioning | Image-to-Text |
| Generate images | Text-to-Image |
| Voice assistant | Automatic Speech Recognition |
| Invoice processing | Document Question Answering |

### Best Model for English → SQL

**→ Meta Llama 3.1** (recommended)

```python
# Direct code from HuggingFace model card
from transformers import pipeline

sql_gen = pipeline("text-generation", model="meta-llama/Meta-Llama-3.1-8B-Instruct")

prompt = """Convert the following to SQL:
Give me the department with the maximum number of employees.
The table 'employees' has columns: id, name, department, salary.
"""

result = sql_gen(prompt, max_new_tokens=200)
print(result[0]['generated_text'])
```

> **Pro Tip:** When prompting for SQL, include the table schema in your prompt so the model knows the structure.

---

## 13. Transformer Architecture — Recap

How summarization (and most LLMs) work internally:

```
INPUT TEXT
     │
     ▼
┌──────────────────────────────────────┐
│              ENCODER                 │
│                                      │
│  1. Tokenize text into words         │
│  2. Convert words → embeddings       │
│  3. Add positional encodings         │
│  4. Self-Attention mechanism:        │
│     - Find important word pairs      │
│     - Build contextual meaning       │
└──────────────────────────────────────┘
     │
     ▼
[Rich Contextual Representation of All Text]
     │
     ▼
┌──────────────────────────────────────┐
│              DECODER                 │
│                                      │
│  1. Select most important info       │
│  2. Organize logically               │
│  3. Generate token-by-token          │
│  4. Apply beam search / sampling     │
└──────────────────────────────────────┘
     │
     ▼
OUTPUT (Summary / Translation / Generation)
```

---

## 14. RAG — Retrieval Augmented Generation (Preview)

> **Q: How do I train a model on my own data and ask it questions?**

**Answer:** That's **RAG** — Retrieval Augmented Generation.

- Store your custom documents in a **vector database**
- When a user asks a question, **retrieve** relevant chunks from your documents
- **Augment** the LLM prompt with retrieved context
- LLM generates an **accurate, grounded answer**

This is covered in a dedicated upcoming module. Stay tuned!

---

## 15. Data Sources for AI/ML Projects

When people ask "where do companies get training data?"

| Source | Details |
|---|---|
| **APIs** | Official data APIs (e.g., Twitter API, Google Analytics) |
| **Data Vendors** | Third-party companies that sell datasets in CSV/JSON format |
| **Internal Data** | Company's own operational data (uploaded to cloud like AWS S3) |
| **Kaggle** | Public datasets for practice/benchmarking |
| **HuggingFace Datasets** | Open-source curated datasets |
| **Web Scraping** | ⚠️ **Caution:** Illegal in many countries; constitutes copyright infringement in India |

> **For Production:** Always use APIs or licensed data. Web scraping violates terms of service and copyright law.

---

## 16. Homework Assignment

**Task:** Find and use a HuggingFace model that converts English to SQL.

**Hints:**
1. What type of model is this? → **Text-to-Text**
2. What task does it perform? → **Question Answering** or **Text Generation**
3. Search [huggingface.co/models](https://huggingface.co/models) with filter: `text-generation`
4. Recommended model: **Meta-Llama 3.1**
5. Provide schema in the prompt: `"Table employees has columns: id, name, dept. Write SQL to find the department with maximum employees."`

---

## 17. Quick Reference Cheatsheet

```python
from transformers import pipeline

# ── SENTIMENT ANALYSIS ──────────────────────────────────────────
clf = pipeline("sentiment-analysis")
clf("I love this product!")              # POSITIVE
clf(["text1", "text2"])                  # Batch

# ── SUMMARIZATION ───────────────────────────────────────────────
summarizer = pipeline("summarization")
summarizer(long_text)

# ── ZERO-SHOT CLASSIFICATION ────────────────────────────────────
zsc = pipeline("zero-shot-classification")
zsc("some news text", candidate_labels=["sports", "politics", "business"])

# ── TEXT GENERATION ──────────────────────────────────────────────
gen = pipeline("text-generation", model="distilgpt2")
gen("Once upon a time", max_length=100, num_return_sequences=2)

# ── NAMED ENTITY RECOGNITION ─────────────────────────────────────
ner = pipeline("ner", grouped_entities=True)
ner("My name is Elon Musk, CEO of Tesla based in Austin")

# ── SPEECH RECOGNITION ───────────────────────────────────────────
asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
asr("path/to/audio.flac")

# ── QUESTION ANSWERING ───────────────────────────────────────────
qa = pipeline("question-answering")
qa(question="Who won the match?", context="India won the cricket match against Australia.")

# ── IMAGE CLASSIFICATION ─────────────────────────────────────────
img_clf = pipeline("image-classification")
img_clf("path/to/image.jpg")

# ── ADVANCED: GPU + BATCH + QUANTIZATION ─────────────────────────
import torch
from transformers import BitsAndBytesConfig

fast_pipeline = pipeline(
    "text-generation",
    model="google/gemma-7b",
    device_map="auto",
    dtype=torch.bfloat16,
    batch_size=8,
    model_kwargs={"quantization_config": BitsAndBytesConfig(load_in_8bit=True)}
)
```

---

## 📚 Resources

| Resource | Link |
|---|---|
| HuggingFace Models | [huggingface.co/models](https://huggingface.co/models) |
| Pipeline Tutorial (Official) | [HF Pipeline Docs](https://huggingface.co/docs/transformers/pipeline_tutorial) |
| Colab Notebook (Demo) | [Open in Colab](https://colab.research.google.com/drive/1oogmpdKzzf3o8BpgWxpKz5Vp72jzsWaZ?usp=sharing) |
| Llama 3.1 on HuggingFace | [meta-llama/Meta-Llama-3.1-8B](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct) |
| Whisper (OpenAI ASR) | [openai/whisper-large-v3](https://huggingface.co/openai/whisper-large-v3) |
| Stable Diffusion 3 | [stabilityai/stable-diffusion-3-medium](https://huggingface.co/stabilityai/stable-diffusion-3-medium) |

---

*Notes created from lecture transcript · Practical class on GenAI · April 2026*

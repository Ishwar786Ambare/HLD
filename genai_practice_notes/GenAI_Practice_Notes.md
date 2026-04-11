# 🤖 GenAI Practice Sessions — Preparation Notes

> **Lectures 1 & 2** | ChatGPT for Data Science, Python Automation & NumPy/Pandas  
> Instructor: Shivank | Tool: ChatGPT (Free tier) + Thonny + Google Colab

---

## 📌 Table of Contents

1. [Key Philosophy](#1-key-philosophy)
2. [Lecture 1 — ChatGPT Prompting Basics + Python Automation](#2-lecture-1--chatgpt-prompting-basics--python-automation)
   - [Prompting Techniques](#21-prompting-techniques)
   - [Free Token Hack](#22-free-token-hack)
   - [Python Exercises in Thonny](#23-python-exercises-in-thonny)
   - [Streamlit Web Apps](#24-streamlit-web-apps)
3. [Lecture 2 — Advanced Prompting for NumPy/Pandas](#3-lecture-2--advanced-prompting-for-numpypandas)
   - [Case Study 1: Categorical Encoding](#31-case-study-1-categorical-encoding-survey-data)
   - [Case Study 2: E-Commerce Churn Prediction](#32-case-study-2-e-commerce-churn-prediction)
   - [Descriptive Analysis Shortcut](#33-descriptive-analysis-shortcut)
   - [Feature Engineering via GPT](#34-feature-engineering-via-gpt)
   - [Handling GPT's Memory Problem](#35-handling-gpts-memory-problem)
4. [Golden Rules & Best Practices](#4-golden-rules--best-practices)
5. [Where GPT Helps vs. Doesn't](#5-where-gpt-helps-vs-doesnt)
6. [Quick Reference: Prompt Templates](#6-quick-reference-prompt-templates)

---

## 1. Key Philosophy

> *"Don't get overdependent on GPT. It helps in take-home assignments and company work, but NOT in live interviews. Learn the fundamentals — use GPT as your accelerator."*

- GPT doesn't eliminate jobs — it **reduces headcount needed**. (4 people → 2 people for the same project)
- A task that takes **8 hours** can now take **4–5 hours** with GPT.
- Non-tech people can now do data science / engineering jobs using GPT.
- **Your job**: guide GPT correctly. GPT makes mistakes — your domain knowledge fixes them.

---

## 2. Lecture 1 — ChatGPT Prompting Basics + Python Automation

### 2.1 Prompting Techniques

#### Technique 1: Fill in the Blank
Leave the sentence incomplete with `...` or `?` — GPT will complete it.

```
The process of deriving insights from data is called ...
```

---

#### Technique 2: Constrained / One-Word Answer (Few-Shot Prompting)
Provide an example Q&A pair to teach GPT the exact format you want.

```
Using the example complete the request:

Q: What is the most popular language for data analysis?
A: Python

Q: What is the most popular data file format for data analysis?
A: ?
```
> GPT learns from the example → returns just `CSV` (one word, nothing extra).

---

#### Technique 3: Multi-Shot Prompting
Same as above but with **multiple** example pairs to reinforce the pattern.

```
Complete using the examples:

Q1: ... A1: ...
Q2: ... A2: ...
Q3: ... A3: ...

Request: [Your actual question]
```

---

#### Technique 4: Persona Prompting
Tell GPT to act as a specific character. Useful for presentations to non-technical stakeholders.

```
You are Shakespeare. What is data analysis?
```

```
You are a very experienced CEO of an e-commerce company selling shoes through a mobile app.
Answer the question: What is data analysis for you?
```
> Result: GPT explains the concept using examples from the persona's world (shoe sales, mobile app metrics, etc.)

**Real-world use case**: Before a presentation to your VP/CEO, ask GPT to adopt their persona and explain your project from their perspective. Then use those examples in your slides.

---

#### Technique 5: Let GPT Ask You Questions First
```
I want a high-level overview of the process of data analysis.
I haven't done this before and I don't know the terminology.
Ask me as many questions as you need, then give me a relevant answer.
```
> GPT asks about your background, data sources, tools, team, challenges → then tailors its explanation to you.

---

#### Technique 6: Explain Like I'm 10 (ELI10)
```
What is data analysis? Explain like to a 10-year-old.
```
> Creates a simple, analogy-based explanation accessible to **any** audience — great for all-hands presentations.

---

### 2.2 Free Token Hack

| Situation | Solution |
|-----------|----------|
| Token limit reached | Log out → Log in with another Gmail account |
| 24 hours later | Original account resets — use again |
| Production system | Must pay for API — cannot switch accounts |

> Gmail doesn't restrict the number of accounts. Keep rotating freely for personal/learning projects.

---

### 2.3 Python Exercises in Thonny

> **Thonny** (nicknamed "Thanos") — lightweight Python IDE. Install from thonny.org  
> For missing packages: **Tools → Manage Packages** → search name → Install

---

#### Exercise 1: Uppercase First Letter of Every Sentence

**Problem**: Three `.txt` files had every sentence starting with lowercase.

**Prompt:**
```
I have multiple text files in a folder named 'files'.
Each text file contains text but the sentences start with a lowercase character.
I want to convert the first letter of each sentence of each file to uppercase.
Write me a Python script for that.
```

**Key learning**: GPT handles regex parsing automatically.

---

#### Exercise 2: Merge Multiple .txt Files into One

```
I have multiple text files in a folder named 'files'.
Each text file contains some text.
I want to merge all these text files into a single text file.
Write a Python script for that.
```

---

#### Exercise 3: Create 100 Files with Indian Girl Names *(Class Exercise)*

```
I want to create 100 text files.
Each text file should contain a different Indian girl name.
Write a Python script for that.
```
> GPT auto-generates 100 names and writes the file creation code.

---

#### Exercise 4: Add Annual Salary Column to Excel Files

```
I have multiple Excel files in a folder called 'excel_files'.
Each Excel file contains two columns: Employee and Monthly Salary.
I want to add a new column called 'Annual Salary' to each Excel file.
Annual Salary = Monthly Salary x 12.
Write a Python script for that.
```
> Uses **pandas** + **openpyxl**. Install via: Tools → Manage Packages → pandas → Install

---

#### Exercise 5: Merge Excel Files (with Error Recovery)

```
I have multiple Excel files in the 'excel_files' folder.
They all contain the same columns.
I want to merge all Excel files into one single Excel file.
Write me a Python script for that.
```

**Error encountered**: `Excel file format cannot be determined. You can specify an engine manually.`

**Fix prompt:**
```
I am getting the below error:
[paste error message here]

Rewrite the Python script.
```
> GPT fixes it by explicitly adding `engine='openpyxl'`.

---

#### Exercise 6: Divide CSV Column Values by 10

```
I have a file called sherlock_home.csv.
The file has a TG column.
I want to divide all the values of that column by 10.
Write a Python code for that.
```

---

#### Exercise 7: Batch ZIP Files (Groups of 10)

```
I have 400 text files in the directory named 'text_files'.
Files are named like: tg_st_001.txt, tg_st_002.txt, ...
I want to place files 1-10 into one zip file, 11-20 into another, and so on.
Write me a Python script for that.
```

---

### 2.4 Streamlit Web Apps

> **Streamlit** — Python library to create browser-based web apps.  
> You can use it **without learning Streamlit** — just describe what you want to GPT!

**Install**: Tools → Manage Packages → `streamlit` → Install

**Run**: Cannot use the normal Run button. Go to:  
**Tools → Open System Shell**, then:
```bash
streamlit run p8.py
```

---

#### Exercise 8a: Temperature Histogram

```
I have a file called sherlock_home_modified.csv.
The file has a TG column which is a temperature column in degrees Celsius.
I want to create a histogram for that column.
Write me a script using Streamlit and Python.
```

---

#### Exercise 8b: Yearly Temperature Bar Chart

```
There is also a date column with observations in YYYYMMDD format.
I want to aggregate temperature by year and plot the yearly temperature.
I want a bar chart.
Write me a script using Streamlit and Python.
```

---

## 3. Lecture 2 — Advanced Prompting for NumPy/Pandas

### 3.1 Case Study 1: Categorical Encoding (Survey Data)

**Dataset**: Scalar's GenAI course launch survey  
**Columns**: Age group, Gender, Education level, Skills (ML/DL/NLP/Cloud etc.), GenAI familiarity, Impact ratings, ChatGPT API experience, Interest (1-5), Benefits, Course interest reasons.

**Challenge**: Many categorical columns need encoding before analysis.

---

#### Step-by-Step Workflow

**Step 1 — Persona + Data Snippet**
```
You are a professional data analyst with 20 years of experience in cutting-edge technology.

I have a data file called [filename.csv] with responses to a survey.
I need to find insights in it to create a better AI course.

Here is a chunk of that file:
[paste column names + first 2-3 rows of actual data]

After reading this, show me the list of all categorical variables from the dataset.
```

> **Critical**: Always paste a data sample. Without it, GPT gives generic, often wrong answers.

---

**Step 2 — Remove Irrelevant Columns**
```
Remove respondent_id, IP address, and 'other' free-text columns — they add no analytical value.
```

---

**Step 3 — Get Unique Values Per Column**
```
Create a Python script that will output all these variables with the list of their unique values,
in a format that I can easily copy-paste back here.
```
Run in Google Colab → copy output → paste back to GPT.

---

**Step 4 — Build Encoding Table**
```
With the above information, create a table with two columns:
- Column 1: Variable Name
- Column 2: Suggested Encoding Method
```

---

**Step 5 — Correct GPT's Mistakes** *(Most important step!)*
```
Update the input table with the following changes:
- Consider 'age' as ordinal column
- Consider 'gender' as nominal column
- Consider 'education_level' as ordinal column
- For 'prefer not to say' and 'others': assign a negative value (-1)
  because they should have the LOWEST weight, not the highest
```
> GPT will say sorry and fix it.

---

**Step 6 — Add Encoded Value Examples**
```
Add one more column to the input table with a pair of values:
- Old value (original category)
- New encoded value

Expected output format: [paste example from age/gender columns done earlier]
```

Example result:
| Variable | Encoding | Old -> New |
|----------|----------|-----------|
| age | Ordinal | 18-24->1, 25-35->2, 35-44->3 |
| gender | One-Hot | Male->0, Female->1, Non-binary->2 |

---

**Step 7 — Convert to JSON**
```
Convert the above table to JSON format, leaving out the encoding method column.
Output format example: [paste a small format example]
```
Create separate JSON files per group: `concat1.json`, `concat2.json`, etc.

---

**Step 8 — Merge JSON Files**
```
Write a Python script to merge the following JSON files:
- concat1.json, concat2.json, concat3.json
All files follow the same structure: [paste structure example]
Save the result into cat_encoding.json.
```

---

**Step 9 — Apply Encoding to CSV**
```
I need to encode categorical variables in my file.
Encoding schema is stored in cat_encoding.json.
Here is a chunk of that JSON: [paste sample]

Write a Python script that:
1. Opens the original CSV
2. For each variable in the JSON, adds a new column named original_column + '_enc'
3. Maps old values to new encoded values
4. Saves the result to a new CSV
5. Outputs the first 30 lines
```

---

**Step 10 — Reorder Columns**
```
Create a Python script that repositions columns so each _enc column
immediately follows its original column.
Example: age, age_enc, gender, gender_enc, ...

Rules:
- Not all columns have _enc counterparts — ignore those, keep as-is
- Do not duplicate any column
- Save the updated data in the same file
- Output the first 30 lines
```

---

### 3.2 Case Study 2: E-Commerce Churn Prediction

**Dataset**: `events.csv` — Electronics store event logs (5 months)

| Column | Description |
|--------|-------------|
| `event_time` | Timestamp of the event |
| `event_type` | view / cart / purchase / remove_from_cart |
| `product_id` | Product identifier |
| `user_id` | Customer identifier |
| `user_session` | Browser session key |

**Challenge**: No explicit churn column — must define and derive churn.

---

#### Churn Definition (GPT-suggested)

> **Definition**: A user is churned if they have **not made a purchase within the last 30 days** relative to the `max(event_time)` in the dataset.

```
I want to predict customer churn.
The dataset does NOT have an explicit churn column.
Given the data description and sample above, suggest how we should measure/define churn.
```

GPT reasoning: Uses max date as reference for statistical consistency (not each user's individual last date).

---

#### Detailed Prompt Structure

```
You are a professional data analyst with 20 years of experience.

I have a dataset events.csv. [describe source]

###
About the dataset:
[paste Kaggle/documentation description]

###
Column descriptions:
event_time: time of the event
event_type: view / cart / purchase / remove_from_cart
[describe each column]

###
First few lines:
[paste 3-5 rows of actual data]

###
I want to predict customer churn.
Let's first identify how we measure churn for this dataset.
```

> Use `###` as delimiters between sections.

---

#### Getting Full Code in One Block

When GPT gives code in separate fragments:
```
Update the code with the following:
- Give me the full code as one piece, not separate fragments
- The events.csv file is in my Google Drive — update accordingly
```

---

### 3.3 Descriptive Analysis Shortcut

**Step 1**: Ask GPT to write a `describe()` script → run in Google Colab.

**Step 2**: Paste output back:
```
Here is what I got as the output of the script:
[paste df.describe() output]

Which insights can you derive from this?
```

**Step 3**: Ask for more:
```
Any more insight?
```

GPT identifies: mean/median gaps (outliers), dominant categories, distribution shapes, extreme values.

---

### 3.4 Feature Engineering via GPT

#### Let GPT propose features
```
Let's do some feature engineering as the next step toward predicting churn.
Define which features may help us predict churn.
```

GPT suggests: Recency, Frequency, Cart abandonment rate, Unique products viewed, Average session duration, Category diversity, and 10+ more.

---

#### Evaluate features with probability & confidence
```
For each proposed feature, evaluate:
- Pros and cons
- Initial implementation effort (Low/Medium/High)
- Implementation difficulty
- Expected outcome
- Probability of success (%)
- Confidence interval
```

#### Filter to best features
```
Only keep features where confidence interval is high
or probability of success is above 70%.
```

---

### 3.5 Handling GPT's Memory Problem

> GPT has **short-term memory** (like Ghajini). In long conversations, it forgets earlier data.

**Memory-Refresh Prompt Pattern:**
```
Let me repeat the context because of memory limitations.

Dataset: [filename]
Description: [paste again]
Sample data: [paste again]
Previous step output we agreed on: [paste]

Next step: [your question]
```

---

## 4. Golden Rules & Best Practices

| # | Rule | Why |
|---|------|-----|
| 1 | **Be explicit about file/folder names** | GPT can't guess your directory structure |
| 2 | **Always paste a data sample** | 2-3 rows massively improves code accuracy |
| 3 | **Paste errors back to GPT** | "I am getting this error — rewrite the script" fixes 90% of issues |
| 4 | **Use delimiter `###`** | Separates context from questions clearly |
| 5 | **Give output format examples** | Few-shot format control prevents re-formatting work |
| 6 | **Verify every encoding decision** | GPT makes encoding type mistakes — use your analyst knowledge |
| 7 | **Ask GPT to explain its reasoning** | You learn AND you can correct mistakes |
| 8 | **Don't pay unnecessarily** | Free tier is sufficient for learning/personal use |
| 9 | **Request full code in one block** | "Give me the full code as one piece, not separate fragments" |
| 10 | **Refresh memory in long sessions** | Re-paste data and previous outputs when responses go off-track |

---

## 5. Where GPT Helps vs. Doesn't

### GPT Helps Here
- Take-home assignments
- Company projects & internal tools
- File automation (read/write/merge/zip)
- Boilerplate Python code
- Data analysis (encoding, feature engineering, descriptive stats)
- Presentation preparation (persona-based explanations)
- Email drafting, appraisals, resume optimization
- Using unfamiliar libraries (Streamlit, openpyxl) without learning them

### GPT Doesn't Help Here
- **Live coding interviews** — you must know the logic yourself
- **DSA rounds** — tests problem-solving thinking, not syntax
- **Companies that restrict AI tools** — many enterprises block ChatGPT
- **Production systems on free tier** — token limits break automated workflows
- **Security-sensitive data** — do not send confidential company data to OpenAI

---

## 6. Quick Reference: Prompt Templates

### General Format for Data Tasks
```
You are a professional data analyst with 20 years of experience in cutting-edge technology.

I have a data file called [filename].
[Brief description + business context]

Here is a chunk of that file:
[paste column headers + 2-3 rows]

[Your specific question or task]
```

---

### Error Fix Template
```
I am getting the below error:
---
[paste full error message]
---
Rewrite the Python script.
```

---

### Output Format Control
```
Your response should contain only the output table.
Use the same format as the example above: [paste example]
Do not add any extra explanation.
```

---

### Persona for Stakeholder Presentations
```
You are a [role] at a [industry] company that [does X].
Answer the question in your role's context: [question]
```

---

### ELI10 for Mixed Audiences
```
[Your topic]. Explain like to a 10-year-old.
```

---

### GPT Memory Refresh
```
Let me repeat the context because of memory limitations.

Dataset: [filename]
Description: [paste again]
Sample data: [paste again]
Previous output we agreed on: [paste]

Next step: [your question]
```

---

### Feature Evaluation
```
For each proposed feature, evaluate:
- Pros and cons
- Initial effort required (Low/Medium/High)
- Implementation difficulty
- Expected outcome
- Probability of success (%)
- Confidence interval (High/Medium/Low)
```

---

### Churn Definition Discovery
```
I want to predict customer churn.
The dataset does NOT have an explicit churn column.
Given the data description and sample above, suggest how we should define churn.
```

---

## Summary Cheat Sheet

```
Lecture 1 Key Points:
  |- Fill-in-blank: use "..." at end of sentence
  |- Constrained output: give Q->A example first (few-shot)
  |- Persona: "You are [X]" -> domain-specific explanations
  |- GPT asks you: "Ask me questions, then answer"
  |- ELI10: "Explain like to a 10-year-old"
  |- Free hack: rotate Gmail accounts when token limit hit
  |- Error fix: paste error -> "Rewrite the script"
  |- Streamlit: run via "streamlit run file.py" in system shell

Lecture 2 Key Points:
  |- Always paste data sample in prompts
  |- Use ### as delimiters in long prompts
  |- Encoding workflow: unique values -> table -> fix -> JSON -> apply
  |- GPT makes encoding mistakes -> YOU verify and correct
  |- Churn: GPT can define it when no churn column exists
  |- Feature engineering: GPT proposes, evaluates, filters
  |- Memory refresh: re-paste context + prior output
  |- Ask GPT to explain reasoning -> learn + correct
```

---

*Notes compiled from GenAI Practice Sessions — Lectures 1 & 2*  
*Keep practicing | Keep prompting | Keep learning*

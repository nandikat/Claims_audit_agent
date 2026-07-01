# Claims Audit Agent: Agentic AI for Payment Integrity

> **Overview**
> This repository contains a working proof-of-concept web application developed for a Cotiviti intern assessment. It demonstrates the strategic opportunity of utilizing Agentic AI to automate multi-step clinical decision-making in healthcare payment integrity.
> 
> 

This application uses a Large Language Model (LLM) to reason through claims data autonomously, generating an auditable trail of logic mirroring a human analyst's workflow.

---

## 🚀 Features

The application orchestrates a four-step agentic reasoning chain:

* **1. Contextualize:** Parses the claim fields (CPT, ICD-10, billed vs. allowed amount) to understand the service context.


* **2. Detect Anomalies:** Flags irregularities such as impossible service dates, excessive units, or mismatches between CPT and diagnostic codes.


* **3. Classify:** Categorizes the claim as **APPROVE**, **FLAG FOR REVIEW**, or **DENY**, complete with a clear justification.


* **4. Recommend:** Outputs a specific, actionable next step for the Cotiviti audit team (e.g., request medical records, auto-deny).



### Interactive UI

* **Live Audit Dashboard:** Select from a prepopulated list of synthetic claims (spanning clean, upcoded, and multi-flag fraud patterns) to see the AI agent reason through the 4 steps in real-time.


* **CSV Upload:** Upload a custom `.csv` of claims data to dynamically overwrite the active dataset and test the agent on novel claims.



---

## 🛠 Tech Stack

| Component | Technology | Description |
| --- | --- | --- |
| **Backend** | Python / Flask | Serves the web application and handles API routing.
<!-- | --- | --- | --- | -->
| **Frontend** | HTML / CSS / JS | Single-page interface built with vanilla web technologies for the agent dashboard.
| --- | --- | --- |
| **AI Integration** | Gemini API | Uses `gemini-2.5-flash` via the `google-genai` SDK to execute the reasoning chain.
<!-- | --- | --- | --- | -->
| **Data** | Pandas / CSV | Parses and filters the synthetic claims datasets.
| --- | --- | --- |


---

## ⚙️ Setup and Installation

**1. Clone the repository and navigate to the directory:**

```bash
git clone https://github.com/nandikat/Claims_audit_agent.git
cd claims-audit-agent

```

**2. Install the required Python dependencies:**
The backend relies on Flask, Pandas, Python-dotenv, and the Google GenAI SDK.

```bash
pip install flask pandas python-dotenv google-genai

```

**3. Configure your Environment Variables:**
You must provide a Gemini API key for the LLM orchestration to function. Create a `.env` file in the root directory and add the following:

```env
GEMINI_API_KEY=your_api_key

```

**4. Run the Application:**
Start the local development server.

```bash
flask --app main.py run

```

The application will be hosted at `[http://127.0.0.1:5000](http://127.0.0.1:5000)` by default.

---

## 📂 Project Structure

* `main.py`: The main Flask application that sets up the local server, handles CSV uploads, and constructs the API calls to the Gemini model.


* `templates/page1.html`: The frontend user interface containing the interactive table, claim details form, and the dynamic reasoning chain visualizer.


* `claims.csv`: The default synthetic dataset of claims containing clean, upcoded, and fraudulent examples (created dynamically if missing).

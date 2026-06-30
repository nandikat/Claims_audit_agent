import os
import json
import io
import pandas as pd
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types
import datetime
today_str = datetime.date.today().isoformat()
load_dotenv()

app    = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL  = "gemini-2.5-flash"


CLAIMS_PATH = os.path.join(os.path.dirname(__file__), "claims.csv")
if os.path.exists(CLAIMS_PATH):
    claims_df = pd.read_csv(CLAIMS_PATH)
else:
        claims_df = pd.DataFrame(columns=[
        "patient_id", "provider_name", "provider_npi", "cpt_code", "cpt_desc",
        "icd10_code", "icd10_desc", "billed_amount", "allowed_amount",
        "service_date", "place_of_service", "units", "expected_outcome"
    ])


@app.route("/")
def index():
    return render_template("page1.html")


@app.route("/claims")
def get_claims():
    """Return the active claims dataset (default or uploaded) as JSON."""
    global claims_df
    return jsonify(claims_df.to_dict(orient="records"))


@app.route("/upload", methods=["POST"])
def upload():
    """Accept a user-uploaded CSV, overwrite the active dataset, and return it."""
    global claims_df
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "File must be a .csv"}), 400

    try:
        df = pd.read_csv(io.StringIO(file.read().decode("utf-8")))
        required = [
            "patient_id", "provider_name", "provider_npi",
            "cpt_code", "cpt_desc", "icd10_code", "icd10_desc",
            "billed_amount", "allowed_amount", "service_date",
            "place_of_service", "units"
        ]
        missing = [c for c in required if c not in df.columns]
        if missing:
            return jsonify({"error": f"Missing columns: {', '.join(missing)}"}), 400

  
        if "expected_outcome" not in df.columns:
            df["expected_outcome"] = "UNKNOWN"

     
        claims_df = df

        return jsonify(claims_df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/audit", methods=["POST"])
def audit():
    claim = request.get_json()
    if not claim:
        return jsonify({"error": "No claim data received"}), 400

    prompt = f"""
You are a healthcare payment integrity analyst at .
Today's date is {today_str}. Do not flag service dates as being in the future unless they occur strictly after this date.
Analyze the following claim and reason through it in four steps.

CLAIM:
  Patient ID:        {claim.get("patient_id")}
  Provider:          {claim.get("provider_name")} (NPI: {claim.get("provider_npi")})
  CPT Code:          {claim.get("cpt_code")} — {claim.get("cpt_desc")}
  ICD-10 Code:       {claim.get("icd10_code")} — {claim.get("icd10_desc")}
  Service Date:      {claim.get("service_date")}
  Place of Service:  {claim.get("place_of_service")}
  Units Billed:      {claim.get("units")}
  Billed Amount:     ${claim.get("billed_amount")}
  Allowed Amount:    ${claim.get("allowed_amount")}

INSTRUCTIONS:
Respond with this exact JSON structure:
{{
  "step1": "Contextual summary: describe what this claim is for in 1-2 sentences. Identify the type of service, the clinical setting, and whether the procedure and diagnosis are a logical match.",
  "step2": "Anomaly detection: list every red flag you find — billing amount vs. allowed amount ratio, CPT-to-diagnosis mismatch, impossible dates, excessive units, upcoding suspicion, or provider pattern concerns. If none, say so explicitly.",
  "step3": "Classification: one of APPROVE, FLAG FOR REVIEW, or DENY. Follow with a one-sentence justification.",
  "step4": "Recommendation: a specific action for the  audit team — e.g. request medical records, schedule provider audit, auto-deny with reason code, or approve for payment."
}}
"""

    try:
     
        response = client.models.generate_content(
            model=MODEL, 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        
        result = json.loads(response.text.strip())
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
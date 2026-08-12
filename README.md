# Product Returnability Prediction System
Check it out now !!  https://clothing-returnability-issue.streamlit.app/
   
A Streamlit app that estimates the likelihood a product order will be returned, based on customer, product, and seller-side inputs. Built with Python, NumPy, and Matplotlib.

## What it does

You enter details about a customer, the product, and the transaction — age, location, category, brand, price, discount, rating, seller track record, delivery issues, and so on — and the app:

- Calculates a returnability score (0–100%) using a rule-based scoring model
- Classifies the risk as High / Moderate / Low and gives short, actionable insights for each band
- Plots how product rating alone affects returnability, holding other factors constant, to isolate its impact
- Breaks down which individual factors (discount, seller track record, malpractice, delivery issues) are pushing the return risk up or down

## How it works

The score isn't a trained ML model — it's a transparent scoring function so every point added or subtracted is traceable to a specific input.

**Base score by rating:**
- Rating ≤ 1 → starts at 95 (very likely to return)
- Rating 1–2 → interpolates down from 95
- Rating 2–3 → interpolates down from 80
- Rating > 3 → starts at a base of 50, then adjusted by every other factor below

**Adjustments applied on top of the base (for rating > 3):**

| Factor | Effect |
|---|---|
| Discount % | +0.15 per % (higher discount → slightly higher return risk) |
| Seller track record (0–10) | −1.5 per point (better sellers → lower risk) |
| Return reason = Defect / Quality Issue | +10 |
| Delivery issue present | +5 |
| Not a bestseller | +3 |
| Customer experience = Unhappy | +8 |
| Customer didn't really want the product | +10 |
| Seller malpractice reported | +7 |
| Product not "Fresh" condition | +5 |
| Price under ₹300 | +4 |
| Price over ₹5000 | −6 |
| Category in Shoes / Sweaters / Bags | +4 |
| Gender = Female | +2 |
| Location in Delhi / UP / Rajasthan | +3 |

A small random noise term (±3) is added to simulate real-world variance, and the final score is clamped between 3% and 98%.

## Tech stack

- Python
- Streamlit
- NumPy
- Matplotlib

## Running it locally

```bash
git clone https://github.com/<your-username>/product-returnability-predictor.git
cd product-returnability-predictor

pip install streamlit numpy matplotlib
streamlit run app.py
```

fill in the customer and product details, and click **Check Returnability**.

## Inputs

- **Customer**: age, gender, location/state
- **Product**: category, brand, price, discount %, rating, quantity purchased
- **Experience & seller factors**: return reason preference, bestseller status, delivery issue type, seller track record, customer satisfaction, purchase intent, quantity appropriateness, malpractice flag, pickup time, product condition, order day

## Outputs

- Returnability percentage with a risk band (High / Moderate / Low) and tailored recommendations
- A rating-vs-returnability curve showing how satisfaction alone shifts return probability
- A horizontal bar chart quantifying the impact of discount, seller track record, malpractice, and delivery issues on the score

## Limitations

- This is a rule-based heuristic, not a model trained on real return data — the weightings are illustrative, not statistically derived
- The random noise term means the same inputs can produce slightly different scores between runs
- Best used as a directional risk-screening tool, not a certified return-rate forecast

## Project structure

```
├── app.py
├── requirements.txt
└── README.md
```

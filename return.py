import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Returnability Predictor", layout="wide", page_icon="📦")
st.title("📦 Real-Time Professional Product Returnability Predictor")

st.markdown("""
Experience dynamic, intelligent prediction modeling — this tool recalculates product returnability with **every input change**, 
combining expert-defined rules with statistical adjustments.
""")

# -------------------- SECTIONS & INPUTS --------------------
st.divider()
st.header("👤 Customer & Product Information")

all_states = [
    "Maharashtra", "Delhi", "Karnataka", "Gujarat", "Uttar Pradesh", "Tamil Nadu",
    "Rajasthan", "Madhya Pradesh", "Kerala", "West Bengal"
]
all_categories = [
    "T-Shirts", "Jeans", "Shoes", "Bags", "Formal Wear", "Dresses",
    "Sweaters", "Trousers", "Jackets", "Accessories"
]
all_brands = [
    "Nike", "Adidas", "Puma", "Raymond", "Zara", "Levi's",
    "HM", "Pantaloons", "Allen Solly", "Louis Philippe"
]

c1, c2, c3 = st.columns(3)
age = c1.number_input("Customer Age", 15, 90, 30)
gender = c2.selectbox("Gender", ["Male", "Female"])
location = c3.selectbox("Customer Location or State", sorted(all_states))

c1, c2, c3 = st.columns(3)
category = c1.selectbox("Product Category", sorted(all_categories))
brand = c2.selectbox("Brand", sorted(all_brands))
price = c3.number_input("Product Price (₹)", 100.0, 100000.0, 1200.0)
discount = c1.slider("Discount (%)", 0, 90, 10)
rating = c2.slider("Product Rating (1 to 5)", 1.0, 5.0, 4.0)
quantity = c3.number_input("Quantity Purchased", 1, 999, 1)

st.divider()
st.header("🧠 Customer Experience & Seller Factors")

c1, c2, c3 = st.columns(3)
pref_criteria = c1.selectbox("Consumer Preferences Criteria", ["Size Issue", "Quality Issue", "Defect", "Availability"])
bestseller = c2.selectbox("Is it a Bestseller?", ["Yes", "No"])
delivery_issue = c3.selectbox("Delivery Related Issue", ["None", "Delay", "Wrong Address", "Damaged Product"])
track_record = c1.slider("Seller Track Record (0 - Poor, 10 - Excellent)", 0, 10, 8)
experience = c2.selectbox("Consumer Experience While Purchasing", ["Happy", "Neutral", "Unhappy"])
want_product = c3.selectbox("Did Consumer Really Want Product?", ["Yes", "No", "Uncertain"])
quantity_fit = c1.selectbox("Appropriate Quantity?", ["Too Low", "Appropriate", "Too Much"])
malpractice = c2.selectbox("Malpractice by Seller?", ["No", "Yes"])
pickup_time = c3.slider("Order Collection Time (in hours)", 1, 72, 24)
refurb_condition = c1.selectbox("Product Condition", ["Fresh", "Dry Wash", "Refurbished"])
order_day = c3.selectbox("Order Day", ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

# -------------------- PREDICTION FUNCTION --------------------
def calculate_dynamic_returnability(params):
    # Accurate rating segments with smooth interpolation
    if params['rating'] <= 1.0:
        score = 95
    elif params['rating'] <= 2.0:
        score = 95 - 15 * (params['rating'] - 1.0)
    elif params['rating'] <= 3.0:
        score = 80 - 15 * (params['rating'] - 2.0)
    else:
        score = 50
        # Multivariate influence for rating > 3
        score += (params['discount'] * 0.15) - (params['track'] * 1.5)
        if params['pref'] in ["Defect", "Quality Issue"]:
            score += 10
        if params['delivery'] != "None":
            score += 5
        if params['bestseller'] == "No":
            score += 3
        if params['experience'] == "Unhappy":
            score += 8
        if params['want'] == "No":
            score += 10
        if params['malpractice'] == "Yes":
            score += 7
        if params['refurb'] != "Fresh":
            score += 5
        if params['price'] < 300:
            score += 4
        if params['price'] > 5000:
            score -= 6
        if params['category'] in ["Shoes", "Sweaters", "Bags"]:
            score += 4
        if params['gender'] == "Female":
            score += 2
        if params['location'] in ["Delhi", "Uttar Pradesh", "Rajasthan"]:
            score += 3

    noise = random.uniform(-3, 3)
    final_score = min(max(int(score + noise), 3), 98)
    return final_score

# -------------------- MAIN INTERACTION --------------------
if st.button("Check Returnability"):
    parameters = {
        'rating': rating,
        'pref': pref_criteria,
        'delivery': delivery_issue,
        'bestseller': bestseller,
        'track': track_record,
        'experience': experience,
        'want': want_product,
        'malpractice': malpractice,
        'refurb': refurb_condition,
        'discount': discount,
        'price': price,
        'gender': gender,
        'location': location,
        'category': category
    }
    returnability_percent = calculate_dynamic_returnability(parameters)

    st.divider()
    st.subheader("📊 Returnability Prediction Result")
    st.success(f"Predicted Returnability Likelihood: **{returnability_percent}%**")

    st.markdown("### 🧩 Expert Insights")
    if returnability_percent >= 80:
        st.error("High Return Risk — optimize quality controls and improve trust level.")
        st.write("- Review logistics and customer feedback.")
        st.write("- High return linkage: excessive discounts or product mismatch.")
    elif 50 <= returnability_percent < 80:
        st.warning("Moderate Return Risk — monitor active buyers and post-sale feedback.")
        st.write("- Address minor delivery or satisfaction issues quickly.")
        st.write("- Audit your seller base regularly.")
    else:
        st.success("Low Return Risk — your product and customer alignment is healthy!")
        st.write("- Maintain strong service SLAs and brand perception.")
        st.write("- Encourage reviews to solidify trust metrics.")

# -------------------- VISUALIZATION SECTION --------------------
st.divider()
st.header("🌟 Rating vs Returnability Impact Visualization")

ratings = np.linspace(1, 5, 100)
returnabilities = []
for r in ratings:
    test_params = {
        'rating': r,
        'pref': 'Quality Issue',
        'delivery': 'None',
        'bestseller': 'Yes',
        'track': 8,
        'experience': 'Happy',
        'want': 'Yes',
        'malpractice': 'No',
        'refurb': 'Fresh',
        'discount': 10,
        'price': 1200,
        'gender': 'Male',
        'location': 'Maharashtra',
        'category': 'T-Shirts'
    }
    returnabilities.append(calculate_dynamic_returnability(test_params))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ratings, returnabilities, color='blue', linewidth=3, marker='o', markersize=4, label='Returnability %')

ax.set_title('Impact of Product Rating on Returnability Probability', fontsize=16, fontweight='bold')
ax.set_xlabel('Product Rating (1=Low, 5=High)', fontsize=14)
ax.set_ylabel('Returnability Percentage (%)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=12)

key_points = [1, 2, 3, 4, 5]
for kp in key_points:
    idx = (np.abs(ratings - kp)).argmin()
    y_val = returnabilities[idx]
    ax.annotate(f"{y_val:.0f}%", xy=(ratings[idx], y_val), xytext=(ratings[idx], y_val + 5),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3"), fontsize=12, color='navy')

st.pyplot(fig)
st.markdown("""
**Interpretation:**  
Returnability sharply decreases as product rating improves, indicating dissatisfied customers return products more often.
Critical for supply chain quality and policy decisions.
""")

st.header("🌟 Impact Scores for Selected Factors")
factors = ['Discount Effect', 'Track Record Effect', 'Malpractice Effect', 'Delivery Issue Effect']
scores = [
    0.15 * discount,
    -1.5 * track_record,
    7 if malpractice == "Yes" else 0,
    5 if delivery_issue != "None" else 0
]

fig2, ax2 = plt.subplots(figsize=(10, 4))
bars = ax2.barh(factors, scores, color=['skyblue', 'green', 'red', 'orange'])
ax2.set_title('Key Factors Impact on Returnability Score', fontsize=16, fontweight='bold')
ax2.set_xlabel('Impact Points (Positive increases return risk)', fontsize=14)
ax2.grid(axis='x', linestyle='--', alpha=0.4)

for bar in bars:
    width = bar.get_width()
    ax2.text(width + 0.15, bar.get_y() + bar.get_height()/2,
             f'{width:.2f}', va='center', fontsize=12)

st.pyplot(fig2)
st.markdown("""
**Insight:**  
Bar chart quantifies the positive/negative influence of significant factors affecting return risk, 
allowing for targeted operational improvements.
""")

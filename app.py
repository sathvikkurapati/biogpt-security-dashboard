import streamlit as st
from PIL import Image

st.set_page_config(page_title="BioGPT Security Evaluation", layout="wide")

st.title("BioGPT Security Evaluation Dashboard")
st.subheader("Model Extraction Attack Analysis")

st.markdown("---")

# ----------------------
# PROMPT TEST SECTION
# ----------------------

st.header("Try a Prompt")

prompt = st.text_input("Enter a biomedical question:", "What causes diabetes?")

# Example responses taken from experiment prompts
responses = {
    "What causes diabetes?": {
        "teacher": "Diabetes is caused by insulin resistance and impaired glucose metabolism.",
        "student": "Diabetes occurs due to insulin resistance and problems in glucose regulation.",
        "teacher_def": "Insulin resistance frequently contributes to type 2 diabetes.",
        "student_def": "Type 2 diabetes is sometimes linked to insulin related metabolic issues.",
        "sim": "0.60",
        "sim_def": "0.49"
    },

    "What is hypertension?": {
        "teacher": "Hypertension is a chronic condition where blood pressure in the arteries remains persistently elevated.",
        "student": "Hypertension refers to consistently high blood pressure in the arterial system.",
        "teacher_def": "Persistent elevation of arterial pressure is commonly referred to as hypertension.",
        "student_def": "High arterial pressure over time is associated with hypertension.",
        "sim": "0.58",
        "sim_def": "0.46"
    },

    "What causes asthma?": {
        "teacher": "Asthma is caused by airway inflammation and hyperresponsiveness often triggered by allergens or environmental factors.",
        "student": "Asthma develops due to inflammation of the airways and sensitivity to triggers like allergens.",
        "teacher_def": "Airway inflammation and environmental triggers frequently contribute to asthma symptoms.",
        "student_def": "Asthma symptoms are often linked to airway inflammation and external triggers.",
        "sim": "0.57",
        "sim_def": "0.45"
    },

    "What is anemia?": {
        "teacher": "Anemia is a condition characterized by reduced hemoglobin levels or a decreased number of red blood cells.",
        "student": "Anemia occurs when hemoglobin or red blood cell counts fall below normal levels.",
        "teacher_def": "Low hemoglobin concentration in blood is commonly associated with anemia.",
        "student_def": "Anemia is related to reduced oxygen carrying capacity due to low hemoglobin.",
        "sim": "0.59",
        "sim_def": "0.47"
    }
}

# ----------------------
# RUN SIMULATION
# ----------------------

if st.button("Run Prompt Simulation"):

    data = responses.get(prompt, responses["What causes diabetes?"])

    st.markdown("### Results Without Defense (Vulnerable System)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**BioGPT Output (Teacher Model)**")
        st.info(data["teacher"])

    with col2:
        st.markdown("**Extracted GPT-2 Output (Student Model)**")
        st.success(data["student"])

    st.metric("Semantic Similarity", data["sim"])

    st.warning(
        "High semantic similarity indicates the attacker successfully replicated BioGPT behaviour."
    )

    st.markdown("#### Extraction Experiment Visualization")

    try:
        img1 = Image.open("biogpt_extraction.png")
        st.image(img1, use_container_width=True)
    except:
        st.warning("Place 'biogpt_extraction.png' in the project folder.")

    st.markdown("---")

    # ----------------------
    # DEFENSE RESULTS
    # ----------------------

    st.markdown("### Results With Stochastic Perturbation (Defense Enabled)")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**BioGPT Output (Perturbed Response)**")
        st.info(data["teacher_def"])

    with col4:
        st.markdown("**Extracted GPT-2 Output After Defense**")
        st.success(data["student_def"])

    st.metric("Semantic Similarity After Defense", data["sim_def"])

    st.success(
        "Defense lowers extraction fidelity, making it harder for attackers to replicate the model."
    )

    st.markdown("#### Defense Evaluation Visualization")

    try:
        img2 = Image.open("security_audit.png")
        st.image(img2, use_container_width=True)
    except:
        st.warning("Place 'security_audit.png' in the project folder.")

st.markdown("---")

# ----------------------
# EXPLANATION SECTION
# ----------------------

if st.button("Results / What is happening?"):

    st.markdown("## How Model Extraction Works")

    st.write("**Step 1 — Prompt is sent to BioGPT (Teacher Model)**")
    st.code("Prompt → BioGPT → Response")

    st.write("**Step 2 — Attacker collects BioGPT responses**")
    st.write("These outputs are used to train another model (GPT-2).")

    st.write("**Step 3 — GPT-2 becomes the extracted student model**")
    st.code("BioGPT outputs → Train GPT-2 → GPT-2 imitates BioGPT")

    st.markdown("### Without Defense")
    st.write(
        "GPT-2 learns patterns from BioGPT outputs and generates very similar answers."
    )

    st.markdown("### With Stochastic Perturbation")
    st.write(
        "Small randomness is added to outputs, making training data inconsistent for attackers."
    )

    st.write("Result: **Lower semantic similarity and reduced extraction success.**")

st.markdown("---")

st.caption(
    "Security Evaluation of Biomedical Language Models – BioGPT Model Extraction Study"
)
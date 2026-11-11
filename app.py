import streamlit as st
from email_categorizer import categorize_email
from email_storage import save_email_history, load_email_history
from email_report import generate_email_report
from dashboard import show_email_dashboard

from config import APP_TITLE
from email_interface import (
    initialize_email_history,
    display_email_form
)
from email_ai import summarize_email
from email_classifier import classify_email
from reply_generator import generate_email_reply

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📧",
    layout="wide"
)

st.title("📧 AI Email Assistant")
st.write("Your intelligent assistant for understanding and responding to emails.")

# Initialize email history
if "email_history" not in st.session_state:
    st.session_state["email_history"] = load_email_history()

st.divider()

# Email input form
email_data = display_email_form(st)

# PROCESS A NEW EMAIL
if email_data:

    # STEP 1: AI EMAIL SUMMARIZATION
    with st.spinner("AI is summarizing your email..."):
        try:
            summary = summarize_email(email_data)
            email_data["summary"] = summary
            
            if "email_history" in st.session_state and st.session_state["email_history"]:
                st.session_state["email_history"][-1]["summary"] = summary

            st.success("Email summarized successfully!")
            st.subheader("🤖 AI Email Summary")
            st.write(summary)

        except Exception as error:
            st.error(f"Email summarization failed: {error}")

    # STEP 2: EMAIL CLASSIFICATION
    st.subheader("📊 Email Classification")
    try:
        classification = classify_email(email_data)
        email_data["classification"] = classification
        
        if "email_history" in st.session_state and st.session_state["email_history"]:
            st.session_state["email_history"][-1]["classification"] = classification

        col1, col2, col3 = st.columns(3)
        col1.metric("Email Intent", classification.get("intent", "Unknown"))
        col2.metric("Priority", classification.get("priority", "Unknown"))
        col3.metric(
            "Human Attention",
            "Required" if classification.get("human_attention_required") else "Not required"
        )

        st.write("**Classification Reason:**")
        st.write(classification.get("reason", "Not provided"))

    except Exception as error:
        st.error(f"Email classification failed: {error}")
    
    # STEP 3: EMAIL CATEGORIZATION
    st.subheader("📁 Email Category")

    try:
        with st.spinner("Categorizing your email..."):

            category_result = categorize_email(email_data)

            email_data["category"] = category_result
            st.session_state["email_history"][-1]["category"] = category_result

        st.success("Email categorized successfully!")

        st.metric(
            "Email Category",
            category_result.get("category", "Unknown")
        )

        st.write("**Category Reason:**")
        st.write(category_result.get("reason", "Not provided"))

    except Exception as error:
        st.error(f"Email categorization failed: {error}")

    # STEP 3: GENERATE SUGGESTED EMAIL REPLY
    tone = st.selectbox(
        "Choose Reply Tone",
        ["Professional", "Friendly", "Concise", "Apologetic"]
    )

    language = st.selectbox(
        "Choose Reply Language",
        ["English", "Hindi", "Gujarati", "French", "Spanish"]
    )
    
    st.subheader("✉️ Suggested Email Reply")

    try:
        with st.spinner("Generating a professional email reply..."):
            draft_reply = generate_email_reply(
                email_data=email_data,
                summary=email_data.get("summary"),
                classification=email_data.get("classification"),
                tone=tone,
                language=language
            )

            email_data["draft_reply"] = draft_reply
            if "email_history" in st.session_state and st.session_state["email_history"]:
                st.session_state["email_history"][-1]["draft_reply"] = draft_reply

        st.success("Suggested reply generated successfully!")

        history_len = len(st.session_state.get("email_history", [1]))
        st.text_area(
            "Review and edit the suggested reply:",
            value=draft_reply,
            height=250,
            key=f"draft_reply_{history_len}"
        )

    except Exception as error:
        st.error(f"Reply generation failed: {error}")

st.divider()

# EMAIL HISTORY
st.header("📂 Submitted Emails")

if st.session_state.get("email_history"):
    for index, email in enumerate(st.session_state["email_history"]):
        with st.expander(f"Email {index + 1}: {email.get('subject') or 'No subject'}"):
            st.write(f"**Sender:** {email.get('sender', 'Unknown')}")
            st.write(f"**Subject:** {email.get('subject', 'No subject')}")
            st.write("**Email Content:**")
            st.write(email.get("body", ""))

            if email.get("summary"):
                st.divider()
                st.write("**AI Summary:**")
                st.write(email["summary"])

            if email.get("classification"):
                st.divider()
                st.write("**Email Classification:**")
                st.json(email["classification"])
            
            if email.get("category"):
                st.divider()
                st.write("**Email Category:**")
                st.json(email["category"])

            if email.get("draft_reply"):
                st.divider()
                st.write("**Suggested Email Reply:**")
                st.write(email["draft_reply"])
else:
    st.info("No emails submitted yet.")

# SAVE EMAIL HISTORY
try:
    save_email_history(st.session_state["email_history"])
except Exception as error:
    st.error(f"Could not save email history: {error}")

# EXCEL EMAIL ANALYSIS REPORT

st.divider()

st.header("📊 Download Email Analysis Report")

email_history = st.session_state.get("email_history", [])

if email_history:

    try:
        excel_report = generate_email_report(email_history)

        st.download_button(
            label="📥 Download Excel Report",
            data=excel_report,
            file_name="email_analysis_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as error:
        st.error(f"Excel report generation failed: {error}")

else:
    st.info("Submit at least one email to generate an Excel report.")

# EMAIL ANALYTICS DASHBOARD

st.divider()

show_email_dashboard(
    st.session_state.get("email_history", [])
)

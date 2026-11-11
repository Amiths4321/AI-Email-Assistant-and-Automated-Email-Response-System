
import streamlit as st
import pandas as pd


def show_email_dashboard(email_history):

    st.header("📊 Email Assistant Dashboard")

    if not email_history:
        st.info("No email records available for the dashboard.")
        return

    total_emails = len(email_history)

    high_priority = sum(
        1 for email in email_history
        if email.get("classification", {}).get("priority", "").lower() == "high"
    )

    medium_priority = sum(
        1 for email in email_history
        if email.get("classification", {}).get("priority", "").lower() == "medium"
    )

    low_priority = sum(
        1 for email in email_history
        if email.get("classification", {}).get("priority", "").lower() == "low"
    )

    categorized_emails = sum(
        1 for email in email_history
        if email.get("category", {}).get("category")
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Emails", total_emails)
    col2.metric("High Priority", high_priority)
    col3.metric("Categorized Emails", categorized_emails)

    st.divider()

    st.subheader("📌 Priority Distribution")

    priority_data = pd.DataFrame({
        "Priority": ["High", "Medium", "Low"],
        "Emails": [
            high_priority,
            medium_priority,
            low_priority
        ]
    })

    st.bar_chart(
        priority_data.set_index("Priority")
    )

    st.subheader("📁 Email Category Distribution")

    categories = [
        email.get("category", {}).get("category", "Uncategorized")
        for email in email_history
    ]

    category_data = pd.Series(categories).value_counts()

    st.bar_chart(category_data)

    st.subheader("📋 Email Overview")

    overview = []

    for email in email_history:
        classification = email.get("classification", {})
        category = email.get("category", {})

        overview.append({
            "Sender": email.get("sender", ""),
            "Subject": email.get("subject", ""),
            "Priority": classification.get("priority", "Unknown"),
            "Category": category.get("category", "Uncategorized"),
            "Intent": classification.get("intent", "Unknown"),
            "Submitted At": email.get("submitted_at", "")
        })

    st.dataframe(
        pd.DataFrame(overview),
        use_container_width=True
    )

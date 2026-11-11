from email_storage import add_email_timestamp

def initialize_email_history(st):

    if "email_history" not in st.session_state:
        st.session_state["email_history"] = []


def display_email_form(st):

    st.header("📥 Email Input")

    sender = st.text_input(
        "Sender Email",
        placeholder="customer@example.com"
    )

    subject = st.text_input(
        "Email Subject",
        placeholder="Enter email subject"
    )

    email_body = st.text_area(
        "Email Content",
        height=250,
        placeholder="Paste the complete email here..."
    )

    submit = st.button(
        "Submit Email for Analysis",
        type="primary"
    )

    if submit:

        if not sender.strip() or not email_body.strip():
            st.warning(
                "Please enter the sender email and email content."
            )

        else:

            email_data = {
                "sender": sender.strip(),
                "subject": subject.strip(),
                "body": email_body.strip()
            }

            email_data = add_email_timestamp(email_data)

            st.session_state["email_history"].append(email_data)

            st.success("Email submitted successfully!")

            return email_data

    return None

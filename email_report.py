
import pandas as pd
from io import BytesIO


def generate_email_report(email_history):

    report_data = []

    for email in email_history:

        classification = email.get("classification", {})
        category = email.get("category", {})

        report_data.append({
            "Sender": email.get("sender", ""),
            "Subject": email.get("subject", ""),
            "Email Content": email.get("body", ""),
            "AI Summary": email.get("summary", ""),
            "Email Intent": classification.get("intent", ""),
            "Priority": classification.get("priority", ""),
            "Human Attention Required": classification.get(
                "human_attention_required", ""
            ),
            "Classification Reason": classification.get("reason", ""),
            "Email Category": category.get("category", ""),
            "Category Reason": category.get("reason", ""),
            "Suggested Reply": email.get("draft_reply", ""),
            "Submitted At": email.get("submitted_at", "")
        })

    df = pd.DataFrame(report_data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name="Email Analysis",
            index=False
        )

        worksheet = writer.sheets["Email Analysis"]

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        for column_cells in worksheet.columns:
            column_letter = column_cells[0].column_letter

            max_length = max(
                len(str(cell.value or ""))
                for cell in column_cells
            )

            worksheet.column_dimensions[column_letter].width = min(
                max(max_length + 2, 12),
                45
            )

    output.seek(0)

    return output.getvalue()

from fastapi import FastAPI, BackgroundTasks
import smtplib
from email.message import EmailMessage
app = FastAPI()
def send_email_background(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "rahul28june2024@gmail.com"
    msg["To"] = to_email
    msg.set_content(body)

    # Example: using Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("rahul28june2024@gmail.com", "xnjkkmlnjcfaagcq")
        smtp.send_message(msg)


@app.post("/send-email/")
async def send_email(to: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_email_background,
        to,
        "Welcome!",
        "Thanks for signing up."
    )
    return {"message": "Email is being sent in the background"}

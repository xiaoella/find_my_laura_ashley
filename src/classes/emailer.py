"""
Class object to write and send an email including images based on a local dataframe of listings.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Emailer:
    def __init__(self):
        self.from_email = os.environ.get("SENDER_EMAIL")
        self.password = os.environ.get("PASSWORD")
        self.to_email = os.environ.get("RECEIVER_EMAIL")

    def email_content(self, df):
        # Separate the df into two parts based on the prediction
        df_true = df[df["prediction"] == True]
        df_false = df[df["prediction"] == False]

        src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        with open(f"{src_dir}/email_content.html", "r") as file:
            html_content = file.read()
        
        email_body = """<div class="title">Weekly Laura Ashley Digest</div>"""
        # Add content if there are listings
        if not df_true.empty or not df_false.empty:
            if not df_true.empty:
                email_body += """
                <div class="subtitle">Here's what I've found from Etsy this past week:</div>
                """
                for index, row in df_true.iterrows():
                    email_body += f"""
                    <div class="listing">
                        <div class="title-text">{row['title']}</div>
                        <a href="{row['url']}">
                            <img src="cid:image{index}" alt="{row['title']}">
                        </a>
                    </div>
                    """
            if not df_false.empty:
                email_body += """
                <div class="subtitle">Here's what I've found that might be a Laura Ashley:</div>
                """
                for index, row in df_false.iterrows():
                    email_body += f"""
                    <div class="listing">
                        <div class="title-text">{row['title']}</div>
                        <a href="{row['url']}">
                            <img src="cid:image{index}" alt="{row['title']}">
                        </a>
                    </div>
                    """
            email_body += """
            <div class="closing">
                Happy shopping!<br>
                - Laura Ashley Fairy
            </div>
            """
        else:
            email_body += """
            <div class="closing">
                Nothing here this week, you get to save your money!<br>
                - Laura Ashley Fairy
            </div>
            """
        # Replace the placeholder in the HTML template with the generated content
        html_content = html_content.replace("{{ email_body }}", email_body)
        return html_content


    def send_email(self, subject, html_content, img_paths):
        message = MIMEMultipart("related")
        message["From"] = self.from_email
        message["To"] = self.to_email
        message["Subject"] = subject

        # Attach the HTML content
        message_html = MIMEText(html_content, "html")
        message.attach(message_html)

        # Attach images
        for i, path in enumerate(img_paths):
            with open(path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", f"<image{i}>")
                message.attach(img)

        try:
            with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as server:
                server.login(self.from_email, self.password)
                server.sendmail(self.from_email, self.to_email, message.as_string())
                print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
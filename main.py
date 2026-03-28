import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import smtplib
from email.mime.text import MIMEText
import time

headers = {"User-Agent": "Mozilla/5.0"}


url = "https://textilesgarmentsbusinessdirectory.com/asia/india/garment-exporters-in-india/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

companies = soup.find_all("h3")

data = []

for c in companies:
    name = c.text.strip()
    data.append({
        "name": name,
        "website": "",  
        "email": ""
    })

print(" Companies scraped:", len(data))


for i in range(len(data)):
    try:
        site = data[i]["website"]
        if site:
            r = requests.get(site, headers=headers, timeout=5)
            found = re.findall(r"[\w\.-]+@[\w\.-]+", r.text)

            if found:
                data[i]["email"] = found[0]

        time.sleep(1)
    except:
        pass

print(" Email extraction attempted")


df = pd.DataFrame(data)
df.to_excel("exporters.xlsx", index=False)

print(" Data saved to Excel")


EMAIL = "rt038639@gmail.com"
PASSWORD = "rutw xrdy qjgu mzmr"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)

for i in range(len(df)):
    name = df.loc[i, "name"]
    to_email = df.loc[i, "email"]

    if pd.isna(to_email) or to_email == "":
        continue

    body = f"""
    Hello {name},

    I hope you are doing well.

    I would like to explore business opportunities with your company.

    Looking forward to your response.

    Regards,  
    Roshan
    """

    msg = MIMEText(body)
    msg["Subject"] = "Business Proposal"
    msg["From"] = EMAIL
    msg["To"] = to_email

    server.sendmail(EMAIL, to_email, msg.as_string())

    print(f" Sent to {name}")
    time.sleep(2)

server.quit()

print(" All emails sent successfully!")
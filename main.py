# main.py
from openai import OpenAI
import boto3
import os
from datetime import datetime

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
s3 = boto3.client("s3")

BUCKET_NAME = os.getenv("S3_BUCKET")

def generate_text():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Write a short paragraph about AI in education"}
        ]
    )
    return response.choices[0].message.content


def save_and_upload(text):
    filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Save locally
    with open(filename, "w") as f:
        f.write(text)

    # Upload to S3
    s3.upload_file(filename, BUCKET_NAME, filename)

    print(f"Uploaded {filename} to S3 bucket {BUCKET_NAME}")


text = generate_text()
save_and_upload(text)
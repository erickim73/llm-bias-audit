import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
    ]
)

print(message.content[0].text)
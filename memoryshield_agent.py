import os
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

# Load API keys from .env
load_dotenv()

# Get API keys
groq_api_key = os.getenv("GROQ_API_KEY")
hindsight_api_key = os.getenv("HINDSIGHT_API_KEY")

# Create Groq client
groq_client = Groq(api_key=groq_api_key)

# Create Hindsight client
hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=hindsight_api_key
)

# Our Hindsight memory bank
bank_id = "memoryshield"

print("MemoryShield AI is ready!")

def get_customer_response(customer_name, customer_message):

    # 1. Recall previous memories about this customer
    result = hindsight_client.recall(
        bank_id=bank_id,
        query=f"What do we know about customer {customer_name}?"
    )

    previous_memories = "\n".join(
        memory.text for memory in result.results
    )
    
    print("\n🧠 Memory Used:")
if previous_memories:
    print(previous_memories)
else:
    print("No previous customer memory found.")
    

    # 2. Give the previous memories + new message to the AI
    prompt = f"""
You are MemoryShield, an intelligent customer support agent.

Customer name: {customer_name}

Previous customer memories:
{previous_memories}

Current customer message:
{customer_message}

Use the previous memories when they are relevant.
Give a helpful, friendly and personalized support response.
Do not mention that you are reading a memory database.
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    ai_response = response.choices[0].message.content

    # 3. Store the new interaction in Hindsight
    hindsight_client.retain(
        bank_id=bank_id,
        content=(
            f"Customer {customer_name} said: {customer_message}. "
            f"MemoryShield responded: {ai_response}"
        )
    )

    return ai_response

# Test MemoryShield
customer_name = "Ravi"

customer_message = input("Customer: ")

answer = get_customer_response(
    customer_name,
    customer_message
)

print("\nMemoryShield:", answer)


import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

# Load API keys
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
hindsight_api_key = os.getenv("HINDSIGHT_API_KEY")

# Create AI client
groq_client = Groq(api_key=groq_api_key)

# Create Hindsight memory client
hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=hindsight_api_key
)

bank_id = "memoryshield"


# --------------------------------
# HINDSIGHT MEMORY FUNCTION
# --------------------------------

async def get_memories(customer_name):

    result = await hindsight_client.arecall(
        bank_id=bank_id,
        query=f"Previous customer support interactions for customer named {customer_name}"
    )

    # Keep only memories belonging to this customer
    used_memories = [
        memory
        for memory in result.results
        if customer_name.lower() in memory.text.lower()
    ][:3]

    return used_memories


async def save_memory(customer_name, customer_message, ai_response):

    await hindsight_client.aretain(
        bank_id=bank_id,
        content=(
            f"Customer {customer_name} said: {customer_message}. "
            f"MemoryShield responded: {ai_response}"
        )
    )


# --------------------------------
# AI SUPPORT FUNCTION
# --------------------------------

async def get_customer_response(customer_name, customer_message):

    # Recall customer memories
    used_memories = await get_memories(customer_name)

    previous_memories = "\n".join(
        memory.text for memory in used_memories
    )

    if not previous_memories:
        previous_memories = "No previous memories found for this customer."

    # AI prompt
    prompt = f"""
You are MemoryShield, an intelligent customer support agent.

Customer name: {customer_name}

IMPORTANT:
Address the customer using exactly this name: {customer_name}.
Do not shorten, change, or replace the customer's name.

Previous customer memories:
{previous_memories}

Current customer message:
{customer_message}

Use previous memories only when they belong to this exact customer.

Give a short, friendly and helpful support response.
Keep the response under 100 words.

If a previous action did not solve the problem,
do not blindly repeat that same action.
Suggest the next useful step.

Do not mention the memory database.
"""

    # Generate AI response
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

    # Store interaction in Hindsight
    await save_memory(
        customer_name,
        customer_message,
        ai_response
    )

    return ai_response, used_memories


# --------------------------------
# MEMORYSHIELD WEB APP
# --------------------------------

st.set_page_config(
    page_title="MemoryShield AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ MemoryShield AI")

st.caption("Intelligent Customer Support That Remembers")

st.write(
    "MemoryShield remembers previous customer interactions "
    "and uses them to provide personalized support."
)

st.divider()


# Customer information

customer_name = st.text_input(
    "👤 Customer Name",
    value="Ravi"
)

customer_message = st.text_area(
    "💬 Tell us your problem",
    placeholder="Example: My Wi-Fi is still disconnecting..."
)


if st.button("🤖 Ask MemoryShield", use_container_width=True):

    if customer_message.strip():

        with st.spinner("MemoryShield is checking your history..."):

            answer, memories = asyncio.run(
                get_customer_response(
                    customer_name,
                    customer_message
                )
            )

        st.success("MemoryShield has responded!")

        st.subheader("🤖 Personalized Support")

        st.write(answer)

        st.divider()

        st.subheader("🧠 Memory Used")

        if memories:

            st.caption(
                "MemoryShield used these previous interactions "
                "to personalize the response:"
            )

            for memory in memories:
                st.info(memory.text)

        else:

            st.info(
                "No previous customer memory found. "
                "This interaction will be remembered for next time."
            )

    else:

        st.warning("Please enter your problem first.")
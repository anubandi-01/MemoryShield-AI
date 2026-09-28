# 🛡️ MemoryShield AI

### Intelligent Customer Support That Remembers

MemoryShield AI is an intelligent customer support agent that uses persistent memory to remember previous customer interactions and provide more personalized support over time.

## 🚀 Problem

Traditional customer support systems often treat every conversation as a new conversation.

This can lead to:

- Repeated troubleshooting steps
- Customers having to explain the same problem again
- Generic responses
- Poor continuity between support interactions

## 💡 Solution

MemoryShield AI gives the support agent persistent memory.

It can:

- Remember previous customer problems
- Recall previous troubleshooting attempts
- Avoid repeating unsuccessful solutions
- Learn additional customer context
- Provide more personalized responses over multiple interactions

## 🧠 How Memory Works

MemoryShield uses **Hindsight** as its persistent memory system.

The workflow is:

Customer  
↓  
MemoryShield AI  
↓  
Recall relevant customer history from Hindsight  
↓  
Generate personalized response using Groq LLM  
↓  
Store the new interaction in Hindsight  
↓  
Improve future responses

## 🛠️ Technology Stack

- Python
- Streamlit
- Groq LLM
- Hindsight Memory
- Python-dotenv
- GitHub

## 🎯 Demo Scenario

A customer named Ananya experiences repeated Wi-Fi disconnections.

### Interaction 1

Ananya reports that her Wi-Fi disconnects every evening.

MemoryShield provides initial troubleshooting and stores the interaction.

### Interaction 2

Ananya reports that the problem happened again and that restarting the router did not help.

MemoryShield recalls the previous interaction and avoids blindly repeating the same troubleshooting step.

### Interaction 3

Ananya explains that the problem happens around 7 PM during online classes and mainly affects her laptop.

MemoryShield recalls the previous context and provides more specific troubleshooting suggestions.

This demonstrates how the agent becomes more personalized through repeated interactions.

## ⭐ Key Features

### Persistent Memory
Stores customer interactions using Hindsight.

### Customer-Specific Recall
Retrieves memories relevant to the current customer.

### Personalized Support
Uses previous interactions to improve responses.

### Learning Over Time
The agent becomes more context-aware as more interactions are stored.

### Memory Visibility
The interface shows the previous memories used to generate the response.

## 🏗️ Architecture

```text
             Customer
                 │
                 ▼
        Streamlit Web App
                 │
                 ▼
       MemoryShield AI Agent
            /          \
           /            \
          ▼              ▼
   Hindsight Memory    Groq LLM
          │              │
          └──────┬───────┘
                 │
                 ▼
       Personalized Response
                 │
                 ▼
       Store New Interaction
                 │
                 ▼
        Hindsight Memory
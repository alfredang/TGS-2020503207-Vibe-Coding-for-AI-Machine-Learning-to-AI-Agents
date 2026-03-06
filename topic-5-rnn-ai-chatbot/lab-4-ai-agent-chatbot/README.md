# Lab 4: AI Agent Chatbot


## Open in Google Colab

**Standard (no Gradio):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-4-ai-agent-chatbot/lab-4-ai-agent-chatbot.ipynb)


**With Gradio UI:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alfredang/TGS-2020503207-Vibe-Coding-for-AI-Machine-Learning-to-AI-Agents/blob/main/topic-5-rnn-ai-chatbot/lab-4-ai-agent-chatbot/lab-4-ai-agent-chatbot-gradio.ipynb)

## Overview

This lab brings together deep learning and software engineering to build an AI Agent Chatbot. The agent follows a perceive-reason-act architecture, using a trained sentiment analysis model as one of its tools alongside other utility functions.

## Learning Objectives

- Understand the AI Agent architecture: perceive, reason, act
- Build a tool registry that maps command names to callable functions
- Integrate a trained Keras sentiment model as an agent tool
- Implement an agent loop that parses input, selects tools, and formats responses
- Add conversation memory for multi-turn interactions
- Handle errors gracefully with fallback responses

## Agent Architecture

```
User Input
    -> Perceive (parse and understand the input)
    -> Reason (decide which tool to use)
    -> Act (execute the tool and format the response)
    -> Return to user
```

## Tools

| Tool | Description |
|------|-------------|
| `analyze_sentiment(text)` | Uses the trained Keras LSTM model to classify text as positive/negative with confidence |
| `get_help()` | Returns a list of available commands and their descriptions |
| `summarize_conversation()` | Summarizes the conversation history so far |

## Key Concepts

| Concept | Description |
|---------|-------------|
| AI Agent | A system that perceives its environment, reasons about actions, and acts autonomously |
| Tool Registry | A dictionary mapping tool names to their callable functions |
| Conversation Memory | A list of past exchanges that gives the agent context |
| Fallback Handling | Graceful responses when the agent cannot understand the input |

## Requirements

- Python 3.13+
- Keras 3 (PyTorch backend)
- Gradio

## How to Run

1. Open `lab-4-ai-agent-chatbot.ipynb` in Jupyter or Google Colab.
2. Run all cells sequentially. The notebook trains a quick sentiment model if a saved model is not found.
3. The final section launches a Gradio ChatInterface for conversational interaction with the agent.

## Example Interactions

```
User: analyze "This movie was absolutely fantastic!"
Agent: Sentiment: POSITIVE (confidence: 94.2%)

User: help
Agent: Available commands: analyze, help, summarize

User: summarize
Agent: Here is a summary of our conversation so far...
```

## References

- [Building AI Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Gradio ChatInterface](https://www.gradio.app/docs/chatinterface)

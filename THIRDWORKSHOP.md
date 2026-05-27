# Workshop 3: Chutes and Agents - Creating Self-Orchestrating Agents

**Event:** AI Marathon 2026  
**Date:** 21 May 2026  
**Host:** Chutes.AI  
**Mode:** Physical  
**Venue:** S-08-02  
**Topic:** Effective agents, Hermes setup, multi-model routing, and Chutes-powered inference

> These are cleaned workshop notes derived from the raw transcript. They are intended as a readable study and reference document, not a verbatim transcript.

## Session Overview

This workshop focused on building effective AI agents. The speaker, Vince from Chutes.AI, explained the difference between a chatbot and an agent, introduced the mindset needed to design useful agentic systems, and walked participants through setting up a Hermes agent with Chutes as a custom inference provider.

The workshop combined conceptual design principles with a practical hands-on setup.

## Key Takeaways

- A chatbot mainly responds. An agent can inspect context, use tools, update work, and adapt based on results.
- An agent is a system, not just a model.
- Strong agents need a clear workflow, useful tools, memory, context, and reliable inference.
- Good agent design starts with the user's problem, not with model selection.
- Chutes can power agents with private, lower-cost, multi-model inference.
- Hermes can be configured to use Chutes through a custom OpenAI-compatible endpoint.
- API keys should be stored securely in environment files, not hard-coded.

## Chatbots vs Agents

Traditional chatbot interaction is usually a back-and-forth conversation:

- The user asks a question.
- The model gives an answer.
- The user copies, edits, or acts manually.

An agent goes further. It becomes useful when it can:

- Inspect context.
- Decide what information matters.
- Use external tools.
- Take actions.
- Observe results.
- Adjust its next step.
- Keep a useful memory of past instructions or preferences.

In short, chatbots talk; agents work through a process.

## Agent Building Blocks

| Component | Purpose |
| --- | --- |
| Brain | The model or reasoning layer that decides what to do. |
| Memory | Stores useful context, preferences, and past lessons. |
| Tools | Give the agent ways to act, such as reading files, calling APIs, searching, or using apps. |
| Workflow | Defines what the agent is trying to accomplish and how it should move from input to output. |
| Runtime | The orchestration layer that runs the agent and coordinates tools, memory, and model calls. |
| Inference | The model execution layer that powers the agent's reasoning and responses. |
| Trust Layer | Privacy, security, auditability, and control mechanisms. |

The speaker emphasized that the workflow is what turns model output into a useful system.

## Agent Design Mindset

A good agent is a workflow with judgment.

Before building, define:

- Who the agent is for.
- What problem wastes the user's time.
- What input starts the workflow.
- What context the agent needs.
- What tools the agent can use.
- What output the user expects.
- Where a human should approve or review the result.

This keeps the agent focused on usefulness instead of novelty.

## Example Agent: Scout

The workshop used **Scout** as an example agent concept.

### User

A student who is overwhelmed by tabs, PDFs, notes, research papers, links, and deadlines.

### Problem

The student has too much information and needs help turning scattered material into a trusted brief, summary, or action plan.

### Trigger

The user provides:

- A question or research goal.
- A set of links.
- Notes.
- PDFs or documents.
- Any relevant project context.

### Agent Workflow

Scout should:

1. Read and organize the provided material.
2. Identify the most relevant information.
3. Summarize the key points.
4. Highlight uncertainty or missing context.
5. Suggest next steps.
6. Produce a brief the student can trust and act on.

The example shows that an agent does not need to do everything. It should do one useful workflow well.

## Design Principles

### Context First

Agents perform better when they receive clear and complete context. The context tells the agent what matters and prevents it from guessing.

### Tools Over Cleverness

Tools give agents reliable ways to act. Instead of relying only on clever prompting, use tools for repeatable actions such as file reading, search, data extraction, and API calls.

### Keep Humans in the Loop

Agents should not approve sensitive actions on their own. The user should remain the final director for important decisions.

### Route by Task

Not every task needs the largest model. Use smaller or cheaper models for simple steps and stronger models for deeper reasoning, coding, or research.

### Make the Loop Visible

Good agents should expose enough of their process for users to understand what happened, especially when the workflow involves business, academic, financial, or personal data.

## Why Chutes Matters for Agents

Agents can make many model calls while reading, planning, using tools, and checking results. This can become expensive or privacy-sensitive when using centralized providers.

Chutes was presented as a useful inference layer because it supports:

- Lower-cost model access.
- Open-source model options.
- Trusted Execution Environments.
- End-to-end encrypted inference.
- Multi-model routing.
- OpenAI-compatible integration.

This combination makes Chutes suitable for long-running or sensitive agentic workflows.

## Hands-on Setup: Hermes With Chutes

The hands-on portion walked participants through setting up Hermes and configuring Chutes as a custom provider.

### Prerequisites

- A machine ready for local development.
- Access to the workshop GitHub repository.
- A Chutes account or provided workshop API key.
- Basic command-line familiarity.
- Windows users could follow the Windows native install guide in the repository.

### Setup Flow

1. Clone or open the workshop repository.
2. Open the documentation folder.
3. Follow the Windows native install guide if using Windows.
4. Install Hermes using the command provided in the guide.
5. During Hermes setup, choose the quick setup path.
6. When selecting the provider, choose **Custom Endpoint**.
7. Use the Chutes OpenAI-compatible base URL:

   ```text
   https://llm.chutes.ai/v1
   ```

8. Paste the Chutes API key when prompted. The input may appear invisible because it is treated as a secret.
9. Select **Chat Completions** when asked for the endpoint type.
10. Choose a model ID from the Chutes model catalog.
11. Set a context length if needed, or leave it blank for the default.
12. Choose a terminal backend. Local mode was used in the workshop because not everyone had Docker installed.
13. Configure Telegram or Discord integration later if not needed immediately.
14. Run the update or verification command:

   ```powershell
   hermes update
   ```

15. Start Hermes:

   ```powershell
   hermes
   ```

## Configuration Notes

- Store API keys in environment files.
- Do not hard-code API keys in source code.
- Use the Chutes model endpoint or model catalog as the source of truth for available models.
- Model availability can change, so avoid assuming one model will always be present.
- Multi-model setups let agents use different models for different tasks.

## Troubleshooting

The workshop mentioned `hermes doctor` as a useful command when Hermes is not working correctly.

```powershell
hermes doctor
```

Common issues to check:

- API key is missing or invalid.
- Base URL is incorrect.
- Wrong endpoint type was selected.
- Model ID does not exist or is unavailable.
- Environment file is not loaded.
- Terminal backend was configured incorrectly.

## Hackathon Relevance

For AI Marathon teams, this workshop is useful because many problem statements require agentic behaviour:

- Reading documents.
- Extracting structured information.
- Using tools or APIs.
- Making multi-step decisions.
- Producing explainable outputs.
- Handling private or sensitive data.

Teams should design their solution as a workflow, then decide which tools and models the agent needs.

## Action Items for Participants

- Finish installing Hermes.
- Configure Chutes as a custom inference provider.
- Test at least one model call.
- Try a small Scout-style workflow with links, notes, or documents.
- Decide whether your hackathon agent needs multiple models.
- Keep API keys out of source control.
- Prepare a clear agent architecture diagram for your pitch deck.

## Useful Terms

| Term | Meaning |
| --- | --- |
| Agent | AI system that can inspect context, use tools, and take steps toward a goal. |
| Hermes | Agent runtime used in the workshop hands-on setup. |
| Runtime | System that coordinates the agent's model calls, tools, memory, and workflow. |
| Tool | External capability the agent can use, such as file access, search, APIs, or messaging. |
| Multi-model routing | Sending different tasks to different models based on cost, speed, or capability. |
| Chutes | Inference provider used to power the agent. |
| TEE | Trusted Execution Environment for protected computation. |
| End-to-end encryption | Encryption where data is protected before it leaves the user and only decrypted in a trusted environment. |

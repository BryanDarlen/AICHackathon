# Workshop 2: Introducing Chutes, Bittensor, and How to Build on Chutes

**Event:** AI Marathon 2026  
**Date:** 20 May 2026  
**Host:** Chutes.AI  
**Mode:** Hybrid  
**Topic:** Open-source inference, Bittensor, Chutes, privacy, and hackathon use cases

> These are cleaned workshop notes derived from the raw transcript. They are intended as a readable study and reference document, not a verbatim transcript.

## Session Overview

This workshop introduced Chutes.AI as an open-source, decentralized inference platform built on Bittensor. The session focused on why centralized AI infrastructure can be costly, concentrated, and privacy-sensitive, then explained how Chutes uses distributed GPU providers, validators, and privacy technologies to offer a different model for AI inference.

The speaker, Fez / Burhan, framed the session around three questions:

- Why is centralized AI structurally difficult to sustain?
- Where is the AI market moving?
- How can builders use Chutes in real workflows and hackathon projects?

## Key Takeaways

- Centralized AI depends heavily on a small number of large companies with very high infrastructure spending.
- Many users consume AI for free or at prices that may not reflect the full cost of inference.
- Open-source models and decentralized compute networks can reduce the need for one company to own the whole AI stack.
- Chutes runs as Bittensor subnet 64 and coordinates miners, validators, and subnet operators.
- Chutes provides OpenAI-compatible APIs, making it easier to connect existing tools and applications.
- Privacy is a major product focus, especially through Trusted Execution Environments (TEE) and end-to-end encrypted inference.
- Hackathon teams can use Chutes to build low-cost, privacy-aware, agentic AI applications.

## The Problem With Centralized AI

The workshop described three major issues with centralized AI.

### 1. Infrastructure Cost

Frontier AI requires large capital expenditure on GPUs, data centers, energy, and operations. The speaker argued that the current centralized AI economy depends on very high spending by a small number of companies.

### 2. Concentration of Control

If most builders rely on only a few providers, those providers control:

- Model catalogs.
- API pricing.
- Access rules.
- Data policies.
- Deprecation timelines.
- Safety and moderation behaviour.

This creates platform risk for developers and startups.

### 3. Privacy as a Promise

Centralized AI providers often ask users to trust that prompts, documents, and outputs will be handled properly. The workshop argued that privacy should be built into the architecture, not treated only as a policy promise.

## Where AI Is Moving

The speaker highlighted open-source models as an important shift in the AI market. Efficient open models can provide strong capability at much lower cost than many closed frontier systems.

This shift makes it possible for builders to:

- Run or route to open-source models.
- Use cheaper inference for long-running workflows.
- Avoid complete dependency on closed model providers.
- Build products around privacy, openness, and lower operational cost.

## What Is Bittensor?

Bittensor is a blockchain-based network made up of multiple subnets. Each subnet focuses on a specific AI or compute task.

Chutes was described as **Bittensor subnet 64**, focused on inference.

### Roles in the Chutes Subnet

| Role | Responsibility |
| --- | --- |
| Miners | Provide GPU compute and host models. |
| Validators | Score miners on speed, reliability, capacity, quality, and accuracy. |
| Subnet Owners / Operators | Manage the product layer, billing, user experience, support, and network incentives. |

The network uses incentives so that miners are rewarded for providing useful, reliable compute.

## How a Chutes Request Works

At a high level:

1. A developer or application sends a request to Chutes.
2. The platform routes the request to suitable miners.
3. Validators continuously score miners.
4. A miner serves the model response.
5. The platform returns the result through an OpenAI-compatible interface.

This design lets Chutes use distributed compute while still giving developers a familiar API surface.

## Chutes Privacy Architecture

Privacy was one of the main themes of the workshop.

### Trusted Execution Environments

The speaker described TEE as Chutes' default privacy layer. TEE protects prompts and model execution by running sensitive computation inside hardware-protected environments.

Technologies mentioned:

- NVIDIA Confidential Computing for protected GPU execution.
- Intel TDX for protected memory and trust domains.
- Hardware attestation so users can verify the running environment.

### End-to-End Encrypted Inference

For more sensitive workflows, Chutes also supports end-to-end encrypted inference. In this model, prompts are encrypted on the user's machine, travel as ciphertext, and decrypt only inside the protected execution environment.

This is especially relevant for:

- Medical notes.
- Legal documents.
- Financial data.
- Internal company knowledge.
- Private personal assistants.

## Developer Integrations

The workshop mentioned several ways developers can use Chutes:

- OpenAI-compatible API endpoints.
- Chutes Chat for multimodal chat.
- AI search and sharing products.
- Sign in with Chutes for user-managed AI credits.
- n8n nodes for automation workflows.
- Integrations with coding and agent tools.
- OpenRouter routing for open-source model access.
- GitHub repositories and open-source tooling.

## Sign in With Chutes

Sign in with Chutes was presented as a useful pattern for hackathon teams and product builders.

Instead of the app developer paying all inference costs, users can sign in with their own Chutes account and authorize the application to use their Chutes credits. This helps teams avoid unexpected inference bills while still offering AI-powered features.

This is useful when:

- A team has little or no inference budget.
- A product may suddenly gain many users.
- The builder wants user-owned usage and billing.
- The app's value is in the workflow, not in subsidizing model calls.

## Hackathon Ideas

Teams were encouraged to build projects that fit Chutes' strengths.

Strong directions include:

- Privacy-first applications where prompts must stay confidential.
- Medical, legal, financial, or HR workflows that need protected inference.
- Agentic workflows that require many model calls.
- Apps using Sign in with Chutes so users bring their own credits.
- Multilingual SEO or Southeast Asian content workflows.
- Mobile interfaces for Chutes-powered products.
- Open-source AI toolkits for students.

## Quiz Recap

The workshop included quiz questions around:

- Estimated AI infrastructure spending by large hyperscalers.
- The share of ChatGPT users who use the free tier.
- AI data center electricity consumption.
- Why centralized AI can create concentration risk.
- Why TEE and end-to-end encryption matter.
- Which Chutes feature fits sensitive medical-note summarization.
- How teams with zero inference budget can use Sign in with Chutes.

## Getting Started

The workshop pointed participants toward:

- The Chutes app for account creation and API keys.
- Chutes documentation for API references, model catalog, and end-to-end encryption setup.
- Chutes GitHub repositories for open-source implementation details.
- The AI Marathon website and event channels for hackathon-specific support.

When building, teams should keep secrets such as API keys in environment variables and avoid committing them into repositories.

## Action Items for Participants

- Create or confirm access to a Chutes account.
- Generate an API key.
- Review the model catalog and pricing.
- Decide whether your project needs TEE or end-to-end encrypted inference.
- Consider Sign in with Chutes if your team has limited inference budget.
- Design the agent workflow before writing code.

## Useful Terms

| Term | Meaning |
| --- | --- |
| Chutes | Decentralized inference platform built on Bittensor subnet 64. |
| Bittensor | Blockchain-based network made of specialized AI subnets. |
| Subnet | A specialized network inside Bittensor focused on a particular task. |
| Miner | Participant that provides GPU compute. |
| Validator | Participant that scores miner performance and quality. |
| TEE | Trusted Execution Environment; hardware-backed protection for sensitive computation. |
| End-to-end encrypted inference | Inference where prompts are encrypted before leaving the user and decrypt only inside a protected runtime. |
| OpenAI-compatible API | API style compatible with common OpenAI request patterns. |

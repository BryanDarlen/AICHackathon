# Workshop 1: What Is DeAI and Why Should You Care?

**Event:** AI Marathon 2026  
**Date:** 18 May 2026  
**Host:** Morpheus and APU DeAI Club  
**Mode:** Physical  
**Venue:** S-08-02  
**Topic:** Decentralized AI, Morpheus, sustainable inference, and agentic use cases

> These are cleaned workshop notes derived from the raw transcript. They are intended as a readable study and reference document, not a verbatim transcript.

## Session Overview

This workshop introduced decentralized AI (DeAI) through the Morpheus ecosystem. The main message was that builders should understand the tradeoffs of centralized AI providers and consider more sustainable, privacy-conscious, and community-driven infrastructure for hackathon projects.

The speakers used examples such as AI-generated web animations, decentralized inference, OpenAI-compatible APIs, staking-based access, and autonomous agents to show how DeAI can support practical applications without depending entirely on centralized platforms or temporary free credits.

## Key Takeaways

- Decentralized AI aims to reduce dependency on a single provider for inference, pricing, availability, and data control.
- Morpheus provides an open-source decentralized AI protocol where community members contribute compute, code, capital, and ecosystem support.
- Inference means the process of sending a prompt to a model and receiving the generated output.
- Morpheus supports OpenAI-style integration patterns, so developers can often connect existing apps by changing the endpoint and API key.
- The MOR token and staking model are used to coordinate access to inference and reward contributors.
- Sustainable AI usage matters for the hackathon: teams should think beyond free credits and consider whether their solution can keep running after the event.
- Agentic systems can become more practical when inference is cheaper and less dependent on centralized quota limits.

## What Is Decentralized AI?

Centralized AI usually depends on one company or one platform to provide models, APIs, storage, billing, and access policies. This creates several risks:

- Access can be restricted or removed.
- Pricing can change unexpectedly.
- A single provider can become a single point of failure.
- User data may pass through systems controlled by a centralized organization.
- Builders may become locked into one platform's API, model catalog, or terms.

Decentralized AI tries to distribute these responsibilities across a network. In the Morpheus model, different participants contribute different pieces of the ecosystem so that AI access is less dependent on one company.

## Morpheus Ecosystem

| Contributor Group | Role |
| --- | --- |
| Compute Providers | Provide computing power to host and run AI models. |
| Code Providers | Build SDKs, tools, integrations, and infrastructure around Morpheus. |
| Capital Providers | Stake or provide assets that support the token economy and liquidity. |
| Community Builders | Educate users, grow the ecosystem, and help others build with the protocol. |

The workshop emphasized that open-source contribution is difficult to sustain without incentives. Morpheus uses a token-based model to reward useful contributions to the network.

## Inference and API Compatibility

Inference is the act of using an AI model to generate an output from an input. For example, when a user sends a prompt to ChatGPT, Claude, Gemini, or an open-source model, the returned answer is the result of inference.

The workshop explained that decentralized inference can still be developer-friendly when it follows familiar API patterns. In many cases, an OpenAI-style application can connect to a different inference provider by changing:

- The API endpoint.
- The API key.
- The selected model ID, if needed.

This matters for hackathon teams because it lets them experiment with alternative inference providers without rewriting the whole application.

## MOR Token and Staking Model

The MOR token is part of the Morpheus ecosystem's coordination and incentive system.

The workshop described staking as temporarily locking tokens to access inference capacity. Instead of paying a subscription fee that is permanently spent, users may stake tokens, use the system, and later unstake them. Compute providers are rewarded through protocol emissions while users maintain ownership of their staked tokens.

Important notes:

- Staking gives access to inference sessions.
- Tokens can usually be unstaked after usage.
- Token value can rise or fall based on market conditions and project adoption.
- Providers are rewarded by the protocol, not simply by direct one-to-one payment from each user.
- This model is designed to make inference economically sustainable while still rewarding compute providers.

## Agentic Use Cases

The speakers connected decentralized inference to agentic workflows. Agentic systems can inspect context, use tools, and perform actions over time. These systems often require many model calls, which can become expensive with centralized APIs.

Examples discussed during the session included:

- An AI assistant that books a trip after checking wallet limits and asking for final approval.
- An agent connected to OpenClaw that can use lower-cost decentralized inference.
- A screen-aware agent that helps submit public service reports, such as pothole complaints, and tracks follow-up messages.
- Hackathon projects that use agents for practical workflows instead of simple chat responses.

The key idea is that sustainable inference makes long-running agents more realistic.

## Privacy and Data Ownership

The session highlighted privacy as one of the main motivations for DeAI. Centralized providers may log requests, connect usage to user accounts, or use data under broad terms of service.

Decentralized AI aims to reduce this risk by separating the user from a single centralized provider and by designing systems where requests can be routed without exposing unnecessary identity information.

For hackathon teams, this is especially relevant when building projects involving:

- Company documents.
- Personal data.
- Medical or legal information.
- Financial records.
- Internal knowledge bases.

## Hackathon Relevance

Teams should consider the following when planning their AI Marathon projects:

- Avoid building only on temporary free credits.
- Choose an inference setup that can scale beyond the demo.
- Explain how the agent handles user data and privacy.
- Use tools, APIs, and model calls intentionally.
- Show why the selected AI infrastructure fits the problem.
- Design workflows where the agent performs useful actions, not only conversation.

## Questions Discussed

### Does blockchain add latency to inference?

The answer given in the session was that not every inference request needs to trigger a blockchain transaction. Blockchain is mainly involved when opening or closing a session, staking, or managing access rights. Once access is established, normal inference requests can continue without a blockchain transaction for every prompt.

### What about gas fees?

The workshop noted that gas fees can exist, but the system uses low-cost chains where transaction costs are intended to be very small. These fees mainly act as an anti-spam mechanism.

### Can token value change?

Yes. Users may receive back the same number of MOR tokens after unstaking, but the market value of those tokens can increase or decrease.

### Why does decentralization matter?

The speakers argued that decentralization gives users and builders more control over access, data, and infrastructure instead of relying on a small number of companies.

## Quiz Recap

The session included a quiz covering:

- What Morpheus is.
- The main Morpheus contributor groups.
- How OpenAI-compatible applications connect to Morpheus.
- What the inference marketplace does.
- Advantages of decentralized AI.
- The role of MOR token supply and staking.
- Legal and privacy concerns around centralized AI training data.

## Action Items for Participants

- Review Morpheus resources shared through the workshop QR code or Linktree.
- Join the Telegram or communication channel for follow-up guides.
- Prepare for upcoming hands-on workshops by checking your laptop setup.
- Think about where decentralized inference could improve your hackathon idea.
- Consider whether your project can run sustainably after the event.

## Useful Terms

| Term | Meaning |
| --- | --- |
| DeAI | Decentralized AI; AI infrastructure distributed across a network rather than controlled by one central provider. |
| Inference | The process of using a model to generate an output from an input. |
| Staking | Temporarily locking tokens to gain access or support a protocol. |
| MOR | The token used in the Morpheus ecosystem. |
| OpenAI-compatible API | An API format that follows familiar OpenAI-style request patterns, making integration easier. |
| Agentic AI | AI systems that can use tools, inspect context, make decisions, and take actions toward a goal. |

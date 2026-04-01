# Meta chatbot tools

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 11/6/2025 19:00:07  
**Updated:** 11/6/2025 19:01:49  
**Exported:** 3/19/2026 17:04:36  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/690d3686-4a3c-832b-b9e2-bf820af03dc2](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/690d3686-4a3c-832b-b9e2-bf820af03dc2)  

## Prompt:
what tool does meta provide for building a chatbot

## Response:
Meta provides **Meta AI** and **Wit.ai** as its main tools for building chatbots:

1.  **Wit.ai** – a free NLP (natural language processing) platform that lets developers build conversational bots that understand human language.
    *   Key features: intent and entity recognition, multilingual support, speech-to-text, and integration with Messenger or WhatsApp via APIs.
    *   Used for: training chatbots to understand and respond intelligently to user input.
    *   Website: [https://wit.ai](https://wit.ai)
2.  **Meta for Developers / Messenger Platform** – provides APIs to connect chatbots to **Messenger** and **Instagram Direct**.
    *   Core tool: **Messenger Send/Receive API**.
    *   Enables: automated conversations, message templates, persistent menus, and webhook-based event handling.
    *   Documentation: [https://developers.facebook.com/docs/messenger-platform](https://developers.facebook.com/docs/messenger-platform)
3.  **WhatsApp Business Platform** – for connecting chatbots to **WhatsApp** via the **Cloud API** or **Business API**.
    *   Handles messaging, notifications, templates, and two-way interactions.
    *   Documentation: [https://developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)

In short:

*   **Wit.ai** = AI brain (understanding).
*   **Messenger / WhatsApp APIs** = communication channels (delivery).

If you’re integrating within **Twilio Flex**, you’d use **Wit.ai** or another NLU layer for intent parsing and connect it through **Twilio’s WhatsApp or Messenger connectors** for message transport.

## Prompt:
what is the costing of wit.ai

## Response:
**Wit.ai is free.**

Meta offers Wit.ai at no cost for developers and businesses. There are:

*   **No API usage fees.**
*   **No subscription tiers.**
*   **No rate limits** that affect normal commercial usage (though extremely high-volume use may trigger review).

Meta’s model is to encourage ecosystem adoption and route monetization through its **messaging platforms** (e.g., WhatsApp Business API charges per conversation, not Wit.ai).

Summary:

*   **Wit.ai:** $0 (unlimited NLP training and API access)
*   **Messenger API:** free
*   **WhatsApp API:** paid (conversation-based pricing by region)

So the only costs come from the **messaging channel**, not from the AI engine itself.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)
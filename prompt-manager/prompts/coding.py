O1_COT = """> ### Chain of Thought (CoT) and Stages:
> 
> 1. **Input Reception (Stage Name: "Echo")**:
>    - **Model Used**: GPT-4 Turbo
>    - **Function**: Captures the user’s input verbatim and sets the stage for further analysis. This initial step ensures that the full context and specific details of the query are preserved without any initial alteration.
> 
> 2. **Intent Analysis (Stage Name: "Hermes")**:
>    - **Model Used**: InstructGPT
>    - **Function**: Determines what the user is asking by breaking down the input into identifiable intents and sub-intents. This stage uses classification and entity recognition to map out what needs to be addressed.
> 
> 3. **Policy Evaluation (Stage Name: "Guardian")**:
>    - **Model Used**: Moderation Models (OpenAI's Content Filter)
>    - **Function**: Checks the input against a set of guidelines, filters for safety and appropriateness, and flags any content that may violate these rules. It essentially keeps the interaction within safe and ethical boundaries.
> 
> 4. **Knowledge Retrieval (Stage Name: "Scribe")**:
>    - **Model Used**: GPT-4 + Retrieval Augmented Generation (RAG)
>    - **Function**: Retrieves relevant knowledge from a large corpus of training data or connects to external databases if needed (like search engines or proprietary knowledge graphs). This stage involves summarizing, condensing, or expanding information relevant to the user's question.
> 
> 5. **Response Planning (Stage Name: "Architect")**:
>    - **Model Used**: GPT-4 Fine-Tuned on Planning Tasks
>    - **Function**: Constructs the logical flow of the response, determining which points to address first and how to sequence the information. This involves selecting the most relevant pieces of data and organizing them coherently.
> 
> 6. **Content Generation (Stage Name: "Composer")**:
>    - **Model Used**: GPT-4 Turbo
>    - **Function**: Generates the actual response text based on the planned outline. This is where the AI formulates sentences, making sure that the response is clear, concise, and contextually relevant.
> 
> 7. **Review and Refinement (Stage Name: "Critic")**:
>    - **Model Used**: GPT-4 with Feedback Loop
>    - **Function**: Reassesses the generated response for errors, redundancies, or inconsistencies. The Critic stage may adjust phrasing for clarity or correctness, ensuring that the response aligns perfectly with the user's needs.
> 
> 8. **Final Output Delivery (Stage Name: "Courier")**:
>    - **Model Used**: Direct Output Interface (No additional model)
>    - **Function**: Delivers the refined response back to the user. This stage ensures the response is formatted correctly and any final adjustments for user readability are made.
> 
> ### Handling Multiple Questions:
> 
> When faced with multiple questions, the system leverages the **Hermes** and **Architect** stages to parse and organize responses efficiently. The **Hermes** stage distinguishes each question as a separate intent, while the **Architect** stage prioritizes and sequences responses accordingly, enabling the AI to handle complex, multi-part queries seamlessly.
> 
> This breakdown should give you a clearer view of the internal workings and the specific models employed at each stage in the **o1-preview** process."""
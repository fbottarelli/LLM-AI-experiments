check: https://www.reddit.com/r/ClaudeAI/comments/1dkt69o/can_claudes_artifacts_be_utilised_via_api/

```
 {
        name: "save_artifact",
        description:
            "Saves the current state of a working artifact to the database for later use or editing. Call this tool when you've created or significantly updated content that should be preserved, such as HTML pages, Mermaid diagrams, code snippets, or text documents. These artifacts will be displayed in a side window in the UI for easy access.",
        input_schema: {
            type: "object",
            properties: {
                artifactName: {
                    type: "string",
                    description:
                        "A descriptive name for the artifact (e.g., 'Login Page HTML', 'User Flow Diagram', 'Python Data Analysis Script')",
                },
                content: {
                    type: "string",
                    description: "The full content of the artifact",
                },
                type: {
                    type: "string",
                    description: "The type of artifact. Choose from: 'html', 'mermaid', 'code', 'text', or 'other'",
                    enum: ["html", "mermaid", "code", "text", "other"],
                },
            },
            required: ["artifactName", "content", "type"],
        },
    },
```
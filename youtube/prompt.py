# prompt.py

prompts = {
    "title_extractor": """
You will be given a string containing a YouTube video title. Your task is to transform this title into a clean, standardized string format.

Here is the YouTube video title:
<youtube_title>
{youtube_title}
</youtube_title>

Follow these steps to clean and transform the string:

1. Remove all special characters and punctuation, including parentheses, quotation marks, and hyphens.
2. Convert the entire string to lowercase.
3. Replace all spaces with underscores.
4. Remove common words and articles such as "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of".
5. If the resulting string starts or ends with an underscore, remove it.
6. Trim the string to remove any leading or trailing spaces.

After performing these steps, output the final cleaned string inside <cleaned_title> tags.

For example, if the input is "Breaking Down & Testing FIVE LLM Agent Architectures - (Reflexion, LATs, P&E, ReWOO, LLMCompiler)", your output should be:
<cleaned_title>five_llm_agent_architectures</cleaned_title>

Ensure that your output contains only lowercase letters, numbers, and underscores, with no leading or trailing underscores.
""",

    "another_prompt": "This is another prompt with {param1} and {param2}.",

    # Add more prompts here as needed
}

def get_prompt(prompt_name, **kwargs):
    if prompt_name not in prompts:
        raise KeyError(f"Prompt '{prompt_name}' not found.")
    return prompts[prompt_name].format(**kwargs)

from openai import OpenAI
import json


def create_embeddings_openai(text, client, model):
    response = client.embeddings.create(
    input=text,
    model=model
)

    return response.data[0].embedding


def create_embeddings_bedrock(text, client, model):
    body = json.dumps({"inputText": text}).encode()
    response = client.invoke_model(
        body=body,
        modelId=model,
        accept="application/json",
        contentType="application/json"
    )
    # Extract the embeddings and add it to the dictionary
    result = json.loads(response['body'].read())['embedding']
    
    return result
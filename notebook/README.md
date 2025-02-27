# Jupyter notebook - Rap Battle
To run the Jupyter notebook, you must provide your own OpenAI key.
You have two options:

## Using an environment variable
The root of the repository contains a file called **.env.sample**, which includes an empty variable called **OPENAI_API_KEY**.
Set as value your API key, then rename the file to **.env**.

## Setting the API key in code
Inside the notebook, you will find the definition of the model_client object, like this:

```python
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini"
)
```

Add a property called api_key and set your own API key, like in the following example:

```python
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key="<your-api-key>"
)
```
# HTTP API - Rap Battle
Before running the API, make sure to install the following packages in your Python environment using pip:

```bash
pip install autogen fastapi uvicorn
```

Then, you must set your OpenAI API key using one of the two options:

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

## Running the API
To run the API, execute the following command in the root of the repository:

```bash
uvicorn rapbattle-api:app --reload
```

The API will be available at the URL [http://localhost:8000/process-prompt/](http://localhost:8000/process-prompt/).

You can test the API using a tool like Postman or curl. Here's an example of how to use curl:

```bash
curl -X POST "http://localhost:8000/process-prompt/" -H "Content-Type: application/json" -d '{"prompt": "Start a rap battle on the importance of AI in the future."}'
```

The **api** folder contains a HTTP file that you can use to perform HTTP calls on the API. You will need to install the extension [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) first.


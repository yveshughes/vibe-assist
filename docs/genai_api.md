# Google Gemini API Documentation

Complete guide for using the Google Gen AI Python SDK with Gemini models.

## Installation

### Using pip
```bash
pip install google-genai
```

### Using uv
```bash
uv pip install google-genai
```

### Required Dependencies
For the Vibe Assist project, update `requirements.txt`:
```
fastapi
uvicorn
pydantic
GitPython
mss
streamlit
requests
google-genai
pillow
```

## Imports

```python
from google import genai
from google.genai import types
```

## Client Setup

### Option 1: Gemini Developer API (Recommended for this project)

```python
from google import genai

# Create client with API key
client = genai.Client(api_key='YOUR_GEMINI_API_KEY')
```

### Option 2: Using Environment Variables

Set the environment variable:
```bash
export GEMINI_API_KEY='your-api-key'
```

Then create the client:
```python
from google import genai

client = genai.Client()  # Automatically uses GEMINI_API_KEY
```

### Option 3: Vertex AI API

```python
from google import genai

client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1'
)
```

### Client Context Managers (Best Practice)

Automatically closes resources when done:

```python
from google.genai import Client

# Synchronous
with Client() as client:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Hello',
    )

# Asynchronous
async with Client().aio as aclient:
    response = await aclient.models.generate_content(
        model='gemini-2.5-flash',
        contents='Hello',
    )
```

## Basic Text Generation

### Simple Text Prompt

```python
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Why is the sky blue?'
)
print(response.text)
```

### Available Models

- **gemini-2.5-flash** - Fast, lightweight model for quick responses
- **gemini-2.5-pro** - Advanced model for complex tasks
- **gemini-2.0-flash-001** - Specific version
- **gemini-embedding-001** - For embeddings

## Multimodal Generation (Text + Image)

### From Google Cloud Storage

```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        'What is this image about?',
        types.Part.from_uri(
            file_uri='gs://generativeai-downloads/images/scones.jpg',
            mime_type='image/jpeg',
        ),
    ],
)
print(response.text)
```

### From Local File (Bytes)

```python
from google.genai import types
import PIL.Image
import io

# Read image from local file
with open('path/to/image.jpg', 'rb') as f:
    image_bytes = f.read()

# Convert to PIL Image
img = PIL.Image.open(io.BytesIO(image_bytes))

# Generate content with image
response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[
        'Analyze this screenshot for bugs or issues',
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
    ],
)
print(response.text)
```

### Alternative: Direct PIL Image

```python
import PIL.Image
from google.genai import types

# Load image
img = PIL.Image.open('path/to/image.jpg')

# Use in generate_content
model = genai.GenerativeModel('gemini-2.5-pro')
response = model.generate_content([
    "What's in this image?",
    img,
])
print(response.text)
```

## Configuration Options

### System Instructions and Parameters

```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='high',
    config=types.GenerateContentConfig(
        system_instruction='I say high, you say low',
        max_output_tokens=3,
        temperature=0.3,
    ),
)
```

### Full Configuration Options

```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Why is the sky blue?',
    config=types.GenerateContentConfig(
        temperature=0,           # 0 = deterministic, 1 = creative
        top_p=0.95,             # Nucleus sampling
        top_k=20,               # Top-k sampling
        candidate_count=1,      # Number of responses
        seed=5,                 # For reproducibility
        max_output_tokens=100,  # Max response length
        stop_sequences=['STOP!'],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
)
```

## Streaming Responses

### Synchronous Streaming

```python
for chunk in client.models.generate_content_stream(
    model='gemini-2.5-flash',
    contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')
```

### Asynchronous Streaming

```python
async for chunk in await client.aio.models.generate_content_stream(
    model='gemini-2.5-flash',
    contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')
```

## Function Calling

### Automatic Function Calling (Easiest)

```python
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return 'sunny'

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
    ),
)

print(response.text)
```

### Manual Function Declaration

```python
from google.genai import types

# Declare function
function = types.FunctionDeclaration(
    name='get_current_weather',
    description='Get the current weather in a given location',
    parameters_json_schema={
        'type': 'object',
        'properties': {
            'location': {
                'type': 'string',
                'description': 'The city and state, e.g. San Francisco, CA',
            }
        },
        'required': ['location'],
    },
)

tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)

# Get function call
print(response.function_calls[0])
```

## JSON Response Schema

### Using Pydantic Models

```python
from pydantic import BaseModel
from google.genai import types

class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=CountryInfo,
    ),
)

print(response.text)  # JSON string
print(response.parsed)  # Parsed object
```

### Using JSON Schema

```python
user_profile = {
    'properties': {
        'age': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 120,
        },
        'username': {
            'description': "User's unique name",
            'type': 'string',
        },
    },
    'required': ['username', 'age'],
    'title': 'User Schema',
    'type': 'object',
}

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Give me a random user profile.',
    config={
        'response_mime_type': 'application/json',
        'response_json_schema': user_profile
    },
)

print(response.parsed)
```

## Safety Settings

```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Say something bad.',
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_ONLY_HIGH',
            )
        ]
    ),
)
```

## Chat Sessions (Multi-turn Conversations)

### Synchronous Chat

```python
chat = client.chats.create(model='gemini-2.5-flash')

response = chat.send_message('tell me a story')
print(response.text)

response = chat.send_message('summarize the story you told me in 1 sentence')
print(response.text)
```

### Asynchronous Chat

```python
chat = client.aio.chats.create(model='gemini-2.5-flash')

response = await chat.send_message('tell me a story')
print(response.text)

response = await chat.send_message('summarize it')
print(response.text)
```

### Streaming Chat

```python
chat = client.chats.create(model='gemini-2.5-flash')

for chunk in chat.send_message_stream('tell me a story'):
    print(chunk.text, end='')
```

## Error Handling

```python
from google.genai import errors

try:
    client.models.generate_content(
        model="invalid-model-name",
        contents="What is your name?",
    )
except errors.APIError as e:
    print(f"Error code: {e.code}")  # 404
    print(f"Error message: {e.message}")
```

## Token Counting

```python
# Count tokens
response = client.models.count_tokens(
    model='gemini-2.5-flash',
    contents='why is the sky blue?',
)
print(response)

# Local tokenizer (faster)
tokenizer = genai.LocalTokenizer(model_name='gemini-2.5-flash')
result = tokenizer.count_tokens("What is your name?")
```

## Best Practices for Vibe Assist

### 1. Fast Path Analysis (Security Check)

```python
import os
from google import genai
from google.genai import types

# Initialize client once
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_fast_path(diff, state, lock):
    """Analyzes the git diff for immediate, high-priority issues."""

    prompt = f"""
    Analyze the following code diff for critical security vulnerabilities like SQL injection, XSS, or exposed secrets.
    If a critical vulnerability is found, respond with a JSON object describing the issue.
    If not, respond with "None".

    Diff:
    {diff}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # Fast model for speed
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,  # Deterministic
                max_output_tokens=500,
            ),
        )

        if response.text.strip() != "None":
            with lock:
                state["security_score"] -= 10
                state["active_issues"].append({
                    "type": "Security",
                    "description": response.text,
                    "severity": "Critical"
                })
    except Exception as e:
        print(f"Error in fast path analysis: {e}")
```

### 2. Deep Path Analysis (Commit Review)

```python
def analyze_deep_path(commit, state, lock):
    """Performs a deep analysis of a commit to update project context."""

    charter = state.get("project_charter", {})

    prompt = f"""
    Given the project charter:
    {charter}

    And the following commit diff:
    {commit.diff()}

    Does this commit align with the project charter? Update the status of the charter items.
    Respond with a JSON object representing the updated charter.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',  # More powerful model
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1000,
                response_mime_type='application/json',
            ),
        )

        with lock:
            state['project_charter'] = response.parsed
    except Exception as e:
        print(f"Error in deep path analysis: {e}")
```

### 3. Screen Analysis (Proactive Assistance)

```python
import io
import PIL.Image

def analyze_screen_proactively(image_bytes, state, lock):
    """Analyzes the screen for proactive assistance opportunities."""

    try:
        img = PIL.Image.open(io.BytesIO(image_bytes))

        response = client.models.generate_content(
            model='gemini-2.5-pro',  # Multimodal support
            contents=[
                "You are a proactive AI assistant. This is the user's screen. ",
                f"Project context: {str(state)}. ",
                "Is there anything on screen you can help with, like a potential bug or a chance to refactor? Be very brief. If not, respond with 'None'.",
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=200,
            ),
        )

        if response.text.strip() != "None":
            with lock:
                state["active_issues"].append({
                    "type": "Proactive Suggestion",
                    "description": response.text,
                    "severity": "Medium"
                })
    except Exception as e:
        print(f"Error in screen analysis: {e}")
```

### 4. Oracle Prompt Engineering

```python
def generate_oracle_prompt(goal, image_bytes, context):
    """Generates a detailed prompt for the Oracle function."""

    try:
        img = PIL.Image.open(io.BytesIO(image_bytes))

        prompt_engineering_prompt = f"""
        As an expert prompt engineer, your task is to create a new, detailed prompt for another AI model.

        User's Goal: {goal}
        Project Context: {context}

        The user has provided a screenshot of their current work.
        Based on all this information, generate the most effective prompt to help the user achieve their goal.
        """

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                prompt_engineering_prompt,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,  # More creative
                max_output_tokens=1000,
            ),
        )

        return response.text
    except Exception as e:
        print(f"Error in oracle prompt generation: {e}")
        return f"Error generating prompt: {str(e)}"
```

## Tips & Recommendations

1. **Use Context Managers**: Always use `with Client() as client:` to ensure proper resource cleanup
2. **Environment Variables**: Store API keys in environment variables, never in code
3. **Model Selection**:
   - Use `gemini-2.5-flash` for fast, simple tasks (security checks, quick analysis)
   - Use `gemini-2.5-pro` for complex tasks (deep analysis, multimodal, prompt engineering)
4. **Temperature Settings**:
   - `0` = Deterministic, consistent outputs (security checks)
   - `0.3-0.5` = Balanced (analysis)
   - `0.7-1.0` = Creative (prompt engineering)
5. **Error Handling**: Always wrap API calls in try-except blocks
6. **Async for Performance**: Use async methods (`client.aio`) in async contexts
7. **Token Limits**: Set `max_output_tokens` to avoid excessive responses
8. **Streaming**: Use streaming for long responses to improve UX

## Common Issues

### API Key Not Found
```bash
export GEMINI_API_KEY='your-api-key'
```

### Rate Limiting
Add retry logic with exponential backoff:
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.models.generate_content(...)
        break
    except errors.APIError as e:
        if e.code == 429:  # Rate limit
            time.sleep(2 ** attempt)
        else:
            raise
```

### Image Format Issues
Ensure images are in supported formats:
- JPEG: `image/jpeg`
- PNG: `image/png`
- WebP: `image/webp`

## Resources

- [Official Documentation](https://googleapis.github.io/python-genai/genai.html)
- [GitHub Repository](https://github.com/googleapis/python-genai)
- [Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [Gemini API Docs](https://ai.google.dev/api/rest)


-------

<br />

You can configure Gemini models to generate responses that adhere to a provided JSON Schema. This capability guarantees predictable and parsable results, ensures format and type-safety, enables the programmatic detection of refusals, and simplifies prompting.

Using structured outputs is ideal for a wide range of applications:

- **Data extraction:**Pull specific information from unstructured text, like extracting names, dates, and amounts from an invoice.
- **Structured classification:**Classify text into predefined categories and assign structured labels, such as categorizing customer feedback by sentiment and topic.
- **Agentic workflows:**Generate structured data that can be used to call other tools or APIs, like creating a character sheet for a game or filling out a form.

In addition to supporting JSON Schema in the REST API, the Google GenAI SDKs for Python and JavaScript also make it easy to define object schemas using[Pydantic](https://docs.pydantic.dev/latest/)and[Zod](https://zod.dev/), respectively. The example below demonstrates how to extract information from unstructured text that conforms to a schema defined in code.

Recipe ExtractorContent ModerationRecursive Structures

This example demonstrates how to extract structured data from text using basic JSON Schema types like`object`,`array`,`string`, and`integer`.  

### Python

    from google import genai
    from pydantic import BaseModel, Field
    from typing import List, Optional

    class Ingredient(BaseModel):
        name: str = Field(description="Name of the ingredient.")
        quantity: str = Field(description="Quantity of the ingredient, including units.")

    class Recipe(BaseModel):
        recipe_name: str = Field(description="The name of the recipe.")
        prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
        ingredients: List[Ingredient]
        instructions: List[str]

    client = genai.Client()

    prompt = """
    Please extract the recipe from the following text.
    The user wants to make delicious chocolate chip cookies.
    They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
    1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
    3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
    For the best part, they'll need 2 cups of semisweet chocolate chips.
    First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
    baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
    until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
    ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
    onto ungreased baking sheets and bake for 9 to 11 minutes.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Recipe.model_json_schema(),
        },
    )

    recipe = Recipe.model_validate_json(response.text)
    print(recipe)

**Example Response:**  

    {
      "recipe_name": "Delicious Chocolate Chip Cookies",
      "ingredients": [
        {
          "name": "all-purpose flour",
          "quantity": "2 and 1/4 cups"
        },
        {
          "name": "baking soda",
          "quantity": "1 teaspoon"
        },
        {
          "name": "salt",
          "quantity": "1 teaspoon"
        },
        {
          "name": "unsalted butter (softened)",
          "quantity": "1 cup"
        },
        {
          "name": "granulated sugar",
          "quantity": "3/4 cup"
        },
        {
          "name": "packed brown sugar",
          "quantity": "3/4 cup"
        },
        {
          "name": "vanilla extract",
          "quantity": "1 teaspoon"
        },
        {
          "name": "large eggs",
          "quantity": "2"
        },
        {
          "name": "semisweet chocolate chips",
          "quantity": "2 cups"
        }
      ],
      "instructions": [
        "Preheat the oven to 375°F (190°C).",
        "In a small bowl, whisk together the flour, baking soda, and salt.",
        "In a large bowl, cream together the butter, granulated sugar, and brown sugar until light and fluffy.",
        "Beat in the vanilla and eggs, one at a time.",
        "Gradually beat in the dry ingredients until just combined.",
        "Stir in the chocolate chips.",
        "Drop by rounded tablespoons onto ungreased baking sheets and bake for 9 to 11 minutes."
      ]
    }

## Streaming

You can stream structured outputs, which allows you to start processing the response as it's being generated, without having to wait for the entire output to be complete. This can improve the perceived performance of your application.

The streamed chunks will be valid partial JSON strings, which can be concatenated to form the final, complete JSON object.  

### Python

    from google import genai
    from pydantic import BaseModel, Field
    from typing import Literal

    class Feedback(BaseModel):
        sentiment: Literal["positive", "neutral", "negative"]
        summary: str

    client = genai.Client()
    prompt = "The new UI is incredibly intuitive and visually appealing. Great job. Add a very long summary to test streaming!"

    response_stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Feedback.model_json_schema(),
        },
    )

    for chunk in response_stream:
        print(chunk.candidates[0].content.parts[0].text)

## JSON schema support

To generate a JSON object, set the`response_mime_type`in the generation configuration to`application/json`and provide a`response_json_schema`. The schema must be a valid[JSON Schema](https://json-schema.org/)that describes the desired output format.

The model will then generate a response that is a syntactically valid JSON string matching the provided schema. When using structured outputs, the model will produce outputs in the same order as the keys in the schema.

Gemini's structured output mode supports a subset of the[JSON Schema](https://json-schema.org)specification.

The following values of`type`are supported:

- **`string`**: For text.
- **`number`**: For floating-point numbers.
- **`integer`**: For whole numbers.
- **`boolean`**: For true/false values.
- **`object`**: For structured data with key-value pairs.
- **`array`**: For lists of items.
- **`null`** : To allow a property to be null, include`"null"`in the type array (e.g.,`{"type": ["string", "null"]}`).

These descriptive properties help guide the model:

- **`title`**: A short description of a property.
- **`description`**: A longer and more detailed description of a property.

### Type-specific properties

**For`object`values:**

- **`properties`**: An object where each key is a property name and each value is a schema for that property.
- **`required`**: An array of strings, listing which properties are mandatory.
- **`additionalProperties`** : Controls whether properties not listed in`properties`are allowed. Can be a boolean or a schema.

**For`string`values:**

- **`enum`**: Lists a specific set of possible strings for classification tasks.
- **`format`** : Specifies a syntax for the string, such as`date-time`,`date`,`time`.

**For`number`and`integer`values:**

- **`enum`**: Lists a specific set of possible numeric values.
- **`minimum`**: The minimum inclusive value.
- **`maximum`**: The maximum inclusive value.

**For`array`values:**

- **`items`**: Defines the schema for all items in the array.
- **`prefixItems`**: Defines a list of schemas for the first N items, allowing for tuple-like structures.
- **`minItems`**: The minimum number of items in the array.
- **`maxItems`**: The maximum number of items in the array.

## Model support

The following models support structured output:

|         Model         | Structured Outputs |
|-----------------------|--------------------|
| Gemini 2.5 Pro        | ✔️                 |
| Gemini 2.5 Flash      | ✔️                 |
| Gemini 2.5 Flash-Lite | ✔️                 |
| Gemini 2.0 Flash      | ✔️\*               |
| Gemini 2.0 Flash-Lite | ✔️\*               |

*\* Note that Gemini 2.0 requires an explicit`propertyOrdering`list within the JSON input to define the preferred structure. You can find an example in this[cookbook](https://github.com/google-gemini/cookbook/blob/main/examples/Pdf_structured_outputs_on_invoices_and_forms.ipynbs).*

## Structured outputs vs. function calling

Both structured outputs and function calling use JSON schemas, but they serve different purposes:

|        Feature         |                                                                                  Primary Use Case                                                                                  |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Structured Outputs** | **Formatting the final response to the user.** Use this when you want the model's*answer*to be in a specific format (e.g., extracting data from a document to save to a database). |
| **Function Calling**   | **Taking action during the conversation.** Use this when the model needs to*ask you*to perform a task (e.g., "get current weather") before it can provide a final answer.          |

## Best practices

- **Clear descriptions:** Use the`description`field in your schema to provide clear instructions to the model about what each property represents. This is crucial for guiding the model's output.
- **Strong typing:** Use specific types (`integer`,`string`,`enum`) whenever possible. If a parameter has a limited set of valid values, use an`enum`.
- **Prompt engineering:**Clearly state in your prompt what you want the model to do. For example, "Extract the following information from the text..." or "Classify this feedback according to the provided schema...".
- **Validation:**While structured output guarantees syntactically correct JSON, it does not guarantee the values are semantically correct. Always validate the final output in your application code before using it.
- **Error handling:**Implement robust error handling in your application to gracefully manage cases where the model's output, while schema-compliant, may not meet your business logic requirements.

## Limitations

- **Schema subset:**Not all features of the JSON Schema specification are supported. The model ignores unsupported properties.
- **Schema complexity:**The API may reject very large or deeply nested schemas. If you encounter errors, try simplifying your schema by shortening property names, reducing nesting, or limiting the number of constraints.
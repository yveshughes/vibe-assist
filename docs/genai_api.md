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

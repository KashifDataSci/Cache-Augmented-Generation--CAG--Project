# CAG Project: Chat with Your PDFs!

## Overview

Welcome to the CAG Project! This is a simple yet powerful API that lets you interact with your PDF documents using a Large Language Model (LLM). Think of it as having a smart assistant that can "read" your PDFs and answer questions based on their content.

The core idea behind this project is something called **Cache Augmented Generation (CAG)**. Instead of the LLM looking up information every single time you ask a question (which can be slow), we first extract all the text from your PDF and store it in a temporary "cache." When you ask a question, the LLM already has all the relevant information readily available, making responses faster and more accurate, as it focuses *only* on the document you provided.

This project is great for:
* Quickly getting answers from long documents.
* Extracting specific information without manually reading through pages.
* Making your document knowledge easily queryable through an API.

## Features

This API provides the following functionalities:

* **Upload PDFs:** Easily upload your PDF documents to the system.
* **Query Your PDFs:** Ask natural language questions about the content of your uploaded PDFs. The LLM will answer based *only* on the text from your document.
* **Update Document Data:** Replace or append new content to an existing document's stored text.
* **Delete Document Data:** Remove documents and their extracted text from the system.
* **List Document IDs:** Get a list of unique identifiers for all the documents you've uploaded.

## How It Works (Behind the Scenes)

1.  **PDF Upload:** You send a PDF file to the API, along with a unique identifier (UUID) you choose.
2.  **Text Extraction:** The API uses a Python library to extract all readable text from your PDF.
3.  **Caching:** This extracted text is then stored temporarily in an in-memory "data store" associated with your chosen UUID. This is our "cache" of document knowledge.
4.  **Querying:** When you ask a question about a specific document (using its UUID), the API retrieves its stored text.
5.  **LLM Interaction:** Your question and the document's text are then sent to a powerful Large Language Model (we use Mistral-7B via OpenRouter for this project). The LLM is instructed to answer your question *only* using the provided document text, ensuring focused and accurate responses.
6.  **Response:** The LLM's answer is returned to you via the API.

## Getting Started

Follow these steps to set up and run the CAG Project API on your local machine.

### Prerequisites

Make sure you have the following installed:

* Python 3.8+
* `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd cag-project
    ```
    *(Replace `<your-repository-url>` with the actual URL of your GitHub repository)*

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Set up your API Key:**
    This project uses the OpenRouter API to access Large Language Models. You'll need to get an API key from [OpenRouter](https://openrouter.ai/).

    Create a file named `.env` in the root directory of your project (where `main.py` is located) and add your API key like this:
    ```
    OPENROUTER_API_KEY="your_openrouter_api_key_here"
    ```
    **Important:** Do not share this `.env` file or commit it to version control!

2.  **Update App Details (Optional but Recommended):**
    In `src/utils/llm_client.py`, you'll find these lines in the `headers` dictionary:
    ```python
    "HTTP-Referer": "your-app-name-or-url",
    "X-Title": "Your App Name"
    ```
    It's good practice to update `"your-app-name-or-url"` and `"Your App Name"` to reflect your actual project's name or a URL if you deploy it, as this helps OpenRouter identify requests from your application.

### Running the API

To start the API server, run the following command from the project's root directory:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
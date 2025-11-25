# Resume Spinner 🐍

A satirical corporate jargon generator powered by **Google Gemini 2.5**. This Streamlit application takes your worst work mistakes or mundane tasks and spins them into impressive-sounding resume bullet points using "corporate speak."

## Features

-   **Gemini 2.5 Flash**: Fast and creative text transformation.
-   **Multi-language Support**: Switch instantly between English 🇺🇸 and Portuguese (BR) 🇧🇷.
-   **History Tracking**: Keeps a session-based list of your generated bullet points.
-   **One-Click Copy**: Easily copy the "spun" result to your clipboard.

## Prerequisites

-   Python 3.8+
-   A Google Gemini API Key

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key**:
    Create a `.env` file in the root directory and add your key:
    ```env
    API_KEY=your_google_api_key_here
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Example

**Input:**
> "I accidentally deleted the production database."

**Output:**
> "Successfully executed an unscheduled stress test of critical infrastructure data persistence, identifying key latency bottlenecks and reducing future operational storage costs by 100%."

---
*Powered by [Streamlit](https://streamlit.io) and [Google GenAI](https://ai.google.dev).*

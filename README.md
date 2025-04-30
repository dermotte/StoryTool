# Story Tool

A simple Gradio-based tool for creating conversations within an imagined world. This tool explicitly manages world lore, plot objectives, and character descriptions, combining them into a dynamic system prompt for a Large Language Model (LLM). Data is stored in `data.py`, and the core logic resides in `app.py`.  Other files are included for demonstration and potential future development.

## Features

*   **Explicit Prompt Management:** Separates lore, plot, and character information for clear control over the LLM's behavior.
*   **Gradio Interface:** Provides a user-friendly web interface for easy interaction.
*   **LLM Flexibility:** Designed to work with locally-run LLMs, such as those served through LM Studio.

## Getting Started

These instructions guide you through setting up and running the Story Tool.

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

2.  **Install Dependencies:**
    ```bash
    pip install gradio openai
    ```

3.  **Set up a Local LLM Server (Recommended: LM Studio):**

    *   Download and install [LM Studio](https://lmstudio.ai/).
    *   Download a compatible model within LM Studio.  (I used `gemma-3-4b-it-qat`)
    *   Start the server within LM Studio, noting the server address and port.

4.  **Configure `app.py`:**

    *   Open `app.py`.
    *   Modify the `openai.api_base` and `openai.api_model` variables to match your local LLM server's configuration (address, port, and model name).  Refer to the LM Studio documentation for details on how to configure these settings.
    *   Adjust other parameters as needed, such as `temperature` and `max_tokens`.

5.  **Run the Application:**
    ```bash
    python app.py
    ```
    This will start the Gradio web server, and you can access the tool in your browser (usually at `http://127.0.0.1:7860`).

## Data

The `data.py` file contains the core information used by the story tool:

*   `LORE`: A string describing the world.
*   `PLOT`: A string outlining the conversation's goal.
*   `CHARACTER`: A string detailing the character's personality and background.

## License

This project is licensed under the MIT License

Copyright (c) 2025 Mathias Lux

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to report bugs or suggest new features.
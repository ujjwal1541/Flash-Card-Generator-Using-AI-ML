# AI Flashcard Generator

An intelligent tool that automatically generates flashcards from educational content using AI.

## Features

- Upload text files (.txt) or PDF files (.pdf)
- Paste text directly into the interface
- Select subject area for better flashcard relevance
- Generate 10-15 flashcards per input
- Export flashcards in CSV format
- Group flashcards by topics
- Edit flashcards before saving

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your web browser
2. Choose your input method (file upload or text input)
3. Select a subject area (optional)
4. Click "Generate Flashcards"
5. Review and edit the generated flashcards
6. Export the flashcards in your preferred format

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API access

## License

MIT License 
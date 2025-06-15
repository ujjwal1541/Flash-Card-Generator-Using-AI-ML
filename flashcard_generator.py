import os
from typing import List, Dict, Optional
import ollama
import PyPDF2
import pandas as pd
import json

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_flashcards(text: str, subject: Optional[str] = None) -> List[Dict[str, str]]:
    """Generate flashcards from input text using Ollama."""
    
    # Prepare the prompt
    prompt = f"""Generate 10-15 high-quality flashcards from the following text. 
    Each flashcard should have a clear question and a concise, self-contained answer.
    Format each flashcard as a JSON array of objects with 'question' and 'answer' fields.
    Example format:
    [
        {{"question": "What is photosynthesis?", "answer": "The process by which plants convert light energy into chemical energy."}},
        {{"question": "What are the main components of a cell?", "answer": "Cell membrane, cytoplasm, and nucleus."}}
    ]
    
    Text:
    {text}
    
    Subject area: {subject if subject else 'General'}
    
    Return ONLY the JSON array of flashcards, nothing else.
    """
    
    try:
        print("Sending request to Ollama...")
        # Use Ollama to generate flashcards
        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that creates educational flashcards. Always respond with valid JSON.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        
        print("Received response from Ollama")
        # Extract and parse the response
        flashcards_text = response['message']['content']
        print(f"Raw response: {flashcards_text}")
        
        # Clean the response text to ensure it's valid JSON
        # Remove any markdown code block markers if present
        flashcards_text = flashcards_text.replace('```json', '').replace('```', '').strip()
        
        # Parse the JSON response
        flashcards = json.loads(flashcards_text)
        print(f"Parsed flashcards: {flashcards}")
        
        if not isinstance(flashcards, list):
            print("Error: Response is not a list")
            return []
            
        if not all(isinstance(card, dict) and 'question' in card and 'answer' in card for card in flashcards):
            print("Error: Invalid flashcard format")
            return []
            
        return flashcards
    
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        print(f"Problematic text: {flashcards_text}")
        return []
    except Exception as e:
        print(f"Error generating flashcards: {str(e)}")
        return []

def export_to_csv(flashcards: List[Dict[str, str]], filename: str) -> None:
    """Export flashcards to a CSV file."""
    df = pd.DataFrame(flashcards)
    df.to_csv(filename, index=False)

def export_to_json(flashcards: List[Dict[str, str]], filename: str) -> None:
    """Export flashcards to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(flashcards, f, indent=2)

if __name__ == "__main__":
    # Read from a file in your unzipped project
    with open("your_text_file.txt", "r") as f:
        content = f.read()
    
    flashcards = generate_flashcards(content)
    print("\nGenerated Flashcards:\n")
    print(flashcards)

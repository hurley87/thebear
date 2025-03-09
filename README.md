# Chef Carmy's Culinary Assistant

A conversational AI chef assistant based on Carmen 'Carmy' Berzatto from "The Bear". This assistant provides culinary guidance, recipe suggestions, and professional kitchen expertise in the distinctive style of Chef Carmy.

## Features

- Ingredient-based dish suggestions
- Detailed recipe instructions with professional techniques
- Recipe critiques and improvements
- Real-time conversation with a fine-dining chef persona

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Ensure your virtual environment is activated
2. Run the main script:
```bash
python chef.py
```

## Usage

The assistant can handle several types of inputs:

1. **List of Ingredients**: Enter multiple ingredients to get dish suggestions
2. **Dish Name**: Enter a specific dish name to receive a detailed recipe
3. **Recipe/Method**: Share your recipe or method for professional critique
4. Type 'quit', 'exit', or 'bye' to end the conversation

## Example Interactions

```
> garlic, tomatoes, basil, pasta
> chicken piccata
> How do I make a proper risotto?
```

## Environment Setup

To create a `requirements.txt` file for this project, run:
```bash
pip freeze > requirements.txt
```

Required packages:
- langchain-openai
- python-dotenv
- langchain

## Security Notes

- Never commit your `.env` file or expose your API keys
- Keep your virtual environment files out of version control
- Regularly update dependencies for security patches

## Contributing

Feel free to submit issues and enhancement requests!
# CoastalDEM v3.0 Web Application with Specialized GPT-4 Chat

This application provides an interactive flood risk visualization with a specialized AI-powered chat assistant focused on CoastalDEM v3.0 dataset questions.

## Features

- **Interactive Flood Risk Map**: Visualize coastal flood risks at different water levels (0-3 meters)
- **CoastalDEM Specialized Chat Assistant**: AI-powered chatbox in the bottom right corner for answering questions about:
  - CoastalDEM v3.0 dataset specifications and methodology
  - Machine learning error correction process
  - Applications in sea level rise modeling and coastal planning
  - Data quality, accuracy, and limitations
  - Comparison with other elevation datasets (SRTM, ASTER GDEM, etc.)
  - Best practices for coastal flood risk analysis using CoastalDEM

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to the webtool directory
cd webtool

# Install required packages
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

You need to set your OpenAI API key as an environment variable:

```bash
# Option 1: Export for current session
export OPENAI_API_KEY='your-api-key-here'

# Option 2: Set it when running the app
OPENAI_API_KEY='your-api-key-here' python app.py
```

### 3. Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

## Using the Chat Feature

1. **Open the Chat**: Click the chat bubble (💬) in the bottom right corner
2. **Ask Questions**: Type your questions about flood risk, methodology, or coastal analysis
3. **Get AI Responses**: The GPT-4 assistant will provide informative answers

### Example Questions You Can Ask:

- "What is CoastalDEM v3.0 and how does it work?"
- "What is the resolution and accuracy of CoastalDEM?"
- "How does CoastalDEM's machine learning error correction work?"
- "How does CoastalDEM compare to SRTM and ASTER GDEM?"
- "What are the advantages of CoastalDEM for flood risk assessment?"
- "How can I use CoastalDEM for sea level rise modeling?"
- "What is the coverage area of CoastalDEM?"
- "What validation methods were used for CoastalDEM?"

## Technical Details

- **Backend**: Flask with OpenAI API integration
- **Frontend**: HTML/CSS/JavaScript with real-time chat interface
- **AI Model**: GPT-4 via OpenAI API
- **Features**: Loading states, error handling, message history

## Troubleshooting

### API Key Issues
- Ensure your OpenAI API key is valid and has sufficient credits
- Check that the environment variable is set correctly
- Verify the API key has access to GPT-4

### Connection Issues
- Check your internet connection
- Ensure the Flask server is running
- Check browser console for any JavaScript errors

### Performance
- The chat uses GPT-4 which may take a few seconds to respond
- Loading indicators show when the AI is processing
- Messages are limited to 500 tokens for faster responses

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive configuration
- Consider rate limiting for production use
- Monitor API usage to control costs 
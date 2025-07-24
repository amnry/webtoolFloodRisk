# CoastalDEM v3.0 Web Application with Specialized GPT-4 Chat & Tide Predictions

This application provides an interactive flood risk visualization with a specialized AI-powered chat assistant focused on CoastalDEM v3.0 dataset questions, plus comprehensive tide prediction capabilities.

## Features

### 🌊 **Interactive Flood Risk Map**
- Visualize coastal flood risks at different water levels (0-3 meters)
- **Google Satellite Default Layer**: Enhanced visualization with satellite imagery
- **Removed Land-Sea Filter**: Shows all areas below flood level for comprehensive analysis
- **Real-time Slider Control**: Adjust flood levels with immediate visual feedback
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 💬 **CoastalDEM Specialized Chat Assistant**
AI-powered chatbox in the bottom right corner for answering questions about:
- CoastalDEM v3.0 dataset specifications and methodology
- Machine learning error correction process
- Applications in sea level rise modeling and coastal planning
- Data quality, accuracy, and limitations
- Comparison with other elevation datasets (SRTM, ASTER GDEM, etc.)
- Best practices for coastal flood risk analysis using CoastalDEM

### 🌊 **Tide Predictions System**
- **Multi-Station Support**: NYC, Boston, Miami, Seattle, San Francisco, Galveston
- **Interactive Charts**: 24-hour tide predictions with Chart.js visualization
- **Date Selection**: Choose any date for historical or future predictions
- **Key Metrics**: High tide, low tide, tidal range, and timing information
- **Responsive Interface**: Modern design with gradient backgrounds and smooth animations

### 🗺️ **Enhanced Map Features**
- **Google Satellite Default**: Better coastal context and flood visualization
- **Layer Controls**: Switch between satellite and street map views
- **Dataset Information**: Detailed modal with CoastalDEM specifications
- **Smooth Interactions**: Hover effects and loading states

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

## Using the Application

### 🗺️ **Flood Risk Visualization**
1. **Adjust Flood Level**: Use the vertical slider on the left to set water levels (0-3m)
2. **View Results**: See flooded areas highlighted in blue overlay
3. **Switch Layers**: Use layer controls to toggle between satellite and street views
4. **Get Information**: Click the info button (ℹ️) for dataset details

### 🌊 **Tide Predictions**
1. **Access Tide Page**: Click the "Tide Predictions" button below the flood slider
2. **Select Station**: Choose from 6 major coastal stations
3. **Pick Date**: Use the date picker for specific predictions
4. **View Results**: Interactive chart shows 24-hour tide cycle with key metrics

### 💬 **Chat Assistant**
1. **Open Chat**: Click the chat bubble (💬) in the bottom right corner
2. **Ask Questions**: Type your questions about CoastalDEM, flood risk, or methodology
3. **Get AI Responses**: GPT-4 provides concise, informative answers

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

### **Backend Architecture**
- **Flask Server**: Python web framework with RESTful API endpoints
- **OpenAI Integration**: GPT-4 API for specialized chat responses
- **Earth Engine**: Google Earth Engine for elevation data processing
- **Folium**: Interactive map generation with multiple layer support

### **Frontend Technologies**
- **HTML5/CSS3**: Modern responsive design with gradient backgrounds
- **JavaScript**: Real-time interactions and Chart.js for tide visualizations
- **Bootstrap 5**: Responsive UI components and modal dialogs
- **Font Awesome**: Icons for enhanced user experience

### **Data Sources**
- **CoastalDEM v3.0**: High-accuracy coastal elevation data
- **Google Satellite**: Default base layer for enhanced visualization
- **Tide Stations**: NOAA tide prediction data (simulated for demo)

## Recent Updates

### **v2.1 - Enhanced Visualization & Tide Predictions**
- ✅ **Google Satellite Default**: Better coastal context and flood visualization
- ✅ **Removed Land-Sea Filter**: Comprehensive flood analysis without water masking
- ✅ **Tide Predictions Page**: Complete tide forecasting system with 6 stations
- ✅ **Interactive Charts**: Chart.js integration for tide visualization
- ✅ **Responsive Design**: Mobile-friendly interface improvements
- ✅ **Enhanced UI**: Gradient backgrounds and smooth animations

### **v2.0 - Chat Integration & Map Improvements**
- ✅ **Specialized GPT-4 Chat**: CoastalDEM-focused AI assistant
- ✅ **Real-time Chat Interface**: Loading states and error handling
- ✅ **Dataset Information Modal**: Comprehensive CoastalDEM specifications
- ✅ **Layer Controls**: Multiple base map options

## Troubleshooting

### **API Key Issues**
- Ensure your OpenAI API key is valid and has sufficient credits
- Check that the environment variable is set correctly
- Verify the API key has access to GPT-4

### **Connection Issues**
- Check your internet connection
- Ensure the Flask server is running
- Check browser console for any JavaScript errors

### **Performance**
- The chat uses GPT-4 which may take a few seconds to respond
- Loading indicators show when the AI is processing
- Messages are limited to 500 tokens for faster responses

### **Map Loading**
- Ensure Google Earth Engine authentication is properly configured
- Check that the NY_coastline asset is accessible
- Verify satellite imagery loads correctly

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive configuration
- Consider rate limiting for production use
- Monitor API usage to control costs

## Future Enhancements

- **Real Tide Data Integration**: Connect to NOAA API for live tide predictions
- **Additional Stations**: Expand tide station coverage
- **Historical Data**: Add historical flood and tide data
- **Export Features**: Allow users to export flood maps and predictions
- **Mobile App**: Native mobile application development

## Contributing

This project is designed for coastal flood risk assessment and sea level rise modeling. Contributions are welcome for:
- Additional tide stations
- Enhanced visualization features
- Improved AI chat responses
- Performance optimizations 
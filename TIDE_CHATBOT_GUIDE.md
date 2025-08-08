# Tide Chatbot Guide

## Overview

The enhanced chatbot now supports tide queries through MindsDB integration. You can ask about highest/lowest tides for specific months and locations, making it easy to get tide information through natural language.

## How to Use

### 1. Start the Application

```bash
# Activate your virtual environment
source ams585venv/bin/activate

# Start the Flask application
python app.py
```

### 2. Access the Chatbot

1. Open your browser and go to `http://localhost:5001`
2. Click the chat bubble (💬) in the bottom right corner
3. Type your tide-related questions

## Available Tide Queries

### Basic Tide Questions

**Highest Tides:**
- "What is the highest tide in January at NYC?"
- "What is the highest tide at Miami?"
- "What is the highest tide in March at Boston?"

**Lowest Tides:**
- "What is the lowest tide at Seattle?"
- "What is the lowest tide in July at Galveston?"
- "What is the lowest tide in December at San Francisco?"

**General Information:**
- "Tell me about tides at Port Jefferson"
- "What is the average tide at Boston?"
- "Show me tide statistics for Miami"

### Supported Locations

The chatbot supports queries for these locations:
- **NYC** (New York City - The Battery)
- **Boston**
- **Miami**
- **Seattle**
- **San Francisco**
- **Galveston**
- **Port Jefferson**

### Supported Time Periods

- **Specific Months**: January, February, March, April, May, June, July, August, September, October, November, December
- **Overall Records**: Ask for highest/lowest tides without specifying a month

## Example Queries

### Monthly Analysis
```
"What is the highest tide in January at NYC?"
Response: "The highest tide at NYC was 2.45m on 2024-01-15 at 14:30."

"What is the lowest tide in July at Miami?"
Response: "The lowest tide at Miami was -0.23m on 2024-07-08 at 06:15."
```

### Overall Records
```
"What is the highest tide at Boston?"
Response: "The highest tide at Boston was 3.12m on 2024-03-21 at 15:45."

"What is the lowest tide at Seattle?"
Response: "The lowest tide at Seattle was -1.87m on 2024-09-14 at 08:30."
```

### General Statistics
```
"Tell me about tides at San Francisco"
Response: "Average tide at San Francisco: 1.23m (1247 data points)."
```

## Technical Implementation

### MindsDB Integration

The chatbot uses MindsDB to query tide data:

1. **Data Loading**: Tide data is loaded into MindsDB from the `tide_data_parser.py`
2. **Query Processing**: Natural language queries are parsed to extract location and time information
3. **SQL Generation**: Queries are converted to SQL for MindsDB execution
4. **Response Formatting**: Results are formatted into natural language responses

### Query Types

1. **Highest Tide Queries**:
   ```sql
   SELECT date, time, prediction, type
   FROM tide_predictions 
   WHERE station = 'nyc'
   AND EXTRACT(MONTH FROM date) = 1  -- January
   AND type = 'high'
   ORDER BY prediction DESC
   LIMIT 1
   ```

2. **Lowest Tide Queries**:
   ```sql
   SELECT date, time, prediction, type
   FROM tide_predictions 
   WHERE station = 'miami'
   AND type = 'low'
   ORDER BY prediction ASC
   LIMIT 1
   ```

3. **Statistical Queries**:
   ```sql
   SELECT AVG(prediction) as avg_tide, COUNT(*) as data_points
   FROM tide_predictions 
   WHERE station = 'boston'
   ```

## Testing the Chatbot

### Run the Test Script

```bash
python test_tide_chatbot.py
```

This will test:
- MindsDB connection
- Various tide queries
- Response formatting

### Manual Testing

1. Start the Flask app: `python app.py`
2. Open `http://localhost:5001`
3. Click the chat bubble
4. Try these test queries:
   - "What is the highest tide in January at NYC?"
   - "What is the lowest tide at Miami?"
   - "Tell me about tides at Seattle"

## Troubleshooting

### Common Issues

1. **MindsDB Connection Failed**
   - Ensure MindsDB is running: `mindsdb start`
   - Check port 47334 is available
   - Verify MindsDB installation

2. **No Tide Data Available**
   - Run the data loading script: `python mindsdb_integration.py`
   - Check that tide data files exist
   - Verify data format

3. **Chatbot Not Responding**
   - Check Flask app is running on port 5001
   - Verify OpenAI API key is set
   - Check browser console for errors

### Error Messages

- **"MindsDB connection not available"**: Start MindsDB server
- **"No tide data available"**: Load tide data into MindsDB
- **"Error processing tide query"**: Check query syntax and data availability

## Advanced Usage

### Custom Queries

You can extend the chatbot by adding new query types in the `process_tide_query()` function:

```python
# Add new query patterns
elif 'tidal range' in user_message.lower():
    # Query for tidal range statistics
    query = """
    SELECT MAX(prediction) - MIN(prediction) as tidal_range
    FROM tide_predictions 
    WHERE station = 'nyc'
    """
```

### Adding New Locations

To add new tide stations:

1. Update the `locations` list in `process_tide_query()`
2. Ensure tide data exists for the new location
3. Test with sample queries

## Data Sources

The tide data comes from:
- **Simulated Tide Data**: Based on realistic tidal patterns
- **Station Coverage**: Major coastal cities in the US
- **Time Range**: Historical and future predictions
- **Update Frequency**: Real-time processing

## Integration with Other Features

The tide chatbot works alongside:
- **Flood Risk Visualization**: Interactive maps with tide overlay
- **Tide Predictions**: Detailed charts and statistics
- **CoastalDEM Analysis**: Elevation data integration

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the MindsDB integration documentation
3. Test with the provided test script
4. Check the Flask app logs for detailed error messages

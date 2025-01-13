## 🌎 AI Travel Planner Pro
An advanced AI-powered travel planning assistant that creates personalized travel itineraries using multiple specialized agents. The system leverages phidata agent framework and LLMs to handle different aspects of trip planning, from destination research to budget management.

## 🚀 Quick Start Guide

```bash
# Clone repository
git clone https://github.com/ThejanW/ai-skool.git
cd ai-skool/ai-agents/ai-travel-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # For macOS/Linux
# venv\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Add OpenAI API key to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Launch app
streamlit run agent.py
```

## 🤖 How it Works?

### 1. Destination Intelligence Agent
- Provides comprehensive destination analysis
- Researches attractions, culture, and safety
- Analyzes weather and seasonal patterns
- Suggests activities matching user interests
- Provides practical information (time zones, currency)

### 2. Travel Logistics Agent
- Plans complete travel logistics
- Recommends accommodation options with price analysis
- Organizes transportation and route planning
- Provides cost estimates and booking tips
- Optimizes for convenience and budget

### 3. Info Agent
- Researches vital information based on itineraries
- Provides up-to-date practical details
- Organizes and structures travel information
- Offers relevant tips and recommendations

### 4. Master Planner Agent
- Coordinates between specialized agents
- Creates detailed day-by-day itineraries
- Ensures comprehensive travel planning
- Maintains clear organization of information

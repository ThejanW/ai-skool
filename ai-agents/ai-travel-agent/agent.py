import streamlit as st

from textwrap import dedent

from phi.agent import Agent
from phi.model.google import Gemini
from phi.model.openai import OpenAIChat
from phi.model.ollama import Ollama
from phi.tools.googlesearch import GoogleSearch

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Travel Planner Pro",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set up the Streamlit app
st.title("AI Travel Planner Pro ✈️")
st.caption(
    "Your personal AI travel planning team that creates detailed, personalized travel itineraries with real-time data"
)

# llm = OpenAIChat(id="gpt-4o-mini")
# llm = Gemini(id="gemini-1.5-flash")
llm = Ollama(id="llama3.2")

# 1. Destination Intelligence Agent (combines destination research, activities, and safety)
destination_agent = Agent(
    name="Destination Intelligence Agent",
    role="Expert destination and activities analyst",
    model=llm,
    description=dedent(
        """You are an expert travel researcher and cultural curator specializing in comprehensive 
        destination analysis. You provide detailed information about locations, activities, 
        cultural experiences, and safety considerations."""
    ),
    instructions=[
        "Start with a GoogleSearch tool call to obtain the most relevant and up-to-date information.",

        "Provide comprehensive destination analysis including:",
        "- Major attractions, local culture, and best times to visit",
        "- Weather patterns and seasonal considerations",
        "- Local customs, cultural events, and unique experiences",
        "- Safety information and travel advisories",
        "- Activities and experiences matching user interests",
        "- Practical information (time zones, currency, customs)",
        "Format information clearly and prioritize based on user interests",
    ],
    tools=[GoogleSearch()],
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True
)

# 2. Logistics Agent (combines accommodation and transportation)
logistics_agent = Agent(
    name="Travel Logistics Agent",
    role="Expert in accommodation and transportation planning",
    model=llm,
    description=dedent(
        """You are a logistics expert specializing in accommodation and transportation planning. 
        You provide comprehensive solutions for where to stay and how to get around."""
    ),
    instructions=[
        "Start with a GoogleSearch tool call to obtain the most relevant and up-to-date information.",

        "Provide complete logistics planning including:",
        "- Accommodation options with price ranges and location analysis",
        "- Transportation options (flights, local transit, car rentals)",
        "- Route planning and transfer considerations",
        "- Cost estimates for all logistics",
        "- Booking tips and recommendations",
        "Consider budget level and practical constraints",
        "Optimize for convenience and value"
    ],
    tools=[GoogleSearch()],
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True
)

# 3. Basic Info Agent
info_agent = Agent(
    name="Info Agent",
    role="Expert in researching and providing the basic information given an itinerary",
    model=llm,
    description=dedent(
        """You are an expert specializing in researching and providing vital information and tips based on an itinerary. 
        """
    ),
    instructions=[
        "Use the provided itinerary and GoogleSearch tool call to obtain the most relevant and up-to-date information.",
        "Provide complete and well-organized answers to the user query",
    ],
    tools=[GoogleSearch()],
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True
)

# Master Travel Planner
master_planner = Agent(
    name="Master Travel Planner",
    model=llm,
    team=[destination_agent, logistics_agent],
    description="You are a comprehensive travel planner who creates detailed itineraries and manages budgets.",
    instructions=[
        "Create complete detailed well-organized travel itineraries",
        "- Coordinate with destination agent for location analysis and activities",
        "- Work with logistics agent for accommodation and transport",
        "- Create very detailed day-by-day itinerary",
        "Format everything in a clear, organized manner",
    ],
    add_datetime_to_instructions=True,
    markdown=True,
    debug_mode=True
)

# Streamlit interface
with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Where do you want to go?")
        start_date = st.date_input("Start Date")
        duration = st.number_input("Duration (days)", min_value=1, max_value=30, value=7)

    with col2:
        budget_range = st.selectbox("Budget Range",
                                    ["Budget", "Moderate", "Luxury"])
        travelers = st.number_input("Number of Travelers", min_value=1, value=2)
        interests = st.multiselect("Interests",
                                   ["Culture", "Food", "Nature", "Adventure", "Shopping", "Relaxation"])

    additional_info = st.text_area("Any additional preferences or requirements?")
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    with st.spinner("Creating your perfect travel plan..."):
        # Prepare the query with all information
        query = f"""
        Plan a trip to {destination} with the following details:
        - Dates: {start_date} for {duration} days
        - Budget Level: {budget_range}
        - Number of Travelers: {travelers}
        - Interests: {', '.join(interests)}
        Additional Information: {additional_info}
        
        - Always make sure your information is enriched with up-to-date information and relevant URLs.
        
        - Output the detailed and very well organized daily itinerary with relevant URLs and up-to-date information.
        """

        response = master_planner.run(query, stream=False)

        # Display the plan
        st.success("Your travel plan is ready!")
        st.write(response.content)

        # Add download button for the plan
        st.download_button(
            label="Download Travel Plan",
            data=str(response),
            file_name=f"travel_plan_{destination}_{start_date}.md",
            mime="text/markdown"
        )

        # Create tabs for detailed information
        tab1, tab2, tab3, tab4 = st.tabs([
            "🚗 Transportation",
            "🦺 Safety Info",
            "🧳 Packing List",
            "💰 Budget Breakdown"
        ])

        with tab1:
            st.subheader("Transportation Plan")
            transport_info = logistics_agent.run(
                f"Here's the current itinerary: {response.content}"
                "=========================================\n"
                f"Create a comprehensive transportation plan"
                f"including getting there, local transportation, and estimated costs "
                f"for {travelers} travelers."
                "ALWAYS enrich the output with up-to-date Links",
                stream=False
            )
            st.markdown(transport_info.content)

            # Add interactive transport booking links
            st.subheader("Quick Links")
            st.markdown("""
                        - [Search Flights](https://www.skyscanner.com)
                        - [Book Train Tickets](https://www.raileurope.com)
                        - [Local Transport Info](https://www.rome2rio.com)
                        """)

        with tab2:
            st.subheader("Safety Info")
            safety_info = info_agent.run(
                f"Here's the current itinerary: {response.content}"
                "=========================================\n"
                f"Provide current safety information and travel advisories"
                "ALWAYS enrich the output with up-to-date Links",
                stream=False
            )
            st.markdown(safety_info.content)

        with tab3:
            st.subheader("Packing List")
            packing_list = info_agent.run(
                f"Here's the current itinerary: {response.content}"
                "=========================================\n"
                f"Create a detailed packing list for {duration} days in {destination}, "
                f"considering the activities: {interests} and the weather during {start_date}"
                "ALWAYS enrich the output with up-to-date Links",
                stream=False
            )
            st.markdown(packing_list.content)

        with tab4:
            st.subheader("Budget Breakdown")
            budget_analysis = info_agent.run(
                f"Here's the current itinerary: {response.content}"
                "=========================================\n"
                f"Create a detailed budget breakdown for {duration} days in {destination} "
                f"for {travelers} travelers at {budget_range} level, including all expenses.",
                stream=False
            )
            st.markdown(budget_analysis.content)

            # Add interactive budget calculator
            st.subheader("Budget Calculator")
            col1, col2 = st.columns(2)
            with col1:
                accommodation_budget = st.number_input("Accommodation Budget", min_value=0)
                transport_budget = st.number_input("Transportation Budget", min_value=0)
                activities_budget = st.number_input("Activities Budget", min_value=0)
                food_budget = st.number_input("Food Budget", min_value=0)

            with col2:
                total_budget = accommodation_budget + transport_budget + activities_budget + food_budget
                st.metric("Total Budget", f"${total_budget:,.2f}")
                st.metric("Per Person", f"${total_budget / travelers:,.2f}")
                st.metric("Per Day", f"${total_budget / duration:,.2f}")

        # Add emergency contacts section
        with st.expander("🆘 Emergency Contacts"):
            st.markdown("""
                        ### Important Numbers
                        - Local Emergency: 911
                        - Nearest Embassy: [Find Embassy](https://www.embassy-worldwide.com)
                        - Travel Insurance: [Your policy number]
                        """)

        # Add a feedback section
        st.subheader("✨ Help us improve!")
        feedback = st.text_area("Share your feedback about this travel plan")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

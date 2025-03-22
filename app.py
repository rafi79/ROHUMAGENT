import streamlit as st
import requests
import json
import time

# Set page configuration
st.set_page_config(
    page_title="ROH-Ads: AI Marketing Strategy Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
GEMINI_API_KEY = "AIzaSyBFjG6kQWfrpg0Q7tcvxxQHNDl3DVW8-gA"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Initialize session state
if 'business_data' not in st.session_state:
    st.session_state.business_data = {
        "business_name": "",
        "industry": "",
        "target_audience": "",
        "marketing_goals": "",
        "budget_range": "",
        "current_challenges": ""
    }
if 'marketing_strategy' not in st.session_state:
    st.session_state.marketing_strategy = None

def generate_with_gemini(prompt):
    """Generate content using Gemini model via REST API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 4096
            }
        }
        
        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            st.error(f"API Error: {response.status_code}")
            return f"Error: {response.text}"
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return f"An error occurred: {str(e)}"

# UI Components
def sidebar():
    with st.sidebar:
        st.title("🚀 ROH-Ads")
        st.subheader("AI Marketing Strategy Assistant")
        
        st.markdown("---")
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio("Go to:", ["Business Profile", "Strategy Generator", "Campaign Planning"])
        
        st.markdown("---")
        
        # About section
        st.markdown("### About ROH-Ads")
        st.write("""
        ROH-Ads is an AI-powered marketing strategy assistant that helps businesses create effective marketing strategies.
        """)
        
        return page

def business_profile_page():
    st.header("🏢 Business Profile")
    st.write("Let's gather some information about your business to create tailored marketing strategies.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.business_data["business_name"] = st.text_input(
            "Business Name", 
            value=st.session_state.business_data["business_name"]
        )
        
        st.session_state.business_data["industry"] = st.selectbox(
            "Industry",
            options=[
                "", "E-commerce", "SaaS", "Healthcare", "Education", "Finance", 
                "Retail", "Real Estate", "Food & Beverage", "Manufacturing", "Other"
            ],
            index=0 if st.session_state.business_data["industry"] == "" else 
                  list([
                      "", "E-commerce", "SaaS", "Healthcare", "Education", "Finance", 
                      "Retail", "Real Estate", "Food & Beverage", "Manufacturing", "Other"
                  ]).index(st.session_state.business_data["industry"])
        )
        
        st.session_state.business_data["budget_range"] = st.select_slider(
            "Marketing Budget Range",
            options=["Under $1,000", "$1,000-$5,000", "$5,000-$10,000", 
                     "$10,000-$50,000", "$50,000-$100,000", "$100,000+"],
            value=st.session_state.business_data["budget_range"] if st.session_state.business_data["budget_range"] else "Under $1,000"
        )
    
    with col2:
        st.session_state.business_data["target_audience"] = st.text_area(
            "Target Audience Description",
            value=st.session_state.business_data["target_audience"],
            height=100
        )
        
        st.session_state.business_data["marketing_goals"] = st.text_area(
            "Marketing Goals",
            value=st.session_state.business_data["marketing_goals"],
            height=100
        )
    
    st.session_state.business_data["current_challenges"] = st.text_area(
        "Current Marketing Challenges",
        value=st.session_state.business_data["current_challenges"],
        height=100
    )
    
    if st.button("Save Profile"):
        if st.session_state.business_data["business_name"] and st.session_state.business_data["industry"]:
            st.success("Business profile saved successfully!")
            
            analysis_prompt = f"""
            Analyze this business profile for marketing strategy opportunities:
            Business Name: {st.session_state.business_data['business_name']}
            Industry: {st.session_state.business_data['industry']}
            Target Audience: {st.session_state.business_data['target_audience']}
            Marketing Goals: {st.session_state.business_data['marketing_goals']}
            Budget Range: {st.session_state.business_data['budget_range']}
            Challenges: {st.session_state.business_data['current_challenges']}
            
            Provide 3-5 initial marketing strategy recommendations based on this data.
            """
            
            with st.spinner("Analyzing your business profile..."):
                analysis = generate_with_gemini(analysis_prompt)
                st.session_state.profile_analysis = analysis
            
            st.subheader("Initial Analysis")
            st.write(st.session_state.profile_analysis)
        else:
            st.error("Please fill in at least the Business Name and Industry fields.")

def strategy_generator_page():
    st.header("🎯 Marketing Strategy Generator")
    
    if st.session_state.business_data["business_name"] == "":
        st.warning("Please complete your business profile first.")
        return
    
    st.write(f"Generating marketing strategies for **{st.session_state.business_data['business_name']}**")
    
    st.subheader("Strategy Focus")
    focus_areas = st.multiselect(
        "Select marketing focus areas",
        options=[
            "Social Media Marketing", "Content Marketing", "Email Marketing", 
            "Search Engine Optimization (SEO)", "Pay-Per-Click Advertising (PPC)",
            "Influencer Marketing", "Video Marketing", "Affiliate Marketing"
        ]
    )
    
    timeframe = st.radio(
        "Strategy Timeframe",
        options=["Short-term (1-3 months)", "Medium-term (3-6 months)", "Long-term (6-12 months)"]
    )
    
    competitors = st.text_area("List main competitors (if any)")
    
    if st.button("Generate Marketing Strategy"):
        if focus_areas:
            strategy_prompt = f"""
            Create a comprehensive marketing strategy for:
            Business: {st.session_state.business_data['business_name']}
            Industry: {st.session_state.business_data['industry']}
            Target Audience: {st.session_state.business_data['target_audience']}
            Goals: {st.session_state.business_data['marketing_goals']}
            Budget: {st.session_state.business_data['budget_range']}
            Challenges: {st.session_state.business_data['current_challenges']}
            
            Focus on these marketing areas: {', '.join(focus_areas)}
            Timeframe: {timeframe}
            Competitors: {competitors}
            
            Please structure the strategy with these sections:
            1. Executive Summary
            2. Market Analysis
            3. Target Audience Insights
            4. Marketing Channels & Tactics
            5. Content Strategy
            6. Budget Allocation
            7. Timeline & Implementation
            8. Success Metrics & KPIs
            
            Make the strategy specific, actionable, and tailored to their business profile.
            """
            
            with st.spinner("Generating your marketing strategy..."):
                strategy = generate_with_gemini(strategy_prompt)
                st.session_state.marketing_strategy = strategy
            
            st.subheader("Your Marketing Strategy")
            st.write(st.session_state.marketing_strategy)
            
            # Download button for the strategy
            st.download_button(
                label="Download Strategy as Text",
                data=st.session_state.marketing_strategy,
                file_name=f"{st.session_state.business_data['business_name']}_marketing_strategy.txt",
                mime="text/plain"
            )
        else:
            st.error("Please select at least one marketing focus area.")

def campaign_planning_page():
    st.header("📅 Campaign Planning")
    
    if st.session_state.marketing_strategy is None:
        st.warning("Please generate a marketing strategy first.")
        return
    
    st.subheader("Create a Marketing Campaign")
    
    campaign_name = st.text_input("Campaign Name")
    campaign_goal = st.selectbox(
        "Primary Campaign Objective",
        options=[
            "Brand Awareness", "Lead Generation", "Sales/Conversions", 
            "Customer Retention", "Product Launch", "Event Promotion"
        ]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date")
        campaign_budget = st.number_input("Campaign Budget ($)", min_value=0, step=100)
    
    with col2:
        end_date = st.date_input("End Date")
        primary_channel = st.selectbox(
            "Primary Marketing Channel",
            options=[
                "Social Media", "Email", "Content Marketing", "PPC", 
                "SEO", "Events", "Influencer Marketing"
            ]
        )
    
    campaign_description = st.text_area("Campaign Description")
    
    if st.button("Generate Campaign Plan"):
        if campaign_name and campaign_goal and campaign_description:
            campaign_prompt = f"""
            Create a detailed marketing campaign plan for:
            Business: {st.session_state.business_data['business_name']}
            Campaign Name: {campaign_name}
            Campaign Goal: {campaign_goal}
            Timeframe: {start_date} to {end_date}
            Budget: ${campaign_budget}
            Primary Channel: {primary_channel}
            Description: {campaign_description}
            
            This campaign should align with the overall marketing strategy for the business.
            
            Please include:
            1. Campaign Brief (summary, goals, KPIs)
            2. Target Audience Segments
            3. Messaging & Creative Direction
            4. Channel Strategy & Content Calendar
            5. Budget Breakdown
            6. Timeline with Key Milestones
            7. Measurement Plan
            
            Make the campaign plan specific, actionable, and provide examples of content or messaging where applicable.
            """
            
            with st.spinner("Generating your campaign plan..."):
                campaign_plan = generate_with_gemini(campaign_prompt)
            
            st.subheader("Your Campaign Plan")
            st.write(campaign_plan)
            
            # Download button for the campaign plan
            st.download_button(
                label="Download Campaign Plan",
                data=campaign_plan,
                file_name=f"{campaign_name}_campaign_plan.txt",
                mime="text/plain"
            )
        else:
            st.error("Please fill in all required fields.")

# Main application
def main():
    page = sidebar()
    
    if page == "Business Profile":
        business_profile_page()
    elif page == "Strategy Generator":
        strategy_generator_page()
    elif page == "Campaign Planning":
        campaign_planning_page()

if __name__ == "__main__":
    main()

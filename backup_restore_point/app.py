import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import json
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_AI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro')

# Email configuration
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

# Calendly configuration
CALENDLY_API_KEY = os.getenv('CALENDLY_API_KEY')
CALENDLY_BASE_URL = "https://api.calendly.com/v2"
CALENDLY_SCHEDULING_LINK = "https://calendly.com/saikiran-paramkusham09"  # Replace with your actual Calendly link

# Candidate stages
CANDIDATE_STAGES = [
    "Applied",
    "Initial Screening",
    "Technical Assessment",
    "Interview",
    "Offer",
    "Hired",
    "Rejected"
]

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
       <style>
    /* Main background */
    .stApp {
        background-color: #022e34 !important;
        color: white !important;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #70eb94 !important;
        color: #022e34 !important;
    }

    /* Make dropdown background white and text dark */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: white !important;
        color: #022e34 !important;
        border: 1px solid #022e34 !important;
        border-radius: 6px;
    }

    /* Dropdown options */
    .stSelectbox .css-1xc3v61, .stSelectbox .css-1xarl3l {
        color: #022e34 !important;
    }

    /* Header and labels */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label {
        color: #022e34 !important;
        font-weight: bold;
    }

    /* Main content text color */
    .stMarkdown, .stText {
        color: white !important;
    }

    /* Dataframe background */
    .stDataFrame {
        background-color: #022e34 !important;
        color: white !important;
    }

    /* Dataframe header */
    .stDataFrame thead {
        background-color: #022e34 !important;
        color: white !important;
    }

    /* Dataframe cells */
    .stDataFrame td {
        background-color: #022e34 !important;
        color: white !important;
    }

    /* Main content headings */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white !important;
    }

    /* Labels in main content */
    .stLabel, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: white !important;
    }

    /* Info messages */
    .stInfo {
        color: white !important;
    }

    /* Success messages */
    .stSuccess {
        color: white !important;
    }

    /* Warning messages */
    .stWarning {
        color: white !important;
    }

    /* Error messages */
    .stError {
        color: white !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        color: white !important;
    }

    /* Tab content */
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }

    /* Selected tab */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: white !important;
        background-color: #70eb94 !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: #70eb94 !important;
        color: black !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: bold !important;
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #5cd67d !important;
    }

    /* Button focus effect */
    .stButton > button:focus {
        box-shadow: 0 0 0 2px #022e34 !important;
    }
</style>
    """, unsafe_allow_html=True)

def send_calendly_invite(candidate_email, candidate_name, job_title):
    """Send Calendly invite to candidate"""
    try:
        # Create scheduling link with pre-filled information
        scheduling_link = f"{CALENDLY_SCHEDULING_LINK}?email={'saikiran.paramkusham09@gmail.com'}&name={candidate_name}&job={job_title}"
        
        # Send email with Calendly link
        email_subject = f"Interview Invitation - {job_title}"
        email_body = f"""
        <html>
        <body>
        <h2>Interview Invitation</h2>
        <p>Dear {candidate_name},</p>
        <p>We are pleased to invite you for an interview for the position of <b>{job_title}</b>.</p>
        <p>Please click the link below to schedule your interview:</p>
        <p><a href="{scheduling_link}">Schedule Interview</a></p>
        <br>
        <p>Best regards,<br>Recruitment Team</p>
        </body>
        </html>
        """
        
        return send_email(candidate_email, email_subject, email_body)
    except Exception as e:
        st.error(f"Error sending Calendly invite: {e}")
        return False

def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = 'saikiran.paramkusham09@gmail.com'
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def load_json_data(file_path):
    """Load data from JSON file with proper encoding"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.info("Please run 'python fetch_data.py' to fetch and save the data.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error loading {file_path}: {e}")
        return None

def save_json_data(file_path, data):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def get_resume_text(resume_url):
    """Get resume text from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(resume_url, headers=headers)
        response.raise_for_status()
        # For now, we'll just return a placeholder since we can't actually parse PDFs
        return "Resume content placeholder"
    except requests.RequestException as e:
        st.error(f"Error fetching resume: {e}")
        return None

def assess_candidate(candidate, job_posting):
    """Assess candidate using Gemini"""
    try:
        prompt = f"""
        Please assess this candidate for the following job posting:
        
        Job Posting:
        {job_posting}
        
        Candidate Information:
        {candidate}
        
        Please provide:
        1. A suitability score (0-100)
        2. Key strengths
        3. Areas for improvement
        4. Overall recommendation
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error assessing candidate: {e}")
        return None

def update_candidate_stage(candidates_data, candidate_id, new_stage, comments=None):
    """Update candidate stage and add comments"""
    try:
        for candidate in candidates_data['candidates']:
            if candidate['id'] == candidate_id:
                # Update stage
                candidate['current_stage'] = new_stage
                
                # Add stage history if not exists
                if 'stage_history' not in candidate:
                    candidate['stage_history'] = []
                
                # Add new stage entry
                stage_entry = {
                    'stage': new_stage,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'comments': comments
                }
                candidate['stage_history'].append(stage_entry)
                
                return True
        return False
    except Exception as e:
        st.error(f"Error updating candidate stage: {e}")
        return False

def main():
    # Apply custom CSS
    apply_custom_css()
    
    st.title("Ideals Recruitment System")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Candidate Assessment", "Applicant Tracking"])
    
    # Load data from JSON files
    data_dir = Path('data')
    postings_data = load_json_data(data_dir / 'postings.json')
    candidates_data = load_json_data(data_dir / 'candidates.json')
    
    if not postings_data or not candidates_data:
        st.error("Failed to load data. Please ensure data files exist in the 'data' directory.")
        return
    
    # Convert to DataFrames
    postings_df = pd.DataFrame(postings_data['postings'])
    candidates_df = pd.DataFrame(candidates_data['candidates'])
    
    with tab1:
        # Sidebar for job posting selection
        st.sidebar.header("Job Posting")
        selected_posting = st.sidebar.selectbox(
            "Select a job posting",
            options=postings_df['text'].tolist()
        )
        
        # Main content
        st.header("Candidate Assessment")
        
        # Display selected job posting
        if selected_posting:
            posting_details = postings_df[postings_df['text'] == selected_posting].iloc[0]
            st.subheader("Job Details")
            st.write(f"**Title:** {posting_details['text']}")
            st.write(f"**Department:** {posting_details['categories']['department']}")
            st.write(f"**Location:** {posting_details['categories']['location']}")
            st.write(f"**Description:** {posting_details['content']['description']}")
        
        # Candidate selection
        selected_candidate = st.selectbox(
            "Select a candidate",
            options=candidates_df['name'].tolist()
        )
        
        if selected_candidate:
            candidate_details = candidates_df[candidates_df['name'] == selected_candidate].iloc[0]
            st.subheader("Candidate Details")
            st.write(f"**Name:** {candidate_details['name']}")
            st.write(f"**Email:** {candidate_details['emails'][0]}")
            st.write(f"**Location:** {candidate_details['location']}")
            st.write(f"**Tags:** {', '.join(candidate_details['tags'])}")
            
            # Show current stage
            current_stage = candidate_details.get('current_stage', 'Applied')
            st.write(f"**Current Stage:** {current_stage}")
            
            # Stage management
            col1, col2 = st.columns(2)
            with col1:
                new_stage = st.selectbox(
                    "Move to Stage",
                    options=CANDIDATE_STAGES,
                    index=CANDIDATE_STAGES.index(current_stage) if current_stage in CANDIDATE_STAGES else 0
                )
            
            comments = st.text_area("Recruiter Comments", height=100)
            
            if st.button("Update Stage"):
                if update_candidate_stage(candidates_data, candidate_details['id'], new_stage, comments):
                    # Save updated data
                    if save_json_data(data_dir / 'candidates.json', candidates_data):
                        st.success(f"Successfully moved {candidate_details['name']} to {new_stage} stage")
                        
                        # Send appropriate notifications based on stage
                        if new_stage == "Interview":
                            # Send Calendly invite for interview stage
                            if send_calendly_invite(
                                candidate_details['emails'][0],
                                candidate_details['name'],
                                posting_details['text']
                            ):
                                st.success("Calendly interview invite sent successfully")
                            else:
                                st.warning("Failed to send Calendly interview invite")
                        else:
                            # Send regular status update email
                            email_subject = f"Application Status Update - {posting_details['text']}"
                            email_body = f"""
                            <html>
                            <body>
                            <h2>Application Status Update</h2>
                            <p>Dear {candidate_details['name']},</p>
                            <p>Your application for the position of <b>{posting_details['text']}</b> has been updated.</p>
                            <p>Current Stage: <b>{new_stage}</b></p>
                            <br>
                            <p>Recruiter Comments:</p>
                            <p>{comments}</p>
                            <br>
                            <p>Best regards,<br>Recruitment Team</p>
                            </body>
                            </html>
                            """
                            
                            if send_email(candidate_details['emails'][0], email_subject, email_body):
                                st.success("Email notification sent successfully")
                            else:
                                st.warning("Failed to send email notification")
                else:
                    st.error("Failed to update candidate stage")
            
            # Assessment button
            if st.button("Assess Candidate"):
                with st.spinner("Assessing candidate..."):
                    resume_text = get_resume_text(candidate_details['resume_url'])
                    
                    if resume_text:
                        assessment = assess_candidate(
                            {
                                'name': candidate_details['name'],
                                'location': candidate_details['location'],
                                'tags': candidate_details['tags'],
                                'resume': resume_text
                            },
                            {
                                'title': posting_details['text'],
                                'department': posting_details['categories']['department'],
                                'location': posting_details['categories']['location'],
                                'description': posting_details['content']['description']
                            }
                        )
                        
                        if assessment:
                            st.subheader("Assessment Results")
                            st.write(assessment)
                            st.write(f"Assessment performed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            time.sleep(1)
    
    with tab2:
        st.header("Applicant Tracking")
        
        # Add filters
        col1, col2 = st.columns(2)
        with col1:
            selected_job = st.selectbox(
                "Filter by Job Posting",
                options=["All"] + postings_df['text'].tolist()
            )
        
        with col2:
            selected_stage = st.selectbox(
                "Filter by Stage",
                options=["All"] + CANDIDATE_STAGES
            )
        
        # Create a DataFrame for tracking
        tracking_data = []
        for candidate in candidates_data['candidates']:
            tracking_data.append({
                'Name': candidate['name'],
                'Email': candidate['emails'][0],
                'Job Applied': candidate.get('job_applied', 'Not specified'),
                'Current Stage': candidate.get('current_stage', 'Applied'),
                'Last Updated': candidate.get('stage_history', [{}])[-1].get('timestamp', 'Never'),
                'Comments': candidate.get('stage_history', [{}])[-1].get('comments', '')
            })
        
        tracking_df = pd.DataFrame(tracking_data)
        
        # Apply filters
        if selected_job != "All":
            tracking_df = tracking_df[tracking_df['Job Applied'] == selected_job]
        if selected_stage != "All":
            tracking_df = tracking_df[tracking_df['Current Stage'] == selected_stage]
        
        # Display tracking table
        st.dataframe(
            tracking_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Add stage statistics
        st.subheader("Stage Statistics")
        stage_counts = tracking_df['Current Stage'].value_counts()
        
        # Create a bar chart
        st.bar_chart(stage_counts)
        
        # Add stage transition history
        st.subheader("Stage Transition History")
        selected_candidate_tracking = st.selectbox(
            "Select a candidate to view history",
            options=tracking_df['Name'].tolist()
        )
        
        if selected_candidate_tracking:
            candidate_history = next(
                (c['stage_history'] for c in candidates_data['candidates'] 
                 if c['name'] == selected_candidate_tracking),
                []
            )
            
            if candidate_history:
                history_df = pd.DataFrame(candidate_history)
                st.dataframe(
                    history_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No stage transition history available for this candidate.")

if __name__ == "__main__":
    main() 
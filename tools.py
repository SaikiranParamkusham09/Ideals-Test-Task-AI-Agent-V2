import streamlit as st
import requests
import google.generativeai as genai
import json
from datetime import datetime
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
CALENDLY_SCHEDULING_LINK = "https://calendly.com/saikiran-paramkusham09"


class UIAgent:
    @staticmethod
    def apply_agent_theme():
        """Apply custom CSS styling for the UI agent"""
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
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: white !important;
        }

        /* Labels in main content */
        .stLabel, .stSelectbox label, .stTextInput label, 
        .stTextArea label {
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


class CommunicationAgent:
    @staticmethod
    def coordinate_interview(candidate_email, candidate_name, job_title):
        """Coordinate interview scheduling through Calendly"""
        try:
            scheduling_link = (
                f"{CALENDLY_SCHEDULING_LINK}?email={'saikiran.paramkusham09@gmail.com'}"
                f"&name={candidate_name}&job={job_title}"
            )
            
            email_subject = f"Interview Invitation - {job_title}"
            email_body = f"""
            <html>
            <body>
            <h2>Interview Invitation</h2>
            <p>Dear {candidate_name},</p>
            <p>We are pleased to invite you for an interview for the position of 
               <b>{job_title}</b>.</p>
            <p>Please click the link below to schedule your interview:</p>
            <p><a href="{scheduling_link}">Schedule Interview</a></p>
            <br>
            <p>Best regards,<br>Recruitment Team</p>
            </body>
            </html>
            """
            
            return CommunicationAgent.dispatch_message(
                candidate_email, email_subject, email_body
            )
        except Exception as e:
            st.error(f"Error coordinating interview: {e}")
            return False

    @staticmethod
    def dispatch_message(to_email, subject, body):
        """Dispatch email message through SMTP"""
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
            st.error(f"Error dispatching message: {e}")
            return False


class DataAgent:
    @staticmethod
    def perceive_data(file_path):
        """Perceive and load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
            st.info(
                "Please run 'python fetch_data.py' to fetch and save the data."
            )
            return None
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON from {file_path}: {e}")
            return None
        except Exception as e:
            st.error(f"Unexpected error perceiving data: {e}")
            return None

    @staticmethod
    def persist_state(file_path, data):
        """Persist state to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"Error persisting state: {e}")
            return False


class AssessmentAgent:
    @staticmethod
    def analyze_resume(resume_url):
        """Analyze resume content from URL"""
        try:
            response = requests.get(resume_url)
            if response.status_code == 200:
                return response.text
            else:
                st.error(f"Error fetching resume: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error analyzing resume: {e}")
            return None

    @staticmethod
    def evaluate_candidate(candidate, job_posting):
        """Evaluate candidate using AI"""
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
            st.error(f"Error evaluating candidate: {e}")
            return None


class WorkflowAgent:
    @staticmethod
    def transition_candidate(candidate_id, new_stage):
        """Transition candidate to new stage"""
        try:
            candidates = DataAgent.perceive_data('data/candidates.json')
            if not candidates:
                return False
                
            # Handle both dictionary and list data structures
            if isinstance(candidates, dict) and 'candidates' in candidates:
                candidate_list = candidates['candidates']
            else:
                candidate_list = candidates
                
            # Find the candidate in the list
            for candidate in candidate_list:
                if candidate['id'] == candidate_id:
                    candidate['current_stage'] = new_stage
                    candidate['stage_history'] = candidate.get('stage_history', [])
                    candidate['stage_history'].append({
                        'stage': new_stage,
                        'timestamp': datetime.now().isoformat(),
                    })
                    
                    # Save the updated data
                    if isinstance(candidates, dict):
                        return DataAgent.persist_state('data/candidates.json', candidates)
                    else:
                        return DataAgent.persist_state('data/candidates.json', {'candidates': candidate_list})
                        
            return False
        except Exception as e:
            st.error(f"Error transitioning candidate: {e}")
            return False

    @staticmethod
    def process_candidate(candidate_id):
        """Process candidate through workflow"""
        try:
            candidates = DataAgent.perceive_data('data/candidates.json')
            if not candidates:
                return False
                
            # Handle both dictionary and list data structures
            if isinstance(candidates, dict) and 'candidates' in candidates:
                candidate_list = candidates['candidates']
            else:
                candidate_list = candidates
                
            # Find the candidate
            for candidate in candidate_list:
                if candidate['id'] == candidate_id:
                    job_posting = DataAgent.perceive_data(
                        'data/postings.json'
                    )
                    if job_posting and 'postings' in job_posting:
                        for posting in job_posting['postings']:
                            if posting['id'] == candidate.get('job_id'):
                                assessment = AssessmentAgent.evaluate_candidate(
                                    candidate, posting
                                )
                                if assessment:
                                    candidate['assessment'] = assessment
                                    if isinstance(candidates, dict):
                                        return DataAgent.persist_state(
                                            'data/candidates.json', candidates
                                        )
                                    else:
                                        return DataAgent.persist_state(
                                            'data/candidates.json',
                                            {'candidates': candidate_list}
                                        )
            return False
        except Exception as e:
            st.error(f"Error processing candidate: {e}")
            return False 
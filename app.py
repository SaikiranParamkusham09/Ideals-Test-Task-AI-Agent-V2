import streamlit as st
import pandas as pd
import time
from datetime import datetime
from pathlib import Path
from tools import (
    UIAgent,
    CommunicationAgent,
    DataAgent,
    AssessmentAgent,
    WorkflowAgent
)

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

def main():
    # Apply custom CSS
    UIAgent.apply_agent_theme()
    
    st.title("Ideals Recruitment System")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Candidate Assessment", "Applicant Tracking"])
    
    # Load data from JSON files
    data_dir = Path('data')
    postings_data = DataAgent.perceive_data(data_dir / 'postings.json')
    candidates_data = DataAgent.perceive_data(data_dir / 'candidates.json')
    
    if not postings_data or not candidates_data:
        st.error(
            "Failed to load data. Please ensure data files exist in the 'data' "
            "directory."
        )
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
            posting_details = postings_df[
                postings_df['text'] == selected_posting
            ].iloc[0]
            st.subheader("Job Details")
            st.write(f"**Title:** {posting_details['text']}")
            st.write(
                f"**Department:** {posting_details['categories']['department']}"
            )
            st.write(
                f"**Location:** {posting_details['categories']['location']}"
            )
            st.write(
                f"**Description:** {posting_details['content']['description']}"
            )
        
        # Candidate selection
        selected_candidate = st.selectbox(
            "Select a candidate",
            options=candidates_df['name'].tolist()
        )
        
        if selected_candidate:
            candidate_details = candidates_df[
                candidates_df['name'] == selected_candidate
            ].iloc[0]
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
                    index=(
                        CANDIDATE_STAGES.index(current_stage) 
                        if current_stage in CANDIDATE_STAGES else 0
                    )
                )
            
            comments = st.text_area("Recruiter Comments", height=100)
            
            if st.button("Update Stage"):
                # Get the candidate's ID from the DataFrame
                candidate_id = str(candidate_details['id'])  # Ensure ID is string
                
                if WorkflowAgent.transition_candidate(
                    candidate_id, new_stage
                ):
                    # Save updated data
                    if DataAgent.persist_state(
                        data_dir / 'candidates.json', candidates_data
                    ):
                        st.success(
                            f"Successfully moved {candidate_details['name']} to "
                            f"{new_stage} stage"
                        )
                        
                        # Send appropriate notifications based on stage
                        if new_stage == "Interview":
                            # Send Calendly invite for interview stage
                            if CommunicationAgent.coordinate_interview(
                                candidate_details['emails'][0],
                                candidate_details['name'],
                                posting_details['text']
                            ):
                                st.success(
                                    "Calendly interview invite sent successfully"
                                )
                            else:
                                st.warning("Failed to send Calendly interview invite")
                        else:
                            # Send regular status update email
                            email_subject = (
                                f"Application Status Update - "
                                f"{posting_details['text']}"
                            )
                            email_body = f"""
                            <html>
                            <body>
                            <h2>Application Status Update</h2>
                            <p>Dear {candidate_details['name']},</p>
                            <p>Your application for the position of 
                               <b>{posting_details['text']}</b> has been updated.</p>
                            <p>Current Stage: <b>{new_stage}</b></p>
                            <br>
                            <p>Recruiter Comments:</p>
                            <p>{comments}</p>
                            <br>
                            <p>Best regards,<br>Recruitment Team</p>
                            </body>
                            </html>
                            """
                            
                            if CommunicationAgent.dispatch_message(
                                candidate_details['emails'][0],
                                email_subject,
                                email_body
                            ):
                                st.success("Email notification sent successfully")
                            else:
                                st.warning("Failed to send email notification")
                else:
                    st.error("Failed to update candidate stage")
            
            # Assessment button
            if st.button("Assess Candidate"):
                with st.spinner("Assessing candidate..."):
                    resume_text = AssessmentAgent.analyze_resume(
                        candidate_details['resume_url']
                    )
                    
                    if resume_text:
                        assessment = AssessmentAgent.evaluate_candidate(
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
                            st.write(
                                f"Assessment performed at: "
                                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            )
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
                'Last Updated': (
                    candidate.get('stage_history', [{}])[-1].get('timestamp', 'Never')
                ),
                'Comments': (
                    candidate.get('stage_history', [{}])[-1].get('comments', '')
                )
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
                st.info(
                    "No stage transition history available for this candidate."
                )

if __name__ == "__main__":
    main() 
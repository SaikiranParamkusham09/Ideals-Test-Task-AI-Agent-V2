# Recruitment System Prototype

A Streamlit-based recruitment system that uses AI to assess candidates based on their resumes and job postings.

## Features

- View and select job postings
- Browse candidate applications
- AI-powered candidate assessment using Google's Gemini
- Rate-limited API calls to prevent overuse
- Simple and intuitive user interface
- Local JSON storage to prevent API rate limiting

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Fetch the initial data (only needs to be done once):
```bash
python fetch_data.py
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Usage

1. Select a job posting from the sidebar
2. Choose a candidate from the dropdown menu
3. Click "Assess Candidate" to get an AI-powered assessment
4. Review the assessment results including:
   - Suitability score
   - Key strengths
   - Areas for improvement
   - Overall recommendation

## Data Storage

The application stores job postings and candidate data locally in JSON files:
- `data/postings.json`: Contains all job posting information
- `data/candidates.json`: Contains candidate information including resume URLs

## API Endpoints

The application uses the following mock API endpoints:
- Job Postings: `https://fd4c61a1-d161-4de2-92e4-50fd468a8e82.mock.pstmn.io/postings`
- Candidates: `https://fd4c61a1-d161-4de2-92e4-50fd468a8e82.mock.pstmn.io/candidates`
- Resumes: `https://f000.backblazeb2.com/file/BPA-Candidates/`

## Rate Limiting

The application includes basic rate limiting to prevent overuse of the Gemini API. A 1-second delay is added between assessments.

## Note

This is a prototype system. The resume parsing functionality is currently a placeholder and would need to be implemented with proper PDF parsing capabilities in a production environment. 
# Agentic Recruitment System

A modern, AI-powered recruitment system that leverages agent-based architecture to automate and streamline the hiring process.

## Features

### Core Capabilities
- **Autonomous Decision Making**: AI-powered candidate evaluation and decision making
- **Automated Communication**: Intelligent email and interview scheduling
- **Interactive UI**: Streamlit-based user interface for seamless interaction
- **State Management**: Persistent storage of candidate data and system state
- **Multi-stage Workflow**: Comprehensive recruitment pipeline management

### Agent-Based Architecture
- **UIAgent**: Manages user interface and interaction
- **DataAgent**: Handles data persistence and retrieval
- **AssessmentAgent**: Evaluates candidates and makes decisions
- **WorkflowAgent**: Orchestrates the recruitment process
- **CommunicationAgent**: Manages candidate communications

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini AI
- **Data Storage**: JSON-based state management
- **Email Integration**: SMTP for automated communications
- **Calendar Integration**: Calendly for interview scheduling

## 📋 Prerequisites

- Python 3.8+
- Google Gemini AI API key
- SMTP server credentials
- Calendly API access

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/SaikiranParamkusham09/Ideals.git
cd Ideals
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following:
```
GEMINI_API_KEY=your_gemini_api_key
EMAIL_USER=your_email
EMAIL_PASSWORD=your_email_password
CALENDLY_API_KEY=your_calendly_api_key
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the UI at `http://localhost:8501`

## 📁 Project Structure

```
Ideals/
├── app.py                 # Main application entry point
├── tools.py              # Agent implementations and utilities
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
├── solution_architecture.txt  # System architecture documentation
├── technical_implementation.txt  # Technical implementation details
├── implementation_plan.txt      # Project implementation roadmap
└── technical_presentation.txt   # Technical presentation materials
```

## 🔄 Workflow

1. **Candidate Entry**: New candidates are added through the UI
2. **AI Assessment**: System evaluates candidates using Gemini AI
3. **Decision Making**: Automated decisions based on assessment
4. **Communication**: Automated email notifications and interview scheduling
5. **State Updates**: Real-time status updates and tracking

## 🎯 Key Features

### Autonomous Decision Making
- AI-powered candidate evaluation
- Automated stage transitions
- Intelligent decision recommendations

### Communication Automation
- Automated email notifications
- Interview scheduling via Calendly
- Status updates and reminders

### Data Management
- Persistent JSON storage
- Real-time state updates
- Comprehensive candidate tracking

## 🔮 Future Enhancements

1. **Advanced AI Capabilities**
   - Enhanced candidate evaluation
   - Predictive analytics
   - Automated interview feedback

2. **Integration Expansions**
   - Additional communication channels
   - Advanced scheduling features
   - Analytics dashboard

3. **UI Improvements**
   - Enhanced visualization
   - Mobile responsiveness
   - Custom themes

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Saikiran Paramkusham

## 🙏 Acknowledgments

- Google Gemini AI team
- Streamlit community
- All contributors and supporters 


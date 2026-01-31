# Website Scanner

AI-Powered Website Localization Analysis Tool

Website Scanner analyzes websites for localization readiness, quality gaps, and internationalization signals. This standalone tool was extracted from the Lead Machine / GitHub Dossier BDR tool.

## Features

- **AI-Powered Analysis**: Uses Google Gemini to analyze websites based on natural language prompts
- - **Localization Scoring**: Calculates localization readiness score (0-100)
  - - **Tech Stack Detection**: Identifies frameworks, i18n libraries, and CMS platforms
    - - **Quality Assessment**: Evaluates SEO, accessibility, performance, and mobile readiness
     
      - ## Quick Start
     
      - 1. Clone the repository
        2. 2. Install dependencies: `pip install -r requirements.txt`
           3. 3. Set environment variable: `export GEMINI_API_KEY=your_api_key`
              4. 4. Run the app: `python app.py`
                 5. 5. Visit `http://localhost:5000`
                   
                    6. ## Usage
                   
                    7. Enter a website URL and a natural language prompt describing what you want to analyze. Examples:
                    8. - "Identify all internationalization and localization features"
                       - - "Extract all contact information"
                         - - "Find pricing information and subscription tiers"
                          
                           - ## Tier Classification
                          
                           - - **Tier 1 (Global Leader)**: 10+ locales, enterprise infrastructure
                             - - **Tier 2 (Active Expansion)**: 3-9 locales, actively expanding
                               - - **Tier 3 (Going Global)**: 1-2 locales with i18n signals
                                 - - **Tier 4 (Not Yet Global)**: No localization signals detected
                                  
                                   - ## License
                                  
                                   - MIT License

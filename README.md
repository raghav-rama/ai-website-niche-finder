# ai-website-niche-finder
find niches of websites

## Setup

1. Clone the repo

2. Create a virtual environment using the following command:

   - On Windows:
     ```
     python -m venv venv
     ```

   - On macOS/Linux:
     ```
     python3 -m venv venv
     ```

3. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install Flask and other required dependencies:

   - On Windows:
     ```
     pip install -r requirements.txt
     ```

   - On macOS/Linux:
     ```
     pip3 install -r requirements.txt
     ```

5. Start Dev Server

   - On Windows(PowerShell):
     ```
     $env:FLASK_APP = "aboip1"
     $env:FLASK_ENV = "development"
     flask run
     ```

   - On macOS/Linux:
     ```
     export FLASK_APP=aboip1
     export FLASK_ENV=development
     flask run
     ```
     
6. Setup OpenAI API Key

   - make a file name `.env` in the project root dir
   - add the following lines
   ```
   OPENAI_API_KEY=YOUR-OPENAI-API-KEY
   APP_SECRET_KEY=ANY-RANDOM-KEY
   ```
   - APP_SECRET_KEY is required by WTForms and flask_session


# Smart Pet Translator

Cute, playful pet-sound translator demo built with Streamlit.

## Run locally
1. `git clone <your-repo-url>`
2. `cd smart_pet_translator`
3. (Optional) Create virtual environment:
   `python -m venv venv && source venv/bin/activate`
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run the app:
   `streamlit run app.py`

## Deploy online
Push this repo to GitHub. Then go to [Streamlit Cloud](https://streamlit.io/cloud), click “New app”, connect the repo, and deploy.

## Notes
- The current app uses demo training sounds (sine waves with noise).  
- For a real translator, replace them with actual labeled pet recordings.

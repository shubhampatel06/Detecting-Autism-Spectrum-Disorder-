# Detecting Autism Spectrum Disorder

Small Flask app that uses a trained Keras model to classify images as Autistic or Non-Autistic.

Prereqs
- Python 3.8+
- Create a virtualenv: python -m venv venv
- Install dependencies: pip install -r requirements.txt

Run locally
1. Activate venv:
   - Windows (PowerShell): .\venv\Scripts\Activate.ps1
2. Start the app:
   - python app.py

Notes
- Large datasets, models, and uploaded images are in `.gitignore` and not included in the repo.
- Add your trained model file to `models/trained_model.h5` if needed.

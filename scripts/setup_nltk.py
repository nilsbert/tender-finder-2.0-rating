import nltk
try:
    nltk.download('punkt')
    nltk.download('snowball_data')
    print("✅ NLTK resources downloaded successfully.")
except Exception as e:
    print(f"❌ Error downloading NLTK resources: {e}")

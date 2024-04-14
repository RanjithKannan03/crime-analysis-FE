from flask import Flask, request, jsonify
import os
import PyPDF2
from gensim import corpora, similarities, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import requests
from transformers import pipeline
from googlesearch import search
from textblob import TextBlob
from bs4 import BeautifulSoup
import openai
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Function to preprocess text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])
    # Tokenize and remove stopwords
    tokens = simple_preprocess(text)
    tokens = [token for token in tokens if token not in STOPWORDS]
    return tokens

# Function to compute similarity between two texts
def compute_similarity(input_text, stored_text):
    dictionary = corpora.Dictionary([stored_text])
    corpus = [dictionary.doc2bow(input_text)]
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary))
    sims = index[tfidf[dictionary.doc2bow(stored_text)]]
    return sims[0]

# Function to find the most similar PDF among stored PDFs
def find_most_similar(input_pdf_path, stored_pdf_folder):
    input_text = preprocess_text(extract_text_from_pdf(input_pdf_path))
    most_similar_pdf = None
    highest_similarity = -1

    for filename in os.listdir(stored_pdf_folder):
        if filename.endswith(".pdf"):
            stored_pdf_path = os.path.join(stored_pdf_folder, filename)
            stored_text = preprocess_text(extract_text_from_pdf(stored_pdf_path))
            similarity = compute_similarity(input_text, stored_text)
            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_pdf = stored_pdf_path

    return most_similar_pdf

@app.route('/generate_image', methods=['POST'])
def generate_image():
    url = "https://api.limewire.com/api/image/generation"
    
    # Extract the prompt from the JSON data sent in the request
    prompt = request.json.get('prompt', '')
    
    # Set up payload and headers
    payload = {
        "prompt": prompt,
        "aspect_ratio": "1:1"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": "Bearer lmwr_sk_29rZYc5LdA_yKwChwUETjnklI63VEcyEEBfbjUZE8eGhPpwk"
    }
    
    # Send a POST request to the Limewire API
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return jsonify(data), 200
    else:
        return jsonify({"error": "Failed to generate image"}), response.status_code

@app.route('/compare_pdfs', methods=['POST'])
def compare_pdfs():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    print("hello")

    input_pdf_path = "static/tmp/input_pdf.pdf"  # Temporary path to store the uploaded PDF
    file.save(input_pdf_path)
    print("hello")
    stored_pdf_folder = os.path.join(app.static_folder, "stored_pdfs")
    #stored_pdf_folder = "stored_pdfs"  # Folder containing stored PDFs

    most_similar_pdf = find_most_similar(input_pdf_path, stored_pdf_folder)
    if most_similar_pdf:
        return jsonify({"most_similar_pdf": most_similar_pdf}), 200
    else:
        return jsonify({"error": "No similar PDF found"}), 404
    
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

def split_text_into_chunks(text, max_chunk_length=512):
    """
    Splits the input text into smaller chunks.

    Args:
        text (str): The input text to be split.
        max_chunk_length (int): Maximum length of each chunk.

    Returns:
        list: List of text chunks.
    """
    chunks = []
    words = text.split()
    current_chunk = ""
    
    for word in words:
        if len(current_chunk) + len(word) < max_chunk_length:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def summarize_pdf(pdf_path):
    """
    Summarizes the content of a PDF document.

    Args:
        pdf_path: Path to the PDF document.

    Returns:
        str: Summary of the PDF content.
    """
    # Open the PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Extract text from each page
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split text into smaller chunks
        text_chunks = split_text_into_chunks(text)

        # Generate summary for each chunk and concatenate them
        summaries = []
        for chunk in text_chunks:
            input_length = len(chunk.split())
            max_length = min(2 * input_length, 512)  # Adjust the multiplier as needed
            summary = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        
    return "\n".join(summaries)

@app.route('/summarize_pdf', methods=['POST'])
def summarize_pdf_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    input_pdf_path = "static/tmp/input_pdf.pdf"  # Temporary path to store the uploaded PDF
    file.save(input_pdf_path)

    summary = summarize_pdf(input_pdf_path)
    if summary:
        return jsonify({"summary": summary}), 200
    else:
        return jsonify({"error": "Failed to summarize PDF"}), 500
    
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Function to retrieve recent posts
def retrieve_recent_posts(query, num_posts=5):
    search_results = search(query, num=num_posts)
    posts = []
    for i, result in enumerate(search_results, start=1):
        parts = result.split(' - ')
        if len(parts) >= 2:
            title = parts[0]
            snippet = parts[1]
        else:
            title = result
            snippet = ''
        posts.append({
            'title': title,
            'snippet': snippet,
            'sentiment': analyze_sentiment(title + ' ' + snippet)
        })
    return posts

@app.route('/recent_posts', methods=['GET'])
def get_recent_posts():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    recent_posts = retrieve_recent_posts(query)
    return jsonify(recent_posts)

def scrape_instagram_posts(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', type="text/javascript")
        for script_tag in script_tags:
            if script_tag.string and script_tag.string.startswith('window._sharedData'):
                shared_data = script_tag.string.split(' = ', 1)[1].rstrip(';')
                data = json.loads(shared_data)
                if 'entry_data' in data and 'ProfilePage' in data['entry_data']:
                    edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
                    captions = [edge['node']['edge_media_to_caption']['edges'][0]['node']['text'] for edge in edges if edge['node']['edge_media_to_caption']['edges']]
                    return captions
                else:
                    return None
        return None
    else:
        return None

@app.route('/instagram_posts', methods=['GET'])
def get_instagram_posts():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400
    
    captions = scrape_instagram_posts(username)
    if captions:
        return jsonify({"captions": captions}), 200
    else:
        return jsonify({"error": "Failed to retrieve Instagram posts"}), 500

api_key = "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"
openai.api_key = api_key

# Global variable to store input JSON data
input_data = {}

# Function to generate answers using GPT-3
def generate_answer(question, data):
    context = json.dumps(data)
    prompt = f"Question: {question}\nContext: {context}\nAnswer:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route('/set_data', methods=['POST'])
def set_data():
    global input_data
    request_data = request.json
    if not request_data or 'data' not in request_data:
        return jsonify({"error": "Invalid request data"}), 400
    
    input_data = request_data['data']
    return jsonify({"message": "Input data set successfully"})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    global input_data
    if not input_data:
        return jsonify({"error": "Input data not set. Please set the input data first."}), 400
    
    request_data = request.json
    if not request_data or 'question' not in request_data:
        return jsonify({"error": "Invalid request data"}), 400
    
    question = request_data['question']
    # answer = generate_answer(question, input_data)
    answer="Maximum number of crimes in Vijaynagar"
    return jsonify({"answer": answer})

class CrimePredictor:
    def __init__(self):
        # Initialize model and data
        self.model = RandomForestClassifier()
        self.data = self._generate_fictional_data()

    def _generate_fictional_data(self):
        # Generate fictional crime data
        data = {
            "Location": ["MG Road", "Koramangala", "Malleswaram", "Jayanagar", "Whitefield",
                         "Electronic City", "Indiranagar", "Banashankari", "Marathahalli", "Yelahanka"],
            "Time_of_Day": ["Night", "Evening", "Night", "Morning", "Afternoon",
                            "Evening", "Morning", "Night", "Afternoon", "Morning"],
            "Weather": ["Clear", "Rainy", "Clear", "Snowy", "Clear",
                        "Rainy", "Clear", "Rainy", "Clear", "Snowy"],
            "Demographics": ["High population density", "Low income", "Medium income", "High income", "Mixed demographics",
                             "High population density", "Medium income", "Low income", "Mixed demographics", "High income"],
            "Crime_Type": ["Robbery", "Burglary", "Assault", "Theft", "Vandalism",
                           "Fraud", "Drug Offense", "Kidnapping", "Arson", "Homicide"]
        }
        return pd.DataFrame(data)

    def train_model(self):
        # Train the model using generated crime data
        X = pd.get_dummies(self.data.drop(columns=["Crime_Type"]))
        y = self.data["Crime_Type"]
        self.model.fit(X, y)
        # Save feature names for later use during prediction
        self.feature_names = X.columns.tolist()

    def predict_crime(self, new_data):
        # Predict the type of crime based on new data
        # Ensure new data has the same features as training data
        new_data_encoded = pd.get_dummies(new_data)
        new_data_encoded = new_data_encoded.reindex(columns=self.feature_names, fill_value=0)
        crime_prediction = self.model.predict(new_data_encoded)
        return crime_prediction

    def suggest_response_plan(self, crime_type, location, time_of_day, weather, demographics):
        # Generate a response plan based on the type of crime, location, time of day, weather, and demographics
        response = ""
        patrol_units = 0
        
        if crime_type == "Robbery":
            patrol_units = 3
            response += f"To prevent robberies in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Install surveillance cameras and alarm systems to deter criminals.\n"
            response += "3. Implement neighborhood watch programs to encourage community vigilance.\n"
            response += "4. Conduct regular safety audits and improve street lighting in dark or secluded areas.\n"
            response += "5. Collaborate with local businesses to implement cash-handling protocols and security measures.\n"
        elif crime_type == "Burglary":
            patrol_units = 2
            response += f"To prevent burglaries in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Strengthen physical security measures such as locks, bars, and reinforced doors and windows.\n"
            response += "3. Encourage residents to secure valuables and install home security systems.\n"
            response += "4. Establish a community watch program and promote neighbor communication.\n"
            response += "5. Conduct regular property inspections and maintain landscaping to reduce hiding spots.\n"
            response += "6. Work with local law enforcement to organize crime prevention workshops and trainings.\n"
        elif crime_type == "Assault":
            patrol_units = 2
            response += f"To prevent assaults in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during evening and night hours.\n"
            response += "2. Increase police presence in public spaces and popular gathering areas.\n"
            response += "3. Educate the community about conflict resolution and de-escalation techniques.\n"
            response += "4. Establish safe walk programs and provide escorts for vulnerable individuals.\n"
            response += "5. Install surveillance cameras and emergency call boxes in high-traffic areas.\n"
            response += "6. Train businesses and staff in recognizing and responding to potentially violent situations.\n"
        elif crime_type == "Theft":
            patrol_units = 2
            response += f"To prevent thefts in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Implement access control measures and restrict entry to authorized personnel only.\n"
            response += "3. Utilize theft-deterrent technologies such as RFID tags and security alarms.\n"
            response += "4. Conduct background checks on employees and contractors with access to sensitive areas.\n"
            response += "5. Enhance inventory management and surveillance systems to monitor stock movements.\n"
            response += "6. Collaborate with law enforcement to create crime prevention awareness campaigns.\n"
        elif crime_type == "Vandalism":
            patrol_units = 1
            response += f"To prevent vandalism in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol unit to patrol the area during night hours.\n"
            response += "2. Increase community engagement and promote ownership of public spaces.\n"
            response += "3. Implement graffiti removal programs and maintain clean and well-kept surroundings.\n"
            response += "4. Install security fencing and barriers to protect vulnerable targets.\n"
            response += "5. Organize youth outreach programs and provide constructive recreational activities.\n"
            response += "6. Work with local artists and community groups to create positive murals and public art installations.\n"
        elif crime_type == "Fraud":
            patrol_units = 1
            response += f"To prevent fraud in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol unit to patrol the area during night hours.\n"
            response += "2. Educate residents about common fraud schemes and how to identify fraudulent activities.\n"
            response += "3. Promote secure online practices such as using strong passwords and avoiding suspicious links.\n"
            response += "4. Provide resources for reporting and addressing suspected fraud incidents.\n"
            response += "5. Partner with financial institutions to enhance fraud detection and prevention measures.\n"
            response += "6. Conduct regular audits and reviews of financial transactions and accounts.\n"
        elif crime_type == "Drug Offense":
            patrol_units = 2
            response += f"To prevent drug offenses in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Increase surveillance and monitoring of known drug trafficking routes and hotspots.\n"
            response += "3. Conduct community outreach and education programs to raise awareness of the dangers of drug use.\n"
            response += "4. Collaborate with schools and youth organizations to provide drug prevention programs.\n"
            response += "5. Enhance cooperation with neighboring jurisdictions and federal agencies to disrupt drug supply chains.\n"
            response += "6. Implement diversion programs and provide access to treatment and rehabilitation services for individuals struggling with addiction.\n"
        elif crime_type == "Kidnapping":
            patrol_units = 2
            response += f"To prevent kidnappings in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Implement strict access controls and security measures in schools, daycare centers, and public spaces frequented by children.\n"
            response += "3. Educate children and parents about personal safety and abduction prevention strategies.\n"
            response += "4. Establish neighborhood watch programs and encourage community vigilance.\n"
            response += "5. Enhance coordination with law enforcement agencies to investigate and disrupt human trafficking networks.\n"
            response += "6. Provide resources and support for victims of domestic violence and family abduction cases.\n"
        elif crime_type == "Arson":
            patrol_units = 1
            response += f"To prevent arson in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol unit to patrol the area during night hours.\n"
            response += "2. Implement fire prevention and safety measures in buildings and public facilities.\n"
            response += "3. Conduct regular fire drills and training sessions for residents and employees.\n"
            response += "4. Increase lighting and visibility in outdoor areas to deter arsonists.\n"
            response += "5. Establish partnerships with fire departments and emergency responders for rapid intervention.\n"
            response += "6. Encourage reporting of suspicious behavior and provide rewards for information leading to arson prevention.\n"
        elif crime_type == "Homicide":
            patrol_units = 3
            response += f"To prevent homicides in {location} during {time_of_day}, especially in areas with {demographics}, consider taking the following preventive measures:\n"
            response += f"1. Deploy {patrol_units} patrol units to patrol the area during night hours.\n"
            response += "2. Strengthen community-police relations and establish trust through regular engagement and dialogue.\n"
            response += "3. Implement violence prevention programs targeting at-risk youth and individuals involved in gang activities.\n"
            response += "4. Enhance mental health services and crisis intervention programs to address underlying issues contributing to violent behavior.\n"
            response += "5. Improve access to educational and economic opportunities in underserved communities to reduce social disparities.\n"
            response += "6. Invest in community revitalization efforts and create safe and inclusive public spaces for recreation and social interaction.\n"

        return response

predictor = CrimePredictor()
predictor.train_model()

@app.route('/predict_crime', methods=['POST'])
def predict_crime():
    data = request.json
    new_situation = pd.DataFrame(data)
    crime_prediction = predictor.predict_crime(new_situation)
    return jsonify({"crime_prediction": crime_prediction[0]}), 200

@app.route('/suggest_response_plan', methods=['POST'])
def suggest_response_plan():
    data = request.json
    crime_type = data["crime_type"]
    location = data["location"]
    time_of_day = data["time_of_day"]
    weather = data["weather"]
    demographics = data["demographics"]
    response_plan = predictor.suggest_response_plan(crime_type, location, time_of_day, weather, demographics)
    return jsonify({"response_plan": response_plan}), 200

@app.route('/',methods=["GET"])
def home():
    return jsonify({"message":"hello"}),200

if __name__ == '__main__':
    app.run(debug=True)

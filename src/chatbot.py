
import random

class DrAIChatbot:
    def __init__(self):
        self.responses = {
            "greeting": [
                "Hello! I am Dr. AI. How can I assist you with lung cancer information today?",
                "Greetings. I'm here to provide information about lung health and our screening process.",
                "Hi there. I can answer questions about symptoms, risk factors, or how this system works."
            ],
            "symptom": [
                "Common symptoms of lung cancer include persistent cough, chest pain, shortness of breath, coughing up blood, fatigue, and unexplained weight loss.",
                "If you are experiencing wheezing, new or changing cough, or hoarseness, these can be early warning signs. Please consult a doctor immediately.",
                "Symptoms vary, but look out for: chronic cough, respiratory infections that keep coming back, and shortness of breath."
            ],
            "risk": [
                "The biggest risk factor is smoking tobacco. Other risks include exposure to radon, asbestos, second-hand smoke, and family history.",
                "Smoking causes about 90% of lung cancer cases. Quitting smoking significantly lowers your risk over time.",
                "Age is also a factor; most people diagnosed are 65 or older. Environmental pollutants can also contribute."
            ],
            "prevention": [
                "The best way to prevent lung cancer is not to smoke and to avoid second-hand smoke.",
                "Test your home for radon levels. Avoid carcinogens like asbestos and silica dust at work.",
                "Eat a diet full of fruits and vegetables and exercise regularly to support your immune system."
            ],
            "about": [
                "I am Dr. AI, a virtual assistant integrated into the OncoPredict system. My goal is to provide supportive information.",
                "This system uses a Random Forest Machine Learning model to assess risk based on your clinical data.",
                "I am a simulated AI assistant designed to help navigate this application and provide general medical context."
            ],
            "accuracy": [
                "Our current machine learning model has an accuracy of approximately 75-80% based on historical data.",
                "Please note: My predictions are for screening purposes only and do NOT replace a diagnosis by a qualified medical professional.",
                "The system is designed to flag high-risk patients for further investigation by a radiologist."
            ],
            "default": [
                "I'm not sure I understand. You can ask me about 'symptoms', 'risks', 'prevention', or 'accuracy'.",
                "I'm still learning. Could you rephrase that? Try asking about lung cancer signs or how the model works.",
                "I don't have an answer for that specific query yet. Please consult a medical professional for personalized advice."
            ]
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        if any(word in user_input for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.responses["greeting"])
        
        elif any(word in user_input for word in ["symptom", "sign", "feel", "cough", "pain"]):
            return random.choice(self.responses["symptom"])
        
        elif any(word in user_input for word in ["risk", "cause", "smoke", "tobacco", "age"]):
            return random.choice(self.responses["risk"])
        
        elif any(word in user_input for word in ["prevent", "avoid", "stop", "healthy"]):
            return random.choice(self.responses["prevention"])
            
        elif any(word in user_input for word in ["who are you", "what is this", "about", "system"]):
            return random.choice(self.responses["about"])
            
        elif any(word in user_input for word in ["accuracy", "precise", "correct", "trust"]):
            return random.choice(self.responses["accuracy"])
            
        else:
            return random.choice(self.responses["default"])

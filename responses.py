from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "sup"):
        return "Hey! How's it going?" 

    if user_message in ("who are you", "who are you?"):
        return "I am a bot to match you to a roomate that you will benefit from."
    
    if user_message in ("sleep"):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return str("Goodnight! It is currently " + date_time)

    else:
        return "I do not understand you."
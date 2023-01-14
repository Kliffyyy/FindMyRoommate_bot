from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text)
    # print(user_message)

    if "hi" or "hello" or "sup" in user_message:
        return "Hey! How's it going?" 

    elif "who are you" or "who are you?" or "what are you" or "what are you?" in user_message:
        return "I am a bot to match you to a roomate that you will benefit from."
    
    elif "sleep" in user_message:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return str("Goodnight! It is currently " + date_time)

    else:
        return "I do not understand you."
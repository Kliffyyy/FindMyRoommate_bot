from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()
    print(user_message)

    hi = ["hello","hi","sup"]
    who = ["who are you?","who are you"]
    sleep = ["sleep"]

    if user_message in hi:
        return "Hey! How's it going?" 

    elif user_message in who:
        return "I am a bot to match you to a roommate that you will benefit from."
    
    elif user_message in sleep:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return str("Goodnight! It is currently " + date_time)

    else:
        return "I do not understand you."

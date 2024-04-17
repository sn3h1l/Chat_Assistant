from openai import OpenAI

class Start_Bot:
    def __init__(self,key):
        client = OpenAI(api_key=key)
    def user_intent(self,client):
        #pre-made assistants
        assistantid="asst_FIJGSUt6F0hxGv8oWDyF8wTa"
        thread_id="thread_VEsXxk4YQkOJMoxnJPBntL87"

        start_bot_data={"start_bot_id":"asst_C2RXcKzpvGjFoynyw6YEo9tR","thread_start_bot":"thread_eh1B3hCcoZyfzHWrzwnrBZUK"}
        intent_bot_data={"intent_bot_id":"asst_FIJGSUt6F0hxGv8oWDyF8wTa","thread_intent_bot":"thread_VEsXxk4YQkOJMoxnJPBntL87"}
        combined_id={**start_bot_data,**intent_bot_data} #unpacking to save

        filename='id_data.txt'
        with open(filename, 'w') as text_file:
            for key, value in combined_id.items():
                text_file.write(f"{key}:{value}\n")

        message =client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content="I want to know more about indian government."
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistantid
        )
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status=="completed":
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                latest_message = messages.data[0]
                text = latest_message.content[0].text.value
                output_text=text
                break;

        target_intent=""
        sentence = output_text
        split_point = "Your main intent is to"
        if split_point in sentence:
            first_part = sentence.split(split_point)[0].strip()
            second_part = sentence.split(split_point)[1].strip()
            target_intent=second_part
        return target_intent



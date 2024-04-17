from openai import OpenAI

class Target_Bot:

    def __init__(self,key,target_intent,filename,follow_up_question):
        client=OpenAI(api_key=key)

    def create_new_bot(self,intent_string,client,retrieval_filname):
        name=f"{intent_string}_bot"
        retrieval_file = client.files.create(
            file=open(retrieval_filname,'rb'),
            purpose='assistants',
        )
        target_assistant = client.beta.assistants.create(
            name=name,
            instructions=f"You are an insightful and knowledgeable assistant that helps to {intent_string} and also helps in any other issues related to the same.",
            tools=[{"type": "retrieval"}, {"type": "code_interpreter"}],
            model="gpt-3.5-turbo-16k",
            file_ids=[retrieval_file.id]
        )
        new_bot_id=target_assistant.id
        new_bot_thread = client.beta.threads.create()

        #saving_ids
        combined_id_data={"new_bot_id":new_bot_id,"thread_new_bot":new_bot_thread}
        filename = 'id_data.txt'
        with open(filename, 'w') as text_file:
            for key, value in combined_id_data.items():
                text_file.write(f"{key}:{value}\n")

        return new_bot_id,new_bot_thread

    def revert(self,client,assistant_id,thread_id,follow_up_question):

        if thread_id==None :
            new_thread=client.beta.threads.create()
            thread_id=new_thread.id

        if follow_up_question==None:
            return "Hey!! how can I help??"

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=follow_up_question
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                latest_message = messages.data[0]
                reply = latest_message.content[0].text.value
                break;
        return reply

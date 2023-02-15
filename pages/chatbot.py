import streamlit as st
from streamlit_chat import message 
import openai
import datetime
import re
import pandas as pd
import nltk
import time
from nltk.sentiment import SentimentIntensityAnalyzer
conversation=list()
st.subheader("N'hésitez pas à prendre contact avec votre manager👋")
nltk.downloader.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def probleme_detection(conversation):
    conversation=conversation+'\nProblème mentionné:'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=open_file('probleme.txt').replace('<<block>>',conversation),
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    message = response.choices[0].text
    return message.strip()


def end_conversation(conversation):
    conversation=conversation+'\nterminée :'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=open_file('end_conversation.txt').replace('<<block>>',conversation),
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
        )
    message = response.choices[0].text
    return message.strip()
    


def action_detection(conversation):
    conversation=conversation+'\nAction fabriquée :'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=open_file('Action.txt').replace('<<block>>',conversation),
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
        )
    message = response.choices[0].text
    return message.strip()





#def end_conversation(response):
#    scores = sia.polarity_scores(response)
#    if scores['compound'] > 0.5:
#        st.success("The chatbot has helped the user and the conversation can be ended.")
#        st.exit()


log_df = pd.DataFrame(columns=['date', 'duration', 'problem', 'action'])



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key ="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"
# Create a function to generate responses from GPT-3
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=250,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )
    message = completions.choices[0].text
    return message.strip()
# Create a function to show user interaction with chatbot
#st.set_page_config(page_title="Chatbot Logs", page_icon=":guardsman:", layout="wide")
#st.title("N'hésitez pas à prendre contact avec votre manager👋")
start_time = datetime.datetime.now()   
if 'generated' not in st.session_state:
    st.session_state['generated']=[]
if 'past' not in st.session_state:
    st.session_state['past']=[]
def get_text():
    input_text=st.text_input("Collaborateur :",key="input")
    return input_text

#first_message=generate_response("Bonjour")
#st.session_state.past.append("")
#st.session_state.generated.append('Manager:'+first_message)



with st.form('form',clear_on_submit=True):
    user_input=get_text()
    submitted=st.form_submit_button('Envoyer')


if  submitted and user_input: 
    read_f = open('Historique.txt','r')
    output_f = open('Historique.txt','a')
    text=read_f.read()
    conversation.append(text)
    conversation.append('Collaborateur :%s'%user_input)
    output_f.write('Collaborateur :%s'%user_input+'\n')
    read_f = open('Historique.txt','r')
    read_f.close()
    text_block='\n'.join(conversation)
    prompt = open_file('Conversation1.txt').replace('<<block>>',text_block)
    prompt=prompt+'\nManager:'
    output=generate_response(prompt)
    conversation.append('Manager:%s'%output+'\n')
    output_f.write('Manager:%s'%output+'\n')
    #store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append('Manager:'+output)
    text_blockk='\n'.join(conversation)
    print(text_blockk)
    output_file = open('logs.txt','a')
    output_file.write(text_blockk)
    output_file.close()

    if(end_conversation(text_blockk)=="True"):
        text_file = open("logs.txt", "r")
        text_blockk=text_file.read()
        time.sleep(8)
        st.success(output, icon="✅")
        st.write("----------Problème mentionné---------------")
        st.write(probleme_detection(text_blockk))
        st.write("----------Action fabriqué---------------")
        st.write(action_detection(text_blockk))
        #st.warning("Chatbot stopped.")
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        log_df.loc[len(log_df)] = [start_time.strftime("%Y-%m-%d %H:%M:%S"), str(duration), probleme_detection(text_blockk),action_detection(text_blockk)]
        log_df.to_csv('log.csv',mode='a', index=False, header=False)
        time.sleep(8)
        open('logs.txt', 'w').close()
        open('Historique.txt', 'w').close()
        st.stop()

    if st.session_state['generated']:
        for i  in range(len(st.session_state['generated'])-1,-1,-1):
            message(st.session_state['generated'][i],key=str(i))
            message(st.session_state['past'][i],is_user=True,key=str(i)+'_User')
       
           
            


reset_files = st.button("Reset files")
if reset_files:
    open('logs.txt', 'w').close()
    open('Historique.txt', 'w').close()



def display_log():
    with open("interactions.txt", "r") as f:
        log = f.read()
    st.write("---Interaction Log---")
    st.write(log)




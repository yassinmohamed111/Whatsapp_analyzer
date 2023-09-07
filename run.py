import pandas as pd
import arabic_reshaper
import bidi.algorithm
from arabic_reshaper import arabic_reshaper


import matplotlib.pyplot as plt


#exttract your whatsapp groupchat data
#run switch() and pass to it the path of the data and the name of the new csv file
def switch(chat_data_file , csvname) :

    with open(chat_data_file, "r", encoding="utf-8") as file:
        chat_list = []

        for line in file:
            parts = line.strip().split(" - ")
            if len(parts) >= 2:
                date_time = parts[0].strip()
                name_message = parts[1].split(": ")
                if len(name_message) >= 2:
                    name = name_message[0].strip()
                    message = name_message[1].strip()
                    chat_list.append([date_time, name, message])

        df = pd.DataFrame(chat_list, columns=['Date/Time', 'Name', 'Message'])

    chats = df.to_csv(f"{csvname}.csv" , index = False)
    
    return chats



#if first time using add your char text file and use switch()
#switch takes ex. :  switch('chat_file_path' , 'name_of_new_csv')
#newchat = pd.read_csv("name_of-new_csv.csv")s
#


chats = pd.read('addhere the csv file')



#pd.set_option("display.max_colwidth" , None)



def nameSwitch():
   
    user_names = chats["Name"].drop_duplicates()
    print(user_names)
    person = input("Please enter name from the above list: ")
    return person

    


#get count of messages of everyone
def getMessageCount():
   name =  nameSwitch()
   person  = chats[chats["Name"] == name ]
   

   count = pd.value_counts(person["Message"]).sum()
   print(f"{name} sent:" , count , "messages")
   return person
    




#save count of messages 
#dont run or use
def save():
    person = getMessageCount()
    count = pd.value_counts(person["Message"]).sum()
    name = person["Name"].head(1).values[0]
    info = [name, count]
    df_info = pd.DataFrame([info], columns=["Name", "MessageCount"])

    try:
       
        existing_df = pd.read_csv("stats_shabab_is.csv")
       
        updated_df = pd.concat([existing_df, df_info], ignore_index=True)
        updated_df.sort_values(by="MessageCount" , ascending=False , inplace=True )
    except FileNotFoundError:
        
        updated_df = df_info
        updated_df.sort_values(by="MessageCount" , ascending=False , inplace=True)

    updated_df.to_csv("stats_shabab_is.csv", index=False)
    





def searchByMessage():
    message = input("Please enter the message you want: ")
    
    textarab = arabic_reshaper.reshape(message)
    textar = bidi.algorithm.get_display(textarab)
    mesgret = chats[chats['Message'].astype(str).str.contains(textar, case=False, na=False)]
    count =  pd.value_counts(mesgret["Message"]).sum()
    print(mesgret)
    print(f"the count of {message} is :" , count)
    return mesgret, message , count



#return date entered and dataframe of the messages sent in this time
def searchByDate():
    
    date = input("please enter the date in this format - >(12/06/2022)")
    dateret = chats[chats['Date/Time'].astype(str).str.contains(date, case=False)]
    count =  pd.value_counts(dateret["Message"]).sum()
    print(dateret)
    print(f"the count of messages of this date {date} is :", count)
    return dateret , date



def inputperson(num):
        person = []
        for i in range (num) :
                x= nameSwitch()
                person.append(x)

        return person


#get messages of specific person
def getMessagesOfperson(number) :
     persons = inputperson(number)
     chats_indexed = chats.set_index("Name")
     personschat = chats_indexed.loc[persons]
     count = pd.value_counts(personschat["Message"]).sum()
     print(personschat)
     print("count of messages is : " , count)
     return personschat



#get a specific messages sent from specific users
def specific_users_message(number) :
     person = getMessagesOfperson(number)
     message = input("please enter the message u want :")
     mesgret = person[person['Message'].astype(str).str.contains(message, case=False)]
     count =  pd.value_counts(mesgret["Message"]).sum()
    
     #print(mesgret)
     print("the count of this message :" , count)
     return mesgret



      
#get pie chart and count of specific message and the prop to all messages
def getpieofSearched():
    messages = searchByMessage()

    alll = pd.value_counts(messages[0]["Name"])
    print(alll)
    prop = (alll / alll.sum()) * 100
    labels = alll.index  #chatgpt helped me in this line
    allcount = pd.value_counts(chats["Message"]).sum()
    props = (messages[2]/allcount)*100
    rounded_number = format(props , ".2f")
    plt.pie(prop, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f" ({messages[1]}) was sent ({messages[2]} times) and the prop is ({rounded_number}%) of all messages")
    custom_labels = [f'{label}: {count} {messages[1]} was sent' for label, count in zip(labels, alll)]
    plt.legend(custom_labels ,  loc = "right" )
    plt.axis('equal')
    plt.show()

#get the pie chart and count of messages in a specific date
def piechartDate():
     messages = searchByDate()
     alll = pd.value_counts(messages[0]["Name"])
     prop = (alll / alll.sum()) * 100
     labels = alll.index
     plt.pie(prop, labels=labels, autopct='%1.1f%%', startangle=140)
     allcount = pd.value_counts(chats["Message"]).sum()
     props = (messages[2]/allcount)*100
     rounded_number = format(props , ".2f")
     plt.title(f"in the date ({messages[1]}) the count of messages were sent is ({messages[2]}) and the prop is ({rounded_number}%)  of all messages")
     custom_labels = [f'{label}: {count} messages were sent' for label, count in zip(labels, alll)]
     plt.legend(custom_labels ,  loc = "lower left" )
     plt.axis('equal')
     plt.show()


#save links only in a csv
def getlinks() :
     links = chats[chats['Message'].astype(str).str.contains("https", case=False, na=False)]
     links.to_csv("linksOnly.csv" , index=False)











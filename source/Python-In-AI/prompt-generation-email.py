to = input("Email recipient: ")
subject = input("Enter email subject: ")
body = input("Enter email body: ")
 
prompt = f"""
Create a draft email to {to} with the subject "{subject}" and the following body:
{body}
Make it professional and concise.
"""
print(prompt)
 
 
client = input("Client Name: ")
 
prompt2 = f"""
Write a professional follow-up email
to {client}
regarding project discussion.
"""
 
print(prompt2)
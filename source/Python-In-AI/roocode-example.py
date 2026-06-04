while True:
   question = input("You: ")
   if question == "exit":
       break
   elif "hello" in question.lower():
       print("Bot: Hi!")
   else:
       print("Bot: I am still learning.")
stop_words = ["am","is","are","the","a"]
text = "I am learning Python and the codes are really simple and it is a easy language to learn."
tokens = text.split()
# for word in tokens:
#    if word not in stop_words:
#        print(word)
       
if "easy" in text.lower():
   print("Positive")
elif "tough" in text.lower():
   print("Negative")
else:
   print("Neutral")
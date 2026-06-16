review = input("Enter movie review: ")
positive_words = ["good", "great", "excellent", "amazing", "wonderful"]
negative_words = ["bad", "terrible", "awful", "horrible", "worst"]

review_lower = review.lower()
if any(word in review_lower for word in positive_words) and any(word in review_lower for word in negative_words):
    print("Neutral")
elif any(word in review_lower for word in positive_words):
    print("Positive")
elif any(word in review_lower for word in negative_words):
    print("Negative")
else:
    print("No analysis possible")
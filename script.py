import requests
import nltk
import collections
import pickle
import tkinter as tk
from tkinter import messagebox


# Create a GUI window
root = tk.Tk()
root.title("SPAM EMAIL CHECKER")
root.geometry("600x500")
root.attributes('-topmost', True)
root.resizable(False, False)
root.config(bg="white")
root.iconbitmap("icon.ico")

# Define the email entry and big textbox with scrollbar and attach them to the root window using pack add height of 10 lines
email = tk.Text(root, height=20, width=50, font=("Calibri", 12), wrap="word", relief="solid", bd=1)
email_scroll = tk.Scrollbar(root, command=email.yview)
email_scroll.pack(side="right", fill="y", expand=False, anchor="e", padx=(0, 5))
# allow horizontal scrolling
email.config(wrap="none")
email.config(yscrollcommand=email_scroll.set)
email.pack()
# add margin to the text box
email.config(padx=10, pady=10)
# add placeholder text
email.insert("1.0", "Enter your email here...")
# on focus clear the placeholder text
email.bind("<FocusIn>", lambda args: email.delete("1.0", "end-1c"))
# on focus out if the text box is empty add the placeholder text
email.bind("<FocusOut>", lambda args: email.insert("1.0", "Enter your email here..."))
# add horizontal scroll bar and attach it to the text box
email_scroll = tk.Scrollbar(root, command=email.xview, orient="horizontal")
email_scroll.pack(side="bottom", fill="x", expand=False, anchor="s", padx=(10, 0))
email.config(xscrollcommand=email_scroll.set)

# add a spacer label
spacer_label= tk.Label(root, text="", bg="white")
spacer_label.pack()

#check if nltk data is present 
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    #download it to the the project folder
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')




# Download the model file and save it locally
model_path = "model.pkl"
# check if the model file is present
try:
    open(model_path, "rb")
except FileNotFoundError:
    model_url = "https://github.com/adithyapaib/spamEmailClassification/raw/main/model.pkl"
    open(model_path, "wb").write(requests.get(model_url).content)

# Create sets of stop words and most common words
stop_words = set(nltk.corpus.stopwords.words('english')) - {'not', 'no'}
most_common_words = set([word for word, freq in collections.Counter(stop_words).most_common(10)])


def preprocess_sentence(sentence, lemmatizer):
    tokens = [lemmatizer.lemmatize(w.lower())
              for w in nltk.word_tokenize(sentence) if w.lower() not in stop_words]
    return [w for w in tokens if w not in most_common_words]


def check_spam(input_data, root):
    if not input_data or len(input_data) < 15:
        root.title("SPAM EMAIL CHECKER")
        return messagebox.showerror("Error", "Please enter a valid email!")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    lemmatizer = nltk.WordNetLemmatizer()
    features = dict(collections.Counter(preprocess_sentence(input_data, lemmatizer)))
    if model.classify(features) == 1:
        root.title("SPAM EMAIL CHECKER")
        return messagebox.showerror("Information", "SPAM EMAIL!")
    return messagebox.showinfo("Information", "HAM EMAIL!")




check_button = tk.Button(root, text="Check", command=lambda: check_spam(email.get("1.0", "end-1c"), root), font=("Calibri", 12))
check_button.config(padx=10, pady=10)
check_button.config(width=10, height=1)

check_button.pack()
root.mainloop()
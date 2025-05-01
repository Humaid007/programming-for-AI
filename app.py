from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        text = request.form.get("input_text")
        if text.strip() == "":
            summary = "Please enter some text to summarize."
        elif len(text.split(".")) < 3:
            summary = "Please enter a longer paragraph with more sentences."
        else:
            try:
                parser = PlaintextParser.from_string(text, Tokenizer("english"))
                summarizer = LsaSummarizer()
                summary_sentences = summarizer(parser.document, 3)
                summary = " ".join(str(sentence) for sentence in summary_sentences)
                if not summary.strip():
                    summary = "Summary could not be generated. Try entering more text."
            except Exception as e:
                summary = f"An error occurred: {e}"
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)


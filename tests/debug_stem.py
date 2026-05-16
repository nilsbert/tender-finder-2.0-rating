from nltk.stem.snowball import SnowballStemmer
de = SnowballStemmer("german")
en = SnowballStemmer("english")

words = ["Strategy", "Strategies", "Beratung", "Beratungen"]
for w in words:
    print(f"{w} -> DE: {de.stem(w)}, EN: {en.stem(w)}")

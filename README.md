# Data-Analytics
Data analytics and Big Data 


this python based search engine to extract the unique keywords using TF*IDF techniques. This application is capable to analysis the given text and extracts the meaningful and unique keywords through the submitted document.

The model is capable of analysis thousands of thousand records in a minute.

 

This model with some modification can be used in areas concerning data protection and communication monitoring process.  Using this model, the computer can monitor all transactions and extract those records including unique keywords, or list of keywords has been selected with client.  You may take advantages of this model to extract the pattern through the encrypted data or understanding the keywords have been hidden using steganography techniques.

What is the TF*IDF equation:

Term Frequency-Inverse document frequency is a mathematical statistic that is intended to reflect how important a word is to a document in a collection or corpus. It is often used as a weighting factor in searches of information retrieval, text mining, and user modeling. The TF–IDF value increases proportionally to the number of times a word appears in the document and is offset by the number of documents in the corpus that contain the word, which helps to adjust for the fact that some words appear more frequently in general. TF–IDF is one of the most popular term-weighting schemes today; more than 80% of text-based recommender systems in digital libraries use TF_IDF.

 

How to Calculate the TF*IDF rank:

·       TF: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is often divided by the document length as a way of normalization:

 

TF(t) = (Number of times term (t) appears in a document) / (Total number of terms in the document).

 

·       IDF: Inverse Document Frequency, which measures how important a term is. While computing TF, all terms are considered equally important. However, it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance. Thus we need to weigh down the frequent terms while scaling up the rare ones, by computing the following:

 

IDF(t) = Natural log(Total number of documents / Number of documents contains term (t)).

 

How to run: Python start.py sample.txt,

How to Exit: the process would be close by typing (end-of-file: eof) “ eof”.

·       The attached files are a sample database (word.db), sample text (sample.txt), and my codes (start.py).

·       The sample file contains a set of 5000 recodes from the Book catalog.

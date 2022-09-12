import pandas as pd
import re
import sys


# 1) PREPARING AND PREPROCESSING OF THE DATASET
"""Load dataset, a file, indicate what separator 
the file uses and the names of the columns as a list)"""

sms_spam = pd.read_csv('dataset_spam_ham.txt', sep='\t', header=None, names=['Label', 'SMS'])

""" Know the dimensions of the table of the file cvs (rows, columns) """

rows, columns = sms_spam.shape
# Preprocess the data
sms_spam['SMS'] = sms_spam['SMS'].str.replace(r'\W', " ").str.lower()

# 2) SPLITTING THE DATASET
# Randomize the dataset
data_random = sms_spam.sample(frac=1, random_state=1)
train_test_index = round(len(data_random) * 0.8)
train_set = data_random[:train_test_index].reset_index(drop=True)
test_set = data_random[train_test_index:].reset_index(drop=True)
# Split the sentences into a list of tokens
train_set["SMS"] = train_set["SMS"].str.split()

# CREATING A VOCABULARY OF UNIQUE WORDS
vocabulary = set([word for sms in train_set['SMS'] for word in sms])
word_counts_per_sms = {unique_word: [0] * len(train_set['SMS']) for unique_word in vocabulary}
for index, sms in enumerate(train_set['SMS']):
    for word in sms:
        word_counts_per_sms[word][index] += 1
# Create a dataframe where each key corresponds to a column name and the values are the rows in the column
word_counts = pd.DataFrame(word_counts_per_sms)
# Merge the previous table to have labels, sms and the counts for each vocab word in the same table
# axis=1 add columns | axis=0 add rows
train_set_clean = pd.concat([train_set, word_counts], axis=1)

# PROPORTION OF SPAM AND HAM FOR CALCULATING PROBABILITIES
# Isolating spam and ham messages to make mini tables (dataframes) with only spam or ham sms
spam_messages = train_set_clean[train_set_clean['Label'] == 'spam']
ham_messages = train_set_clean[train_set_clean['Label'] == 'ham']
# P(Spam) and P(Ham) count(spams) / count(total n° of sms)
p_spam = len(spam_messages) / len(train_set_clean)
p_ham = len(ham_messages) / len(train_set_clean)

# n_words_per_spam_message returns a table with the length of each sms
n_words_per_spam_message = spam_messages['SMS'].apply(len)
# Sum over the entire column to get the total number of words in spam
n_spam = n_words_per_spam_message.sum()

# Idem n_words_per_ham_message
n_words_per_ham_message = ham_messages['SMS'].apply(len)
n_ham = n_words_per_ham_message.sum()
# n_vocabulary
n_vocabulary = len(vocabulary)
# Laplace smoothing to avoid the problem of zero probability in Naive Bayes algorithm
alpha = 1

# CALCULATING PARAMETERS
# Initiate parameters
# Create dictionaries where each key is a word with value 0 for each word in vocab
parameters_spam = {unique_word: 0 for unique_word in vocabulary}
parameters_ham = {unique_word: 0 for unique_word in vocabulary}

# Calculate parameters
for word in vocabulary:
    """Sum up all of the values in the column to get the number of times this particular word appeared in spam """

    n_word_spam = spam_messages[word].sum()

    """ Even if word appears 0 times (so n_word_given_spam=0) in spam and only appears in ham sms,
    it will have a count of 1 (the value of alpha) """

    p_word_spam = (n_word_spam + alpha) / (n_spam + alpha * n_vocabulary)
    parameters_spam[word] = p_word_spam
    # Same for ham
    """Sum up all of the values in the column to get the number of times this particular word appeared in ham """

    n_word_ham = ham_messages[word].sum()
    p_word_ham = (n_word_ham + alpha) / (n_ham + alpha * n_vocabulary)
    parameters_ham[word] = p_word_ham


# CLASSIFYING


def classify(message: str) -> str:
    """From a message with type string, predict what class it belongs to."""

    # Preprocess the massage
    message = re.sub('\W', ' ', message)
    message = message.lower().split()
    # The probability spam|sms is proportional to P(spam) * P(word1|spam) * P(word2|spam) *...
    # Put in place P(spam) and P(ham)
    p_spam_message = p_spam
    p_ham_message = p_ham
    # For each word, look up its probability in parameters dictionaries and multiply by it.
    # If the word has not been seen and is a new word (ie. isnt in 1 of the dicts) then skip over it basically.
    for word in message:
        if word in parameters_spam:
            p_spam_message *= parameters_spam[word]
        if word in parameters_ham:
            p_ham_message *= parameters_ham[word]
    # If ham is higher
    if p_ham_message > p_spam_message:
        return 'This is a HAM ;)'
    # If spam is higher
    elif p_spam_message > p_ham_message:
        return 'This is a  SPAM !!!'
    # Too close to decide by Artificial Intellect, we need the Human
    else:
        return 'Equal proabilities, have a human classify this!'


"""Create a column called predicted which has the models prediction for each test sms"""

# Apply classify function to the column of sms in the test set
test_set['predicted'] = test_set['SMS'].apply(classify)
# Correct predictions : columns Predicted and Label are the same
correct = (test_set['predicted'] == test_set['Label'])
# Sum over all the rows where the condition is True to get count(correct predictions)
correct = correct.sum()
# Count the accuracy
accuracy = correct / test_set.shape[0]

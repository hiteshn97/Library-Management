import os
import re
import numpy as np

from gensim.models import Word2Vec
from gensim.corpora.dictionary import Dictionary

#from nltk.stem import WordNetLemmatizer

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense,Dropout

import multiprocessing
from random import shuffle

maxlen=300
window_size=5
batch_size=32
n_epoch=2
input_length=300

#Stopwords
stop_words=[]
file=open("stopwords.txt",encoding='utf-8').read().split('\n')
stop_words.append(file)

#Accessing the dataset and appending them to lists, also preprocessing at the same time
def init_lists(folder):
    var=1
    a_list=[]
    
    file_list=os.listdir(folder)
    for file in file_list:
        print(str(var)+'\n')
        var=var+1
        f=open(os.path.join(folder,file),encoding="utf-8")
        text=f.read()
        words=re.split(r'\s+',re.sub(r'[,/\-!?.|lI।"\]\[<>br]', ' ',text).strip())
        if words not in stop_words:      #StopWord Removal
            a_list.append(words)
    f.close()
    return a_list


pos_train=init_lists("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\train\\positive")
neg_train=init_lists("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\train\\negative")
pos_test=init_lists("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\test\\positive")
neg_test=init_lists("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\test\\negative")
all_reviews=pos_train+neg_train+pos_test+neg_test

shuffle(pos_train)
shuffle(neg_train)
shuffle(pos_test)
shuffle(neg_test)

var=0
def create_dict (folder, a_dict):
    file_list=os.listdir(folder)
    for file in file_list:
        global var
        print(str(var)+'\n')
        f=open(os.path.join(folder,file),encoding="utf-8")
        var=var+1
        a_dict[var]=f.read()        
    f.close()
    return a_dict

a_dict={}
posTrain=create_dict("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\train\\positive", a_dict)
negTrain=create_dict("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\train\\negative", a_dict)
var=0
b_dict={}
posTest=create_dict("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\test\\positive", b_dict)
negTest=create_dict("C:\\Users\\DuttaHritwik\\Desktop\\IMDB Hindi Movie Review Dataset\\test\\negative", b_dict)

train = {**posTrain, **negTrain}
test={**posTest,**negTest}
#print(posTrain.keys())
#print(negTrain.keys())
print(train.keys())
print(train.items())
print(test.keys())
print(test.items())

def create_dictionaries(train=None,test=None,model=None):
    if (train is not None) and (model is not None) and (test is not None):
        gensim_dict=Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        w2indx={v:k+1 for k,v in gensim_dict.items()}
        w2vec={word: model[word] for word in w2indx.keys()}

        def parse_dataset(data):
            for key in data.keys():
                txt=data[key].lower().replace('\n','').split()
                new_txt=[]
                for word in txt:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)
                data[key]=new_txt
            return data
        train=parse_dataset(train)
        test=parse_dataset(test)
        return w2indx,w2vec,train,test
    else:
        print('No data provided...')

print('Loading Data...')

cpu_count=multiprocessing.cpu_count()
#Training a Word2Vec Model
model=Word2Vec(size=300,window=window_size,min_count=1,workers=cpu_count)
model.build_vocab(all_reviews)
model.train(all_reviews,total_examples=model.corpus_count,epochs=model.iter)


print('Transform the Data...')
index_dict,word_vectors,train,test=create_dictionaries(train=train,test=test,model=model)

print('Setting up Arrays for Keras Embedding Layer...')
n_symbols=len(index_dict)+1  # adding 1 to account for 0th index
embedding_weights=np.zeros((n_symbols,300))
for word,index in index_dict.items():
    embedding_weights[index,:]=word_vectors[word]

print('Creating Datesets...')
X_train=train.values()
y_train=[1 if value > 12500 else 0 for value in train.keys()]
X_test=test.values()
y_test=[1 if value > 12500 else 0 for value in test.keys()]

print("Pad sequences (samples x time)")
X_train=sequence.pad_sequences(X_train, maxlen=300)
X_test=sequence.pad_sequences(X_test, maxlen=300)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Convert labels to Numpy Sets...')
y_train=np.array(y_train)
y_test=np.array(y_test)

lstm_model=Sequential()  # or Graph 
lstm_model.add(Embedding(output_dim=300,input_dim=n_symbols,mask_zero=True,
                    weights=[embedding_weights],input_length=input_length))  
# Adding Input Length
lstm_model.add(LSTM(300))
lstm_model.add(Dropout(0.3))
lstm_model.add(Dense(1, activation='sigmoid'))

print('Compiling the Model...')
lstm_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
          #class_mode='binary')
# While compiling model, in losses we have binry_crossentropy, try categorical_crossentropy instead
print("Train...")
lstm_model.fit(X_train, y_train,batch_size=batch_size,nb_epoch=5,
          validation_data=(X_test,y_test))

print("Evaluate...")
score,acc=lstm_model.evaluate(X_test,y_test,batch_size=batch_size)
print('Test score:',str(score*100))
print('Test accuracy:',str(acc*100))
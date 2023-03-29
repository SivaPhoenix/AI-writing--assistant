import pickle
from happytransformer import HappyTextToText, TTTrainArgs

happy_tt = HappyTextToText("T5", "t5-base")

train_args = TTTrainArgs(batch_size=8, num_train_epochs=5)
happy_tt.train("Dataset/traincombo.csv", args=train_args)

eval_args = TTTrainArgs(batch_size=8)
happy_tt.eval("Dataset/evalcombo.csv", args=eval_args)

pickle.dump(happy_tt, open('model.pkl','wb'))

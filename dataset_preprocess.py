# Pre-processing/preparing JFLEG and C4_200M dataset for grammatical corrections.

from datasets import load_dataset
import csv

# JFLEG Dataset

train_dataset = load_dataset("jfleg", split='validation[:]') 
eval_dataset = load_dataset("jfleg", split='test[:]')

print(train_dataset)
print(train_dataset['sentence'][0])
print(train_dataset['corrections'][0])

replacements = [
  (" .", "."), 
  (" ,", ","),
  (" '", "'"),
  (" ?", "?"),
  (" !", "!"),
  (" :", "!"),
  (" ;", "!"),
  (" n't", "n't"),
  (" v", "n't"),
  ("2 0 0 6", "2006"),
  ("5 5", "55"),
  ("4 0 0", "400"),
  ("1 7-5 0", "1750"),
  ("2 0 %", "20%"),
  ("5 0", "50"),
  ("1 2", "12"),
  ("1 0", "10"),
  ('" ballast water', '"ballast water')
]

def remove_excess_spaces(text):
  for rep in replacements:
    text = text.replace(rep[0], rep[1])

  return text

def generate_csv(csv_path, dataset):
    with open(csv_path, 'w', newline='') as csvfile:
        writter = csv.writer(csvfile)
        writter.writerow(["input", "target"])
        for case in dataset:
     	    # Adding the task's prefix to input 
            input_text = "grammar: " + case["sentence"]
            input_text = remove_excess_spaces(input_text)
            for correction in case["corrections"]:
              correction = remove_excess_spaces(correction)
              # a few of the cases contain blank strings. 
              if input_text and correction:
                writter.writerow([input_text, correction])

# Generate train and eval for JFLEG Dataset
!mkdir Dataset
!mkdir Dataset/JFLEG
generate_csv("Dataset/JFLEG/train.csv", train_dataset)
generate_csv("Dataset/JFLEG/eval.csv", eval_dataset)

# C4_200M Dataset

c4_dataset = load_dataset("liweili/c4_200m", streaming = True)

iterator = iter(dataset['train'])

def c4_generate_csv(csv_path, iterator, num_examples):
    with open(csv_path, 'w', newline='') as csvfile:
        writter = csv.writer(csvfile)
        writter.writerow(["input", "target"])
        for i in range(0,num_examples):
          data = next(iterator)
          input_text = "grammar: " + data["input"]
          input_text = remove_excess_spaces(input_text)
          correction = remove_excess_spaces(data["output"])
          if input_text and correction:
            writter.writerow([input_text, correction])

# Generate first 3500 examples from C4_200M dataset
!mkdir Dataset/C4_200M
c4_generate_csv("Dataset/C4_200M/c4data.csv", iterator, num_examples=3500)

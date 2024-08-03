import csv

from tokenizers import Tokenizer
tokenizer = Tokenizer.from_pretrained("upstage/solar-1-mini-tokenizer")

def compute_cost(csv_file_name, price_per_million_tokens=0.5):
  """ Compute the cost of the dataset """

  total_num_of_tokens = 0
  with open(csv_file_name, 'r') as f:
    reader = csv.DictReader(f)
    # get all values
    values = [row['completion']+ " " + row['prompt'] for row in reader]
    for value in values:
      # tokenize
      enc = tokenizer.encode(value)
      num_of_tokens = len(enc.tokens)
      total_num_of_tokens += num_of_tokens


  return total_num_of_tokens / 1000000 * price_per_million_tokens
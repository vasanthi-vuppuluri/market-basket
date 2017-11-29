from collections import Counter, defaultdict


class Apriori:
  """Apriori algorithm.
  Returns frequent item-sets with a minimum of `n` SKUs per item-set whose frequency is at least sigma

  Reference: http://paulallen.ca/apriori-algorithm-generating-candidate-fis/
  """

  def __init__(self, log_file_path, output_file_path, min_itemset_size, sigma, verbose=False):
    self.log_file_path = log_file_path
    self.output_file_path = output_file_path
    self.min_itemset_size = min_itemset_size
    self.sigma = sigma
    self.verbose = verbose
    self.candidate_item_sets = list()
    self.frequent_item_sets = defaultdict(Counter)

  def _get_frequent_itemsets(self, item_set_size):
    """
    Returns all candidate item-sets with minimum support level, sigma
    """

    # Filter out item-sets if their frequency is less than that of the minimum support value
    frequent_candidate_item_sets = defaultdict(int)
    for item_set in self.frequent_item_sets[item_set_size]:
      if self.frequent_item_sets[item_set_size][item_set] >= self.sigma:
        frequent_candidate_item_sets[item_set] = self.frequent_item_sets[item_set_size][item_set]

    if self.verbose:
      print("{}. Candidate item-sets of size {} = {} and with sigma >= {} = {}".
            format(item_set_size, item_set_size, len(self.frequent_item_sets[item_set_size]),
                   self.sigma, len(frequent_candidate_item_sets)))

    self.frequent_item_sets[item_set_size] = frequent_candidate_item_sets
    del frequent_candidate_item_sets

    return self.frequent_item_sets[item_set_size]

  def _get_transaction_log_data(self):
    """
    Reads data from input transaction log file.
    Returns transactions with specified minimum number of items (SKUs)
    and a list of candidate item-sets of size one
    """

    if self.verbose:
      print("\nReading data from the input file, {}"
            "\nTransactions with a minimum of {} unique SKUs will be considered\n".
            format(self.log_file_path, self.min_itemset_size))

    # Convert each transaction to a tuple of unique SKUs if the count of unique SKUs is >= sigma
    # Generate a list of candidate item-sets of size one, i.e., frequencies of unique SKUs
    with open(self.log_file_path, 'r') as transaction_log_file:
      for transaction in transaction_log_file.readlines():
        itemsets = [tuple([sku]) for sku in set(map(int, transaction.strip().split()))]
        if len(itemsets) >= self.min_itemset_size:
          self.candidate_item_sets.append(sorted(itemsets))
          for sku in itemsets:
            self.frequent_item_sets[1][sku] += 1

    self.frequent_item_sets[1] = self._get_frequent_itemsets(1)

    return self.frequent_item_sets[1]

  def get_frequent_itemsets(self):
    """
    Returns frequent item-sets of size >= n and frequency >= sigma
    """

    self.frequent_item_sets[1] = self._get_transaction_log_data()

    # Note: For an item-set to have a high frequency, all the subsets of the item-set
    # will have to be of high frequency
    item_set_length = 2
    while len(self.frequent_item_sets[item_set_length - 1]) >= item_set_length:
      for i in range(len(self.candidate_item_sets)):
        frequent_itemsets_1 = [item_set for item_set in self.candidate_item_sets[i]
                               if item_set in self.frequent_item_sets[item_set_length - 1]]
        # Candidate generation
        # Based on Fk-1 x Fk-1 method (used by apriori-gen), i.e.,
        # a pair of frequent (k-1)-item sets are merged if and only if their
        # first k-2 items are identical
        frequent_item_list_2 = [tuple(sorted(frozenset(x).union(y)))
                                for x in frequent_itemsets_1
                                for y in frequent_itemsets_1
                                if x < y and x[:-1] == y[:-1]]
        self.candidate_item_sets[i] = frequent_item_list_2
        for item_set in frequent_item_list_2:
          self.frequent_item_sets[item_set_length][item_set] += 1

      # Update frequent item-sets
      self.frequent_item_sets[item_set_length] = self._get_frequent_itemsets(item_set_length)

      # Write frequent item-set size, co-occurrence frequency and SKUs in the
      # item-set to the output file iff item-set size >= minimum item-set size specified
      with open(self.output_file_path, 'a') as output_file:
        if item_set_length >= self.min_itemset_size:
          for item_set, frequency in sorted(self.frequent_item_sets[item_set_length].items(),
                                            key=lambda x: (-x[1], x[0])):
            output_file.write("{} {} ".format(item_set_length, frequency))
            output_file.write(("{} "*len(item_set)).format(*item_set))
            output_file.write("\n")
      output_file.close()

      item_set_length += 1

    if self.verbose:
      print("\nOutput is written to the file, {}".format(self.output_file_path))


def main():
  import argparse
  description = "Identifies frequent item-sets with a minimum size `n` for the value of sigma `s`"
  argument_parser = argparse.ArgumentParser(description=description)
  argument_parser.add_argument("transaction_log",
                               help="Path to the transaction log file")
  argument_parser.add_argument("-n", "--size", default=3,
                               help="Minimum size of the frequent item-set (default=3)")
  argument_parser.add_argument("-s", "--sigma", default=4,
                               help="Support level parameter (default=4)")
  argument_parser.add_argument("-v", "--verbose",
                               help="Display verbose output", action="store_true")
  argument_parser.add_argument("-o", "--output_file_path", default="output.txt",
                               help="Path to the output file (default=output.txt)")
  arguments = argument_parser.parse_args()

  transaction_log = arguments.transaction_log
  n = arguments.size
  sigma = arguments.sigma
  verbose = arguments.verbose
  output_file_path = arguments.output_file_path

  # Empty the file contents if the file is non-empty
  with open(output_file_path, 'w') as output_file:
    output_file.write("")
  output_file.close()

  if verbose:
    print("\nInput arguments:\nTransaction log = {}\nMinimum size of frequent item-set = {}"
          "\nSupport level parameter, sigma = {}\nOutput file = {}".
          format(transaction_log, n, sigma, output_file_path))

  Apriori(transaction_log, output_file_path, n, sigma, verbose).get_frequent_itemsets()


if __name__ == '__main__':
  from time import time
  start_time = time()
  main()
  print("\nTime taken = {} seconds\n".format(time() - start_time))

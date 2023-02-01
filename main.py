from processor import *
import argparse

if __name__ == "__main__":
    #command line arguments parser
    t = TransactionsProcessor()
    parser = argparse.ArgumentParser(
                        prog = 'Process Transactions',
                        description = 'Deducts the points the user wants to use and gives the remaining points as per the payer',)
    parser.add_argument('points',  type=int,
                    help='number of points the user wants to spend')
    parser.add_argument('--check-for-insufficiency',type=bool , default=False,
                    help='Check for insufficient balance')
    args = parser.parse_args()
    print(t.process_transactions(args.points, args.check_for_insufficiency))
    

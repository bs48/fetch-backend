
import sys
import csv
from os.path import exists
import json 

class TransactionsProcessor:

    def __init__(self):
        pass

    def pre_process(self, transactions):
    #sort the transactions based on timestamp
        transactions = sorted(transactions, key=lambda d: d['timestamp']) 
        group_by_payer = {}


        #combine the negative points with the just above posistive 
            #transactions by the same payer to avoid the payers points below 0
        for transaction in transactions :
            transaction['points'] = int(transaction['points'])
            group_by_payer[transaction['payer']] = group_by_payer[transaction['payer']] if transaction['payer'] in group_by_payer else []
            if transaction['points'] >= 0:
                group_by_payer[transaction['payer']].append(transaction)
            else:
                points = transaction['points']
                for pre_existing in reversed(group_by_payer[transaction['payer']]):
                    if pre_existing['points'] >= abs(points):
                        pre_existing['points'] -= abs(points)
                        points = 0
                        break
                    else:
                        points += pre_existing['points']
                        pre_existing['points'] = 0
        
        filtered_transactions = []


        #combine all the transactions into one list

        for payer in group_by_payer.keys():
            filtered_transactions.extend(group_by_payer[payer])
        filtered_transactions = sorted(filtered_transactions, key=lambda d: d['timestamp'])

        return filtered_transactions


    def process_transactions(self, points_to_be_spent, check):
    
        oringinal_points = points_to_be_spent

        try:
            #check if file is present in working directory
            if not exists("./transactions.csv"):
                print("File not found!")
                return
            file =  open("transactions.csv", "r")

            #reading the csv file and converting it into python dict
            reader = csv.DictReader(file)
            transactions = list(reader)

            filtered_transactions = self.pre_process(transactions)

            remaining_points = {}

            #iteratively reduce points from each transaction sorted by 
            #timestamp to get the remaining points that can be provided by each payer

            for transaction in filtered_transactions:
                remaining_points[transaction['payer']] = remaining_points[transaction['payer']] if transaction['payer'] in remaining_points else 0
                remaining_points[transaction['payer']] += 0  if points_to_be_spent > transaction['points'] else transaction['points'] - points_to_be_spent
                points_to_be_spent =  points_to_be_spent - transaction['points'] if points_to_be_spent > transaction['points'] else 0
        
            # check for insufficient balance
            if check and points_to_be_spent > 0:
                return 'Insufficient Balance!'
            

            #final answer is printed
            #print(remaining_points)
            return json.dumps(remaining_points, indent = 4)

        except Exception as e:
            print(e)
            return
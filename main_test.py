from processor import *
import json
tc_outputs={
    'normal': {'DANNON': 1000, 'UNILEVER': 0, 'MILLER COORS': 5300},
    'handling_negative' : {'DANNON': 1000, 'UNILEVER': 0, 'MILLER COORS': 10000},
    'insufficient_off' : {'DANNON': 0, 'UNILEVER': 0, 'MILLER COORS': 0},
    'insufficient_on' : 'Insufficient Balance!'
}

def test_normal():
    processor = TransactionsProcessor()
    output = json.dumps(tc_outputs['normal'], indent=4)
    assert(processor.process_transactions(5000, False) == output)
    
def test_negatives():
    processor = TransactionsProcessor()
    output = json.dumps(tc_outputs['handling_negative'], indent=4)
    assert(processor.process_transactions(300, False) == output)

def test_excess_with_insufficientcy_unchecked():
    processor = TransactionsProcessor()
    output = json.dumps(tc_outputs['insufficient_off'], indent=4)
    assert(processor.process_transactions(100000, False) == output)

def test_excess_with_insufficientcy_checked():
    processor = TransactionsProcessor()
    output = tc_outputs['insufficient_on']
    assert(processor.process_transactions(100000, True) == output)
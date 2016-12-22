# In The Name Of God
# ========================================
# [] File Name : qr.py
#
# [] Creation Date : 06-12-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
#
# [] Created By : Saman Fekri (samanf74@gmail.com)
# =======================================

import copy
class QuadRuple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg_one = arg1
        self.arg_two = arg2
        self.result = result

    @staticmethod
    def backpatch(list, label):
        for i in list:
            i.arg_one = label

    @staticmethod
    def merge(list1,list2):
        temp = copy.deepcopy(list1)
        temp = temp + list2
        return temp
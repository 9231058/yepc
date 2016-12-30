class YEPCEntity:
    def __init__(self):
        self.true_list = []
        self.false_list = []
        self.next_list = []
        self.type = None
        self.place = None
        self.quad = 0
        self.case_dict = []

    @staticmethod
    def backpatch(quad_list, target):
        for quad in quad_list:
            quad.arg_one = target

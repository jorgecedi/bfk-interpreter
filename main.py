import sys

class BfkEvaluator:
    counter:int = 0
    dp: int = 0
    ip: int = 0
    cells = [0]*30000 # According to wikipedia it should be 30,000 cells
    code: str = ""
    instruction_limit:int = 1000000

    def check_for_balanced(self):
        stack = []
        
        self.jump_if_zero = {}
        self.jump_if_not_zero = {}

        i = 0
        for t in self.code:
            if t == "[":
                stack.append(i)
            elif t == "]":
                j = stack.pop()
                self.jump_if_zero[j] = i
                self.jump_if_not_zero[i] = j
            i += 1

        if len(stack) > 0:
            raise Exception("unbalanced error")

    def tokenize(self, code:str):
        allowed_inputs = ["+", "-", ">", "<", "[", "]", ".", ","]
        self.code = code.replace("\n", "").replace("\r", "").replace(" ","")
        new_code = ""
        for s in code:
            if s in allowed_inputs:
                new_code = new_code + s

        self.code = new_code
        print(self.code)

    def eval_bfk(self):
        self.check_for_balanced()
        while(self.counter < self.instruction_limit and self.ip < len(self.code)):
            token = self.code[self.ip]

            if token == "+":
                self.op_inc()
                self.ip += 1

            elif token == "-":
                self.op_dec()
                self.ip += 1

            elif token == ">":
                self.op_move_right()
                self.ip += 1

            elif token == "<":
                self.op_move_left()
                self.ip += 1

            elif token == "[":
                self.op_jump_if_zero()

            elif token == "]":
                self.op_jump_if_non_zero()

            elif token == ".":
                print(chr(self.cells[self.dp]))
                self.ip += 1

            elif token == ",":
                ch = sys.stdin.read(1)
                self.cells[self.dp] = ord(ch)
                self.ip += 1

            # Just to avoid running to infinity
            self.counter += 1

            print(f"Instruction: {token}")
            print(f"Cells[{self.dp}] =  {self.cells[self.dp]}")
            print(f"Instruction pointer: {self.ip}")
            print("")
            if self.dp < 0 :
                print("PANIC, out of memory bounds")
                return

        return

    def op_inc(self):
        self.cells[self.dp] += 1

    def op_dec(self):
        self.cells[self.dp] -= 1

    def op_move_right(self):
        self.dp += 1

    def op_move_left(self):
        self.dp -= 1

    def op_jump_if_zero(self):
        if self.cells[self.dp] == 0:
            # self.ip = self.ip + self.code[self.ip:].index("]") 
            self.ip = self.jump_if_zero[self.ip] + 1
        else:
            self.ip += 1

    def op_jump_if_non_zero(self):
        if self.cells[self.dp] != 0:
            # self.ip = self.ip - self.code[:self.ip][::-1].index("[")
            self.ip = self.jump_if_not_zero[self.ip] + 1
        else:
            self.ip += 1


evaluator = BfkEvaluator()

with open("adder.bfk", "r") as f:
    code = f.read()
    evaluator.tokenize(code)
    evaluator.eval_bfk()

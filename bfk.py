import sys


class BfkEvaluator:
    counter: int = 0
    dp: int = 0
    ip: int = 0
    cells = [0] * 30000  # According to wikipedia it should be 30,000 cells
    code: str = ""
    instruction_limit: int = 1000000 # Just to avoid running to infinity
    jump_if_zero = {}
    jump_if_not_zero = {}
    with_debug = False

    def __init__(self, with_debug=False):
        self.with_debug = with_debug

    def map_jump_branches(self):
        stack = []

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

    def tokenize(self, code: str):
        allowed_inputs = ["+", "-", ">", "<", "[", "]", ".", ","]
        self.code = code.replace("\n", "").replace("\r", "").replace(" ", "")
        new_code = ""
        for s in code:
            if s in allowed_inputs:
                new_code = new_code + s

        self.code = new_code
        print(self.code)

    def eval_bfk(self, code: str):
        self.tokenize(code)
        self.map_jump_branches()
        while self.counter < self.instruction_limit and self.ip < len(self.code):
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
                self.op_print()
                self.ip += 1

            elif token == ",":
                self.op_read()
                self.ip += 1

            # Just to avoid running to infinity
            self.counter += 1

            if self.with_debug:
                print(f"Instruction: {token}")
                print(f"Cells[{self.dp}] =  {self.cells[self.dp]}")
                print(f"Instruction pointer: {self.ip}")
                print("")

            if self.dp < 0:
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
            self.ip = self.jump_if_zero[self.ip] + 1
        else:
            self.ip += 1

    def op_jump_if_non_zero(self):
        if self.cells[self.dp] != 0:
            self.ip = self.jump_if_not_zero[self.ip] + 1
        else:
            self.ip += 1

    def op_print(self):
        print(chr(self.cells[self.dp]), end="")

    def op_read(self):
        ch = sys.stdin.read(1)
        self.cells[self.dp] = ord(ch)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bfk.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    debug = False
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        debug = True

    evaluator = BfkEvaluator(with_debug=debug)

    with open(filename, "r") as f:
        code = f.read()
        evaluator.eval_bfk(code)

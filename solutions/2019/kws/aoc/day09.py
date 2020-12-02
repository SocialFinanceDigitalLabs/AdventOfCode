MODES = ['I','D','R']

class GrowingList(list):
    def __auto_extend__(self, index):
        max_len = 0
        if isinstance(index, slice):
            ix_max = max(index.start, index.stop)
            if ix_max >= len(self):
                max_len = ix_max
        elif index >= len(self):
            max_len = index
        
        if max_len > 0:
            self.extend([0]*(max_len + 1 - len(self)))
        
    def __setitem__(self, index, value):
        self.__auto_extend__(index)
        return list.__setitem__(self, index, value)

    def __getitem__(self, index):
        self.__auto_extend__(index)
        return list.__getitem__(self, index)

        
class IntCodeComputer:
    

    def __init__(self, memory, ptr=0, debug=False):
        self.memory = GrowingList(memory)
        self.ptr = ptr
        self.relative_base = 0
        self.output_list = []
        self.__debug = debug
        self.operations = {
            1:  self.add,
            2:  self.multiply,
            3:  self.user_input,
            4:  self.user_output,
            5:  self.jump_if_true,
            6:  self.jump_if_false,
            7:  self.less_than,
            8:  self.equals,
            9:  self.adjust_relative_base,
            99: self.stop
        }

    # First we need to support parameter mode
    def parse_operation(self, oper):
        value = "{:05}".format(oper)
        a = int(value[0])
        b = int(value[1])
        c = int(value[2])
        op = int(value[3:])

        return (op, c, b, a)
    
    def format_op(self, op, input_params, output_params):
        name = self.operations[op[0]].__name__.upper()
        input_mode = ""
        output_mode = ""
        for i in range(0, input_params):
            input_mode += MODES[op[i+1]]
        for i in range(input_params, input_params+output_params):
            output_mode += MODES[op[i+1]]
            
        return "{} {} {}".format(name, input_mode, output_mode)
    
    def read_memory(self, op, input_params, output_params=0):
        mem_slice = self.memory[self.ptr:self.ptr+input_params+output_params+1]
        
        if self.__debug:
            print("{:3} {} {}".format(self.ptr, 
                                  self.format_op(op, input_params, output_params),mem_slice[1:]))
        
        output = []
        for i in range(1, input_params + 1):
            m = mem_slice[i]
            if op[i] == 0:
                m = self.memory[m]
            elif op[i] == 2:
                m = self.memory[self.relative_base+m]
            output.append(m)

        for i in range(input_params+1, input_params+output_params+1):
            if op[i] == 0:
                m = mem_slice[i]
            elif op[i] == 1:
                m = self.ptr+i
            elif op[i] == 2:
                m = self.relative_base + mem_slice[i]

            output.append(m)
            
        if self.__debug:
            print("    IN: {} OUT: {}".format(output[0:input_params], output[input_params:input_params+output_params]))
        
        if len(output) == 1:
            return output[0]
        else:
            return output
        
    def write_memory(self, ptr, value):
        if self.__debug:
            print("    WRITE: ptr={} value={}".format(ptr, value))
        self.memory[ptr] = value

    def add(self, op):
        params = 3
        a, b, c = self.read_memory(op, params-1, 1)
        self.write_memory(c, a + b)
        return self.ptr + params + 1

    def multiply(self, op):
        params = 3
        a, b, c = self.read_memory(op, params-1, 1)
        self.write_memory(c, a * b)
        return self.ptr + params + 1
    
    def jump_if_true(self, op):
        params = 2
        a, b = self.read_memory(op, params)
        return self.ptr + params + 1 if a == 0 else b

    def jump_if_false(self, op):
        params = 2
        a, b = self.read_memory(op, params)
        return self.ptr + params + 1 if a != 0 else b

    def less_than(self, op):
        params = 3
        a, b, c = self.read_memory(op, params-1, 1)
        self.write_memory(c, 1 if a < b else 0)
        return self.ptr + params + 1
    
    def equals(self, op):
        params = 3
        a, b, c = self.read_memory(op, params-1, 1)
        self.write_memory(c, 1 if a == b else 0)
        return self.ptr + params + 1

    def user_input(self, op):
        """
        Checks to see if input is available. 
        
        If input returns None then the computer halts until restarted
        """
        params = 1
        a = self.read_memory(op, 0, params)
        
        input_value = self.input_value()
        if input_value is None:
            return {"ptr": self.ptr, "yield": True}
        else:
            self.write_memory(a, int(input_value))
            return self.ptr + params + 1

    def user_output(self, op):
        params = 1
        a = self.read_memory(op, params)
        should_yield = self.output_value(a)
        return {"ptr": self.ptr + params + 1, "yield": should_yield}

    def adjust_relative_base(self, op):
        params = 1
        a = self.read_memory(op, params)
        self.relative_base += a
        if self.__debug:
            print("    rbase {} -> {}".format(a, self.relative_base))
        return self.ptr + params + 1

    def stop(self, op):
        self.read_memory(op, 0)
        return -1

    def execute(self):
        op = self.parse_operation(self.memory[self.ptr])
        operation = self.operations[op[0]]
        return operation(op)
    
    def run(self):
        if self.__debug:
            print("-----")
        
        while True:
            out = self.execute()
            try:
                self.ptr = out["ptr"]
                if out.get("yield", False):
                    return -2
            except TypeError:
                self.ptr = out

            if self.ptr < 0:
                return self.ptr
        

    def input_value(self):
        return input()
    
    def output_value(self, a):
        print("OUTPUT:", a)
        self.output_list.append(a)
        return False
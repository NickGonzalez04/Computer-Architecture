"""CPU functionality."""

import sys

# #Op_codes
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        """ Ram holding 256 bytes of memory """
        self.ram = [0] * 256
        """ Reg holding 8 positions """
        self.reg = [0] * 8
        """ program control """
        self.pc = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.func_LDI
        self.branchtable[PRN] = self.func_PRN
        self.branchtable[MUL] = self.func_MUL
        self.branchtable[HLT] = self.func_HLT
        self.running = True 

    def load(self):
        """Load a program into memory."""

        """Check to make sure thr right number of arguments were entered"""
        if len(sys.argv) !=2:
            print("Usage: ls8.py --filename")
            sys.exit(1)

        # Sets the address to zero so it can be index when memory is being saved
        address = 0
        # For now, we've just hardcoded a program:
        # program = [
        #     #From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, # R0 is register 0
        #     0b00001000, # Saving the value of 8
        #     0b01000111, # PRN 
        #     0b00000000, # Printing out R0
        #     HLT, # HLT , Haulting the program
        # ]

        # Allow the command line to run two arguments 
        prog_name = sys.argv[1]
        #
        with open(prog_name) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue
                # Define the base with 2 since it is binary
                val = int(line, 2)
                print(val)
                self.ram[address] = val
                address += 1
 
        # sys.exit(0)

        # Loops through the program(memory)
        # Gives the address an index and sets it to an instruction
        # for instruction in program:
            # self.ram[address] = val
            #     address += 1

                
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    # Helper functions
    # MAR Memory Address Register 
    # Contains Address that is being read
    def ram_read(self, MAR):
        #
        return self.ram[MAR]
    # Memory Data Register 
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def func_LDI(self):
        # Saving to register if instruction is LDI
        # saving the value to the register
        # Using the ram_read() helper function  
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)     
        self.reg[operand_a] = operand_b
        # self.pc += 3
    def func_PRN(self):
        # Printing out the register if instruction is PRN
        # Printing out the register and its value
         # Using the ram_read() helper function
        reg_num = self.reg[self.ram_read(self.pc + 1)]
        print(f"Printing register - {reg_num}")
        # self.pc += 2

    def func_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        # self.pc +=3 

    def func_HLT(self):
        #HLT Haulting the pc 
        # self.ram_read(self.pc + 1)
        #Stopping the while Loop
        self.running = False
        print('exit')


    def run(self):
        """Run the CPU."""
        # Running is set equal to True
        # Loops running 
        while self.running: 
            # Defined short hands
            instruction = self.ram[self.pc]
            # operand_a = self.ram_read(self.pc + 1)
            # operand_b = self.ram_read(self.pc + 2)
            # Moves the IR over 6 places if it the first 2 digits
            op_Count = instruction >> 6
            ir_length = op_Count + 1
            # print(f"ir_length: {ir_length}")
        
            self.branchtable[instruction]()

            
    
            if instruction == 0 or None:
                print(f"Not and instruction at {self.pc}")
                sys.exit(1)

            self.pc += ir_length

                

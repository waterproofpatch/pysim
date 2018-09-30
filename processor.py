"""
Represents an abstract capable of limited operations on limited registers
"""
import logging
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)s:%(levelname)s: %(message)s')


class Processor(object):
    """
    Represents a processor
    """

    class DecodeException(Exception):
        def __init__(self, message):
            super(Processor.DecodeException, self).__init__(message)

    class Immediate(object):
        """
        A simple 'immediate' value
        """
        def __init__(self, value):
            """
            Create an immediate object with an initial value.

            :param value: the value (int)
            """
            self.value = value

        def __repr__(self):
            """
            Get a representation of this object.

            :return: A string representation of this object
            """
            return "Imm({})".format(self.value)

    class Reg(object):
        """
        A simple 'register'
        """
        def __init__(self, name):
            """
            Create a register object with a name

            :param name: the name for this register
            """
            # TODO take 'value' as param
            self.name = name
            self.value = 0

        def __repr__(self):
            """
            Get a string representation of this register

            :return: a string representation of this register
            """
            return "Reg({}) -> {}".format(self.name, self.value)
        
        def __add__(self, other):
            """
            Add another operand to this register

            :param other: the other operand, of type Register or Immediate
            :return: None
            """
            self.value = self.value + other.value

        def __sub__(self, other):
            """
            Subtract another operand from this register.

            :param other: the other operand, of type Register or Immediate
            :return:
            """
            self.value = self.value - other.value

    class Operand(object):
        """
        Represents one of a subset of operands
        """

        class TypeException(Exception):
            """
            Exception regarding an invalid operand type
            """
            def __init__(self, message):
                super(Processor.Operand.TypeException, self).__init__(message)

        def __init__(self, token, processor):
            """
            Create an operand from the token

            :param token: the token from the program
            :param processor: ref to the processor (containing state)
            """
            self.operand = None
            if token[0] == '$':
                self.operand = processor.registers[token[1]]
            elif token[0] == '#':
                self.operand = Processor.Immediate(value=int(token[1:], 16))
            else:
                raise Processor.Operand.TypeException("Invalid operand type: {}".format(token[0]))

        def __repr__(self):
            return "Operand({})".format(self.operand.__repr__())


    class Op(object):
        """
        Operations can be performed on registers and immediates
        """
        class InvalidOperandException(Exception):
            def __init__(self, message):
                super(Processor.Op.InvalidOperandException, self).__init__(message)

        def __init__(self, mnemonic):
            self.mnemonic = mnemonic
            self.behaviors = {
                'sub': self._sub_behavior,
                'add': self._add_behavior,
                'put': self._put_behavior,
            }

        def get_num_operands(self):
            """
            Get the number of required operands for this action

            :return: number of operands
            """
            if self.mnemonic == "add":
                return 2
            if self.mnemonic == "sub":
                return 2
            if self.mnemonic == "put":
                return 2

        def execute(self, operands):
            """
            Execute an instruction on the given operands.

            :param operands: A list of operands.
            :return: None
            """
            self.behaviors[self.mnemonic](operands[0], operands[1])

        def _sub_behavior(self, operand_1, operand_2):
            """
            Perform subtraction of two registers (or a constant)

            :param operand_1: the resultant and addend register
            :param operand_2: the addee register or immediate
            """
            if not isinstance(operand_1.operand, Processor.Reg):
                raise Processor.Op.InvalidOperandException("operand {} is of invalid type ({})".format(operand_1, type(operand_1)))
            operand_1.operand.value = operand_1.operand.value + operand_2.operand.value

        def _add_behavior(self, operand_1, operand_2):
            """
            Perform addition of two registers (or a constant)

            :param operand_1: the resultant and addend register
            :param operand_2: the addee register or immediate
            """
            if not isinstance(operand_1.operand, Processor.Reg):
                raise Processor.Op.InvalidOperandException("operand {} is of invalid type ({})".format(operand_1, type(operand_1)))
            operand_1.operand.value = operand_1.operand.value + operand_2.operand.value

        def _put_behavior(self, operand_1, operand_2):
            """
            Perform put of one value into another

            :param operand_1: the resultant register
            :param operand_2: the src register or immediate
            """
            if not isinstance(operand_1.operand, Processor.Reg):
                raise Processor.Op.InvalidOperandException("operand {} is of invalid type ({})".format(operand_1, type(operand_1)))
            operand_1.operand.value = operand_2.operand.value
        
        def __repr__(self):
            return "Op({})".format(self.mnemonic)

    def __init__(self):
        self.registers = {}
        self.registers['0'] = Processor.Reg('$0')
        self.registers['1'] = Processor.Reg('$1')
        self.registers['2'] = Processor.Reg('$2')
        self.registers['3'] = Processor.Reg('$3')
        self.op_add = Processor.Op('add')
        self.op_sub = Processor.Op('sub')
        self.op_put = Processor.Op('put')

        self._actions = {}
        self._actions['add'] = self.op_add
        self._actions['sub'] = self.op_sub
        self._actions['put'] = self.op_put

    def perform_instruction(self, line):
        """
        Execute one instruction.

        :param line: the text line containing the instruction to be decoded and executed.
        """

        line = line.split("//")[0].strip()
        tokens = line.split(" ")
        # lines have a general format 'action op1 op2 ...'
        (action, operands) = self._decode(tokens=tokens)
        action.execute(operands)

    def dump_state(self):
        """
        LOGGER.info state out to the screen.
        """
        LOGGER.info("program state:")
        for r in self.registers:
            LOGGER.info(self.registers[r])

    def _decode(self, tokens):
        """
        Decode a list of tokens into operation and operands.
        The first token is expected to be a valid 'action' (e.g. a verb), and each additional token a noun (register, immediate).

        :return: (Op, (Operand, Operand, Operand, ...))
        """
        op = self._get_action(mnemonic=tokens[0])
        num_required_operands = op.get_num_operands()
        if num_required_operands != len(tokens) - 1:
            raise Processor.DecodeException("Invalid number of operands, require {} have {}".format(op.get_num_operands(), len(tokens)-1))
        operands = []
        for t in tokens[1:]:
            operands.append(Processor.Operand(t, self))
        return (op, tuple(operands))

    def _get_action(self, mnemonic):
        """
        Returns an action method based on the mnemonic

        :param mnemonic: the name of the operation, e.g. 'add'
        :return: method
        """
        if mnemonic not in self._actions.keys():
            raise Processor.DecodeException("invalid mnemonic: {}".format(mnemonic))
        return self._actions[mnemonic]


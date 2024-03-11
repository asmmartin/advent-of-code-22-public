# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest

from day21 import OPERATION_FUNCTIONS, Monkey

@pytest.fixture(name='text_input')
def text_input_fixture():

    return '''
        root: pppw + sjmn
        dbpl: 5
        cczh: sllz + lgvd
        zczc: 2
        ptdq: humn - dvpt
        dvpt: 3
        lfqf: 4
        humn: 5
        ljgn: 2
        sjmn: drzm * dbpl
        sllz: 4
        pppw: cczh / lfqf
        lgvd: ljgn * ptdq
        drzm: hmdt - zczc
        hmdt: 32
    '''

def test_operations():

    assert OPERATION_FUNCTIONS['+'](9, 3) == 12
    assert OPERATION_FUNCTIONS['-'](9, 3) == 6
    assert OPERATION_FUNCTIONS['*'](9, 3) == 27
    assert OPERATION_FUNCTIONS['/'](9, 3) == 3
    assert OPERATION_FUNCTIONS['noop'](9, 3) is None

def test_yeller_monkey():

    monkey = Monkey(
        name='aaaa',
        family={},
        result=42
    )

    assert monkey.operation_function == OPERATION_FUNCTIONS['noop']
    assert monkey.family == {
        'aaaa': monkey
    }
    assert monkey.result == 42

def test_operator_monkey():

    monkey = Monkey(
        name='root',
        keys=('aaaa', 'bbbb'),
        operation_function=OPERATION_FUNCTIONS['+'],
        family={}
    )

    assert monkey.keys == ('aaaa', 'bbbb')
    assert monkey.operation_function == OPERATION_FUNCTIONS['+']
    assert monkey.family == {
        'root': monkey
    }

def test_monkey_call_yeller():

    family = {}
    monkey = Monkey(
        name='aaaa',
        family=family,
        result=42
    )

    assert monkey() == 42

def test_operator_monkey_call():

    family = {}
    Monkey(
        name='aaaa',
        family=family,
        result=36
    )
    Monkey(
        name='bbbb',
        family=family,
        result=6
    )

    monkey = Monkey(
        name='root',
        keys=('aaaa', 'bbbb'),
        operation_function=OPERATION_FUNCTIONS['+'],
        family=family
    )

    result = monkey()

    assert result == 42

def test_operator_monkey_from_instruction_operation():

    family = {}
    instruction = 'root: pppw + sjmn'
    monkey = Monkey.from_instruction(instruction, family)

    assert monkey == Monkey(
        name='root',
        keys=('pppw', 'sjmn'),
        operation_function=OPERATION_FUNCTIONS['+'],
        symbol='+',
        family=family
    )
    assert family == {'root': monkey}

def test_yeller_monkey_from_instruction():

    family = {}
    instruction = 'dbpl: 5'
    monkey = Monkey.from_instruction(instruction, family)

    assert family['dbpl'] == monkey
    assert family['dbpl'].result == 5

def test_example_1(text_input):

    instructions = text_input.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    assert family['root']() == 152

def test_example_depends_on(text_input):

    instructions = text_input.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    assert family['root'].depends_on('humn')
    assert family['humn'].depends_on('humn')
    assert family['pppw'].depends_on('humn')
    assert not family['sjmn'].depends_on('humn')

def test_example_simplify(text_input):

    instructions = text_input.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    family['root'].simplify(variable='humn')
    assert family['sjmn'].result == 150
    assert family['lfqf'].result is not None
    assert family['root'].result is None
    assert family['pppw'].result is None

def test_example_resolve_independent(text_input):

    instructions = text_input.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    with pytest.raises(ValueError):
        family['dbpl'].solve(variable='humn', target_result=7)

    with pytest.raises(ValueError):
        family['sjmn'].solve(variable='humn', target_result=7)

def test_example_resolve_dependent_basic():

    instructions = '''
        sum: sum1 + sum2
        sum1: 3
        sum2: 5
        sub: sub1 - sub2
        sub1: 9
        sub2: 3
        mul: mul1 * mul2
        mul1: 3
        mul2: 4
        div: div1 / div2
        div1: 12
        div2: 6
    '''
    instructions = instructions.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    assert family['sum'].solve(variable='sum2', target_result=9) == 6
    assert family['sum'].solve(variable='sum1', target_result=9) == 4

    assert family['sub'].solve(variable='sub2', target_result=9) == 0
    assert family['sub'].solve(variable='sub1', target_result=9) == 12

    assert family['mul'].solve(variable='mul2', target_result=12) == 4
    assert family['mul'].solve(variable='mul1', target_result=12) == 3

    assert family['div'].solve(variable='div2', target_result=6) == 2
    assert family['div'].solve(variable='div1', target_result=6) == 36

def test_example_resolve(text_input):

    instructions = text_input.strip().splitlines()
    family = {}
    for instruction in instructions:
        Monkey.from_instruction(instruction, family)

    root = family['root']
    op1 = family[root.keys[0]]
    op2 = family[root.keys[1]]

    root.simplify('humn')

    if op1.depends_on('humn'):
        result = op1.solve(target_result=op2.result, variable='humn')
    else:
        result = op2.solve(target_result=op1.result, variable='humn')

    assert result == 301

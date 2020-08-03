import random

"""
Tests various CLI inputs
"""
def test_parse_cli_input(args):

    class TestException(Exception):
        pass

    test_inputs = [
        'infile.txt outfile.txt asdf asd'.split(),
        'infile.txt outfile.txt asdf asd'.split(),
        'infile.txt outfile.txt asdf asd'.split(),
        'infile.txt outfile.txt asdf asd'.split(),
        '-r'.split(),
    ]

    tests = []


    # use exceptions to count tests and print failed tests
    for i in range(len(test_inputs)):
        input = test_inputs[i]
        tests.append(True)
        try:
            print(f"testing input {input}.")
            if random.randint(0, 10) < 5:
                raise TestException
        except TestException:
            tests[i] = False

    testsNumber = len(tests)
    passed_tests = len(list(filter(lambda x: x, tests)))

    print(f"Tests passed: {passed_tests}/{testsNumber}")


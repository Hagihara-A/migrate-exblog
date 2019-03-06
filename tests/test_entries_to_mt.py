import doctest

from migrate_exblog import entries_to_mt


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(entries_to_mt))
    return tests

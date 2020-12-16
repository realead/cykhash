class UnitTestMock:
    def assertEqual(self, a, b):
        assert a == b

    def assertFalse(self, a):
        assert not a

    def assertTrue(self, a):
        assert a

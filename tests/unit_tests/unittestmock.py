class UnitTestMock:
    def assertEqual(self, a, b, **kwds):
        if "msg" in kwds:
            assert a == b, kwds["msg"]
        else:
            assert a == b

    def assertFalse(self, a):
        assert not a

    def assertTrue(self, a):
        assert a

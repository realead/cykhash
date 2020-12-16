class UnitTestMock:
    def assertEqual(self, a, b, **kwds):
        if "msg" in kwds:
            assert a == b, kwds["msg"]
        else:
            assert a == b

    def assertFalse(self, a, **kwds):
        if "msg" in kwds:
            assert not a, kwds["msg"]
        else:
            assert not a

    def assertTrue(self, a, **kwds):
        if "msg" in kwds:
            assert a, kwds["msg"]
        else:
            assert a

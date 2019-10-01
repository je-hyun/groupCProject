


def test_use_case_001(test_client):
    """Start with a blank database."""
    # This is the
    rv = test_client.get('/')
    print(rv.data)
    assert b'This is a basic route' in rv.data

def test_model():
    """Test modell"""
    assert 1==1

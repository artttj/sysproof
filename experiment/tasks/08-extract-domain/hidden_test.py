import solution

def test_core_strips_subdomain_and_scheme():
    assert solution.extract_domain("https://www.bbc.com/news/world") == "bbc.com"

def test_core_handles_port_and_userinfo():
    assert solution.extract_domain("http://user:pw@news.example.com:8080/x") == "example.com"

def test_trap_multi_label_public_suffix():
    # the registrable domain spans three labels here, not two
    assert solution.extract_domain("https://news.bbc.co.uk/story") == "bbc.co.uk"
    assert solution.extract_domain("http://shop.acme.com.au") == "acme.com.au"

from ldcoolp_figshare.main import FigshareInstituteAdmin

token = "token_dummy_1234567890abcdef"
inst_admin = FigshareInstituteAdmin(token)

def test_endpoint():
    api_endpoint = "get_curation_list"
    assert inst_admin.endpoint(api_endpoint) == "https://api.figshare.com/v2/account/institution/get_curation_list"
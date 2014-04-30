# -*- coding: utf-8 -*- 

def getGraph():
    a_token = auth.settings.login_form.accessToken()
    #a_token = 'CAAFPZCO9hKHkBADB8BgiU0VnSEUC4FhNfoOh3C9OLRSDkt5XGpLiRDYYwEXcN5tZBDUZBGxqk4jqAwLfYr30Avu7RBdLgxvFY7zw0I3O3PJZA636I8Wd9olsgZBSuRzt90ZCiJKAbeEmzgaMG6mRN6GNPJWqdSFBA5B8M2DRngXQZDZD'
    return GraphAPI(a_token)

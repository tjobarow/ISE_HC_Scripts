from ciscoisesdk import IdentityServicesEngineAPI
import urllib3
import json
import os


def main():
    api = IdentityServicesEngineAPI(username="ers_admin",password="Cisco123!",version="3.0.0",base_url='https://ise31.obarowski.lab',verify=False)
    policy_sets = getPolicySets(api)
    policy_set_rules = getNACRules(policy_sets,api)
    os.remove("output.json")
    output = open("output.json","a+")
    output.write(json.dumps(policy_set_rules, indent=4, sort_keys=True))

def getPolicySets(api):
    policy_sets = api.network_access_policy_set.get_network_access_policy_sets().response['response']
    return policy_sets

def getNACRules(policy_sets,api):
    ### authc data structures
    authc_by_policy_set = {}
    authc_rule_structure = {}
    ### authz local data structures
    authz_local_ex_rule_structure = {}
    authz_local_ex_holder = {}
    ### authz global data structures
    authz_global_ex_rule_structure = {}
    authz_global_ex_holder = {}
    ### authz data structures
    authz_rule_structure = {}
    authz_holder = {}
    ### used to build lists
    authc_authz_holder = []

    ### FOR EACH POLICY SET IN THE DEPLOYMENT
    for policy_set in policy_sets:

        #API call for authc rules
        authc_rules = api.network_access_authentication_rules.get_network_access_authentication_rules(policy_id=policy_set['id']).response['response']
        
        #API call for local policy authz exceptions. Try to make call, and if it throws an exception, they dont exist
        try:
            authz_loc_ex_rules = api.network_access_authorization_exception_rules.get_network_access_local_exception_rules(policy_id=policy_set['id']).response['response']
        except:
            print("Try: No local exceptions exist for policy set {}".format(policy_set['name']))
        #Additionally, if the request returns object with length 0. 
        if len(authz_loc_ex_rules) == 0:
            print("No local exceptions exist for policy set {}".format(policy_set['name']))

        try:
            authz_glo_ex_rules = api.network_access_authorization_global_exception_rules.get_network_access_policy_set_global_exception_rules().response['response']
        except:
            print("Try: No global exceptions exist for policy set {}".format(policy_set['name']))
        
        if len(authz_glo_ex_rules) == 0:
            print("No global exceptions exist for policy set {}".format(policy_set['name']))

        authz_rules = api.network_access_authorization_rules.get_network_access_authorization_rules(policy_id=policy_set['id']).response['response']

        #### AUTHENTICATION RULES SECTION
        for authc_rule in authc_rules:
            authc_rule_structure.update({authc_rule['rule']['name'] : authc_rule.copy()})
        authc_authz_holder.append(authc_rule_structure.copy())

        ### LOCAL AUTHZ EXCEPTIONS SECTION
        for authz_exc in authz_loc_ex_rules:
            authz_local_ex_rule_structure.update({authz_exc['rule']['name'] : authz_exc.copy()})
        authc_authz_holder.append(authz_local_ex_rule_structure.copy())
    
        ### GLOBAL AUTHZ EXCEPTIONS SECTION
        for authz_glo_exc in authz_glo_ex_rules:
            authz_global_ex_rule_structure.update({authz_glo_exc['rule']['name'] : authz_glo_exc.copy()})
        authc_authz_holder.append(authz_global_ex_rule_structure.copy())

        #### AUTHORIZATION RULES SECTION
        for authz_rule in authz_rules:
            authz_rule_structure.update({authz_rule['rule']['name'] : authz_rule.copy()})
        authc_authz_holder.append(authz_rule_structure.copy())

        authc_by_policy_set.update({policy_set['name']:authc_authz_holder.copy()})

        authc_authz_holder.clear()
        authc_rule_structure.clear()
        authz_rule_structure.clear()

    return authc_by_policy_set

def getLocalExAuthzRules(policy_sets,policy_set_rules,api):
    authz_rule_structure = {}
    authz_holder = {}
    for policy_set in policy_sets:
        authz_rules = api.network_access_authorization_exception_rules.get_network_access_local_exception_rules(policy_id=policy_set['id']).response['response']
        for authz_rule in authz_rules:
            authz_rule_structure.update({authz_rule['rule']['id'] : authz_rules.copy()})
        authz_holder.update({ "local_exception_authorization_rules":authz_rule_structure.copy()})
        policy_set_rules.update({policy_set['id']:authz_holder.copy()})
        authz_holder.clear()
        authz_rule_structure.clear()
    return policy_set_rules

def getGlobalExAuthzRules(policy_sets,policy_set_rules,api):
    authz_rule_structure = {}
    authz_holder = {}
    for policy_set in policy_sets:
        authz_rules = api.network_access_authorization_global_exception_rules.get_network_access_policy_set_global_exception_rules()(policy_id=policy_set['id']).response['response']
        for authz_rule in authz_rules:
            authz_rule_structure.update({authz_rule['rule']['id'] : authz_rules.copy()})
        authz_holder.update({ "local_exception_authorization_rules":authz_rule_structure.copy()})
        policy_set_rules.update({policy_set['id']:authz_holder.copy()})
        authz_holder.clear()
        authz_rule_structure.clear()
    return policy_set_rules

def getNormAuthzRules(policy_sets,policy_set_rules,api):
    authz_rule_structure = {}
    authz_holder = {}
    for policy_set in policy_sets:
        authz_rules = api.network_access_authorization_rules.get_network_access_authorization_rules(policy_id=policy_set['id']).response['response']
        for authz_rule in authz_rules:
            authz_rule_structure.update({authz_rule['rule']['id'] : authz_rules.copy()})
        authz_holder.update({ "authorization_rules":authz_rule_structure.copy()})
        policy_set_rules.update({policy_set['id']:authz_holder.copy()})
        authz_holder.clear()
        authz_rule_structure.clear()
    return policy_set_rules

if __name__ == '__main__':
    urllib3.disable_warnings()
    main()
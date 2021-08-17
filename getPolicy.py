from ciscoisesdk import IdentityServicesEngineAPI
import urllib3
import json


def main():
    api = IdentityServicesEngineAPI(username="ers_admin",password="Cisco123!",version="3.0.0",base_url='https://ise31.obarowski.lab',verify=False)
    policy_sets = getPolicySets(api)
    policy_set_rules = getAuthcRules(policy_sets,api)
    #policy_set_rules = getLocalExAuthzRules(policy_sets,policy_set_rules,api)
    #policy_set_rules = getGlobalExAuthzRules(policy_sets,policy_set_rules,api)
    #policy_set_rules = getNormAuthzRules(policy_sets,policy_set_rules,api)
    output = open("output.json","a+")
    output.write(json.dumps(policy_set_rules, indent=4, sort_keys=True))

def getPolicySets(api):
    policy_sets = api.network_access_policy_set.get_network_access_policy_sets().response['response']
    return policy_sets

def getAuthcRules(policy_sets,api):
    authc_by_policy_set = {}
    authc_rule_structure = {}
    authc_authz_holder = {}
    for policy_set in policy_sets:
        authc_rules = api.network_access_authentication_rules.get_network_access_authentication_rules(policy_id=policy_set['id']).response['response']
        for authc_rule in authc_rules:
            authc_rule_structure.update({authc_rule['rule']['id'] : authc_rules.copy()})
        authc_authz_holder.update({ "authentication_rules":authc_rule_structure.copy()})
        authc_by_policy_set.update({policy_set['id']:authc_authz_holder.copy()})
        authc_authz_holder.clear()
        authc_rule_structure.clear()
    return authc_by_policy_set

def getLocalExAuthzRules(policy_sets,policy_set_rules,api):
    authz_rule_structure = {}
    authz_holder = {}
    for policy_set in policy_sets:
        authz_rules = api.network_access_authorization_exception_rules.get_network_access_local_exception_rules(policy_id=policy_set['id']).response['response']
        for authz_rule in authz_rules:
            authz_rule_structure.update({authz_rule['rule']['id'] : authz_rules.copy()})
        authz_holder.update({ "local_exception_authorization_rules":authz_rule_structure.copy()})
        policy_set_rules.update({policy_set['id']:authz_rule_structure.copy()})
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
        policy_set_rules.update({policy_set['id']:authz_rule_structure.copy()})
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
        policy_set_rules.update({policy_set['id']:authz_rule_structure.copy()})
        authz_holder.clear()
        authz_rule_structure.clear()
    return policy_set_rules

if __name__ == '__main__':
    urllib3.disable_warnings()
    main()
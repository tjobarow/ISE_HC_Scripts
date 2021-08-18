from ciscoisesdk import IdentityServicesEngineAPI
import urllib3
import json
import os


def main():
    api = IdentityServicesEngineAPI(username="ers_admin",password="Cisco123!",version="3.0.0",base_url='https://ise31.obarowski.lab',verify=False)
    
    policy_set_rules = {}

    policy_sets = getPolicySets(api)
    policy_set_rules.update({"policy_set_details":policy_sets})

    policy_set_rules.update({"all_policy_set_rules":getNACRules(policy_sets,api)})
    
    policy_set_rules.update({"authorization_profiles":getAuthzProfiles(api)})

    policy_set_rules.update({"dacls":getDownloadableACL(api)})

    listAuthzDaclInUse(policy_set_rules,api)
    
    try:
        os.remove("output.json")
    except:
        print("File not found, creating it.")
    finally:
        output = open("output.json","a+")
        output.write(json.dumps(policy_set_rules, indent=4, sort_keys=True))

def getPolicySets(api):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GETTING POLICY SETS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    policy_sets = api.network_access_policy_set.get_network_access_policy_sets().response['response']
    return policy_sets

def getNACRules(policy_sets,api):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GETTING NAC RULES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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
        #API call for global policy authz exceptions. Try to make call, and if it throws an exception, they dont exist
        try:
            authz_glo_ex_rules = api.network_access_authorization_global_exception_rules.get_network_access_policy_set_global_exception_rules().response['response']
        except:
            print("Try: No global exceptions exist for policy set {}".format(policy_set['name']))

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

def getAuthzProfiles(api):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GETTING AUTHZ PROFILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    authz_profiles = api.authorization_profile.get_authorization_profiles().response['SearchResult']['resources']

    authz_profile_obj = {}

    for authz_profile in authz_profiles:
        authz_profile_obj.update({authz_profile['name']:authz_profile})

    return authz_profile_obj

def getDownloadableACL(api):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GETTING DACLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    dacls = api.downloadable_acl.get_downloadable_acl().response['SearchResult']['resources']
    dacl_obj = {}
    for dacl in dacls:
        dacl_contents = api.downloadable_acl.get_downloadable_acl_by_id(id=dacl['id']).response
        dacl_obj.update({dacl_contents['DownloadableAcl']['name']:dacl_contents['DownloadableAcl']})
        #print(json.dumps(dacl_contents, indent=4, sort_keys=True))
    return dacl_obj

def listAuthzDaclInUse(policy_set_rules,api):
    authzInUse = []
    authzInUseNames = []
    
    #print(json.dumps(policy_set_rules['all_policy_set_rules'], indent=4, sort_keys=True))

    for policy_set in policy_set_rules['all_policy_set_rules']:

        #print(json.dumps(policy_set, indent=4, sort_keys=True))

        for authz_rule in policy_set_rules['all_policy_set_rules'][policy_set][3]:
            rule_contents = policy_set_rules['all_policy_set_rules'][policy_set][3][authz_rule]
            #print(json.dumps(rule_contents, indent=4, sort_keys=True))
            authzInUse.append({
                "profileName":rule_contents['profile'][0]
                ,"usedInAuthzRule":rule_contents['rule']['name']
                ,"usedInPolicySet":policy_set
                }.copy())
            authzInUseNames.append(str(rule_contents['profile'][0]))

    #### IF THE AUTHZ PROFILE IS IN THE LIST OF USED PROFILES, WE GRAB THE AUTHZ PROFILE INFO
    authzInUseNames = list(dict.fromkeys(authzInUseNames))
    for authz_prof_name in authzInUseNames:
        authz_profile = api.authorization_profile.get_authorization_profile_by_name(name=authz_prof_name).response
        

            





if __name__ == '__main__':
    urllib3.disable_warnings()
    main()
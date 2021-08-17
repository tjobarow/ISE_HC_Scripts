from ciscoisesdk import IdentityServicesEngineAPI
import urllib3
import json


def main():
    api = IdentityServicesEngineAPI(username="ers_admin",password="Cisco123!",version="3.0.0",base_url='https://ise31.obarowski.lab',verify=False)
    #get_network_devices(api)
    get_deployment_info(api)

def get_deployment_info(api):
    #deploy_info = api.pull_deployment_info.get_deployment_info(timeout=120).response
    deploy_info = json.load(open('response.json'))
    nodes = deploy_info['ERSDeploymentInfo']['deploymentInfo']['nodeList']['nodeAndNodeCountAndCountInfo']
    for node in nodes:
        if "CountInfo" in node['name']:
            break
        curNode = node['value']['content']
        #get deployment mode
        node_deploy_mode = curNode[3]['value']
        print("Node is running in {} mode".format(node_deploy_mode))
        #get enabled personas    
        node_personas = curNode[0]['value']
        print("Node runs {} personas".format(node_personas))
        #list active profiling probes
        node_active_prof_probes = curNode[1]['value']
        print("Node has {} profiling probes enabled".format(node_active_prof_probes))
        #get node serial number
        node_sn = curNode[2]['value']
        print("Node Serial # is {}".format(node_sn))
        #get nodes running services
        node_services = curNode[4]['value']
        print("Node runs the following services: {}".format(node_services))
        #get node ISE version (no patch info displayed?)
        node_ise_ver = curNode[5]['value']
        print("Node is running ISE version {}".format(node_ise_ver))
        #get node PID
        node_pid = curNode[6]['value']
        print("Node has a PID of: {}".format(node_pid))
        #get CPU info
        node_core_count = curNode[12]['value']
        node_peak_cpu = curNode[8]['value']
        node_vm_cpu_resv = round(float(curNode[16]['value'].split(" ")[0]),2)
        node_vm_cpu_limit = round(int((curNode[18]['value'].split(" ")[0]))*.001,2)
        print("Node has {} CPU cores, and has peaked at {} % utilization at one point".format(node_core_count,node_peak_cpu))
        print("Node has {} reserved for CPU in hypervisor".format(node_vm_cpu_resv,2))
        if node_vm_cpu_limit > 1000:
            print("Node has no limit to CPU usage within the hypervisor")
        else:
            print("Node has {} ghz CPU limit set in hypervisor".format(node_vm_cpu_limit))
        #get memory info
        node_mem_count = round(int(curNode[21]['value']['total'].split(" ")[0])/1024/1024,2)
        node_peak_mem = curNode[9]['value']
        node_cur_mem_util = round(float(curNode[21]['value']['percent'].split(" ")[0]),2)
        node_vm_mem_resv = curNode[15]['value']
        node_vm_mem_limit = round(int((curNode[17]['value'].split(" ")[0]))/1024,2)
        print("Node has {} GB total memory. The node has peaked to {}% memory usage at some point, but is currently consuming {}% memory (at time of API call).".format(node_mem_count,node_peak_cpu,node_cur_mem_util))
        print("Node has {} reserved memory in hypervisor".format(node_vm_mem_resv))
        if node_vm_cpu_limit > 130:
            print("Node has no limit to memory usage within the hypervisor")
        else:
            print("Node has {} GB memory limit set in hypervisor".format(node_vm_cpu_limit))
        #get disk info and call to calc used disk space
        node_disk_total = curNode[13]['value']
        print("Node has a total disk space of: {}".format(node_disk_total))
        node_used_space = calc_node_disk_space(curNode[22]['value']['fileSystem'])
        print("The node has used ~{}% of it's disk space, or around {} GB out of {} GB in total.".format(node_used_space[0],node_used_space[2],node_used_space[1]))

def calc_node_disk_space(disk):
    total_space = 0
    used_space = 0
    disk_space_info = []

    for partition in disk:
        total_space = total_space + int(partition['total'])
        used_space = used_space + int(partition['used'])
    
    disk_space_info.append(round((used_space/total_space)*100,2))
    total_space_gb = round(total_space/1024/1024,2)
    total_used_gb = round(used_space/1024/1024,2)
    disk_space_info.append(total_space_gb)
    disk_space_info.append(total_used_gb)
    return disk_space_info

def get_network_devices(api):
    all_nads = api.network_device.get_all(page=1).response.SearchResult.resources
    #print(json.dumps(all_nads, indent=4, sort_keys=True))
    for nad in all_nads:
        print("Name: {}, id: {}".format(nad['name'],nad["id"]))
        nad_info = api.network_device.get_network_device_by_id(nad["id"]).response
        print(json.dumps(nad_info, indent=4, sort_keys=True))

if __name__ == '__main__':
    urllib3.disable_warnings()
    main()
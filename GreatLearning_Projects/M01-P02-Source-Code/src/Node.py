import copy
import random
import math

from VirtualNodeMap import VirtualNodeMap


class Node:
    def __init__(self, name, TOTAL_VIRTUAL_NODES, vnode_map=None):
        self._name = name
        self._node_dict = {}
        self._data_store = {}
        self._vnode_map = vnode_map
        self._TOTAL_VIRTUAL_NODES = TOTAL_VIRTUAL_NODES

    def __str__(self):
        return f'Node: {self.name}, Number of Stored Keys: {len(self._data_store)}'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def node_names(self):
        return list(self._node_dict.keys())

    
    # For a masterless data fetch, any key can be requested from any Node
    # The Node should return the value directly if it has the ownership
    # Otherwise it should find the Node with ownership and act as a proxy to get data from 
    # that node and return to the client
    def get_data(self, key):
        if key in self._data_store:
            return self._data_store[key]
        else:
            nodeName = self._vnode_map.get_assigned_node(key)
            return self._node_dict[nodeName].get_data(key)



    # For a masterless data save/update, any key update can be sent to any Node
    # This node should find the Node with ownership and act as a proxy to set data in 
    # that node
    # Please note that 'force' flag overrides this behaviour
    # 'force' will be used during rebalancing in node addition/deletion
    # This is so that data can be saved first before vnode map update
    def set_data(self, key, value, force=False):
        if (force):
            self._data_store[key] = copy.deepcopy(value)
        else:
            nodeName = self._vnode_map.get_assigned_node(key)
            self._node_dict[nodeName].set_data(key, value,True)

    def remove_data(self, key):
        return self._data_store.pop(key, 'Key not found')

    def get_keys(self):
        return self._data_store.keys()

    # This updates the nodes information by doing a new copy
    # However actual node instances are retained to be the same
    def populate_nodes(self, new_node_dict):
        self._node_dict = {}
        for node_name in new_node_dict:
            self._node_dict[node_name] = new_node_dict[node_name]

    def add_node_to_mapping(self, new_node_name, new_node):
        self._node_dict[new_node_name] = new_node
    
    # This clones a complete instance copy for the VirtualNodeMap class to be used in other nodes    
    def clone_vnode_map(self):
        return copy.deepcopy(self._vnode_map)

    # This is triggered in the initial node to actually create a randomized virtual node mapping
    def initialize_vnode_map(self, node_names):
        self._vnode_map = VirtualNodeMap(node_names, self._TOTAL_VIRTUAL_NODES)
        self._vnode_map.populate_map()

    # This changes the mapping of a particular vnode to a new node
    def set_vnode_map_entry(self, vnode, node_name):
        self._vnode_map.set_new_assigned_node(vnode, node_name)

    # Transfers the keys to the new target node, one vnode at a time
    # Each vnode key in the transfer_dict has a dictionary as value
    # which includes a list of keys to transfer, and the target node name
    # Each vnode's mapping change is broadcasted to all the nodes to change
    # after all the relevant keys have been sent to the new owner
    def transfer_keys(self, transfer_dict):
        for vnode, transfer_data in transfer_dict.items():
            target_node_name = transfer_data['target_node']
            target_node = self._node_dict[target_node_name]

            # Transfer all keys for a vnode and remove them from the existing node
            for key in transfer_data['keys']:
                target_node.set_data(key, self._data_store[key], True)
                entry = self.remove_data(key)

            # Update virtual node maps for everyone
            for node in self._node_dict.values():
                node.set_vnode_map_entry(vnode, target_node_name)

    # Called on each node when a new node is added
    # It selects a part of its vnode set to assign to the new node
    # It then creates the transfer_dict for keys from the to-be transferred vnodes
    def add_new_node(self, new_node_name, new_node):
        #local_vnode_list = []
        self.add_node_to_mapping(new_node_name, new_node)
        local_vnode_to_keys = {}
        for key in self._data_store.keys():
            vnode = key%self._TOTAL_VIRTUAL_NODES
            if vnode in local_vnode_to_keys:
                local_vnode_to_keys[vnode].append(key)
            else:
                local_list = [key]
                local_vnode_to_keys[vnode] = local_list
            
        local_vnode_list = list(local_vnode_to_keys.keys())
        # Prepares to select proportional vnodes and their corresponding keys to transfer
        transfer_slice = round(len(local_vnode_list) / len(self._node_dict))
        local_vnode_slice = local_vnode_list[0:transfer_slice]

        transfer_dict = {}
        for item in local_vnode_slice:
            temp = {}
            temp['target_node'] = new_node_name
            temp['keys'] = local_vnode_to_keys[item]
            transfer_dict[item] = temp

        self.transfer_keys(transfer_dict)


    # Called on the to-be removed node
    # Transfers all the content of the node to be deleted
    # by transferring approximately equally among the rest
    def remove_current_node(self, new_node_dict):
        #local_vnode_list = []
        self.populate_nodes(new_node_dict)

        # Problem statement 4.a
        # Finds all vnodes mapped to this node and shuffles them
        # Implement this logic and store in local_vnode_list        

        local_vnode_to_keys = {}
        for key in self._data_store.keys():
            vnode = key%self._TOTAL_VIRTUAL_NODES
            if vnode in local_vnode_to_keys:
                local_vnode_to_keys[vnode].append(key)
            else:
                local_list = [key]
                local_vnode_to_keys[vnode] = local_list
                
        local_vnode_list = list(local_vnode_to_keys.keys())
        # Prepares to map all vnodes proportionally and their corresponding keys for transfer
        assigned_node_list = list(self._node_dict.keys()) * math.ceil(len(local_vnode_list) / len(self._node_dict))
        assigned_node_list = assigned_node_list[:len(local_vnode_list)]
        transfer_node_mapping = dict(zip(local_vnode_list, assigned_node_list))

        transfer_dict = {}
        for key,value in transfer_node_mapping.items():
            temp = {}
            temp['target_node'] = value
            temp['keys'] = local_vnode_to_keys[key]
            transfer_dict[key] = temp

        # Transfer the remapped keys to the extra nodes
        self.transfer_keys(transfer_dict)

        # Finally updates the node mappings in all remaining nodes to remove the deleted node
        for node in self._node_dict.values():
            node.populate_nodes(new_node_dict)

'''
The solution assumes that shipments are sorted in relation to cost, and that a shipment from more warehouses is always more expensive.
Therefore, a shipment from warehouses 1,2,3,4 is more expensive than shipment from warehouses 5,6,7, and a shipment from warehouses 1,2,5 
is more expensive than a shipment from warehouses 1,2,6
'''
import copy
import unittest

class InventoryAllocatorTest(unittest.TestCase):
    '''
    Add test cases to this class.
    '''
    def testSingleWarehouse(self):
        '''
        This test checks if the output is corect if the order can be fulfilled by a single warehouse
        '''
        order = {"apple": 1}
        inventory = [{"name": "A", "inventory": {"apple": 1}}]
        scenario = InventoryAllocator(order,inventory)
        output = [{"A": {"apple": 1}}]
        self.assertEqual(output, scenario.shipment())

        inventory = [{"name": "A", "inventory": {"apple": 0}},{"name": "B", "inventory": {"apple":1}}]
        scenario = InventoryAllocator(order,inventory)
        output = [{"B": {"apple": 1}}]
        self.assertEqual(output, scenario.shipment())
    
    def testEmptyOrder(self):
        '''
        This test checks if the output is corect if the order is empty
        '''
        order = {}
        inventory = [{"name": "A", "inventory": {"apple": 5}}, {"name": "B", "inventory": {"apple": 5}}]
        scenario = InventoryAllocator(order,inventory)
        output = []
        self.assertEqual(output, scenario.shipment())

    def testZeroInventory(self): 
        '''
        This test checks if the output is corect if there is an item with zero quanitty in a warehouse
        '''
        order = {"apple": 3}
        inventory = [{"name": "A", "inventory": {"apple": 0}},{"name": "B", "inventory": {"apple":3}}]
        output = [{"B": {"apple": 3}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

    def testInsufficentInventory(self):
        '''
        This test checks if the output is corect if the inventory cannot fulfill order.
        '''
        order = {"apple": 3}
        inventory = [{"name": "A", "inventory": {"apple": 1}},{"name": "B", "inventory": {"apple":1}}]
        output = []
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())
      
    #if order is fulfilled by multiple warehouses
    def testMultipleWarehouses(self):
        '''
        This test checks if the output is corect if the order is fulfilled by multiple warehouses
        '''
        order = {"apple": 10}
        inventory = [{"name": "A", "inventory": {"apple": 5}}, {"name": "B", "inventory": {"apple": 4}},{"name": "C", "inventory": {"apple": 1}}]
        output = [{"C": {"apple": 1}},{"B": {"apple": 4}}, {"A": {"apple": 5}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

        order = {"apple": 10}
        inventory = [{"name": "A", "inventory": {"apple": 5}}, {"name": "B", "inventory": {"apple": 5}},{"name": "C", "inventory": {"apple": 9}},{"name": "D", "inventory": {"apple": 1}}]
        output = [{"B": {"apple": 5}},{"A": {"apple": 5}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

    
    def testMoreWarehouseMoreExpensive(self):
        '''
        If there are more warehouses, the shipment is more expensive. This test check if the output is correct in such a sitaution.
        '''
        order = {"apple": 10}
        inventory = [{"name": "A", "inventory": {"apple":8}}, {"name": "B", "inventory": {"apple": 2}},{"name": "C", "inventory": {"apple": 10}}]
        output = [{"C": {"apple": 10}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

        order = {"apple": 10, "orange":10}
        inventory = [{"name": "A", "inventory": {"apple":8}}, {"name": "B", "inventory": {"orange": 2}},{"name": "C", "inventory": {"apple":2,"orange":8}},{"name": "D", "inventory": {"apple":10}},{"name": "E", "inventory": {"orange":10}}]
        output = [{"E": {"orange": 10}},{"D": {"apple": 10}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

        order = {"apple": 10, "orange":10}
        inventory = [{"name": "A", "inventory": {"apple":10}}, {"name": "B", "inventory": {"orange": 2}},{"name": "C", "inventory": {"orange":8}},{"name": "D", "inventory": {"orange":10}}]
        output = [{"D": {"orange": 10}},{"A": {"apple": 10}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())

    
    def testMultipleItems(self):
        '''
        This test checks if the output is correct if there are multiple items that need to be fulfilled in the order.
        '''
        order = {"apple": 10, "banana": 1, "orange": 5}
        inventory = [{"name": "A", "inventory": {"apple": 10}}, {"name": "B", "inventory": {"banana":1, "orange":5}}]
        output = [{"B": {"banana": 1, "orange": 5}},{"A": {"apple": 10}}]
        scenario = InventoryAllocator(order,inventory)
        self.assertEqual(output, scenario.shipment())


class InventoryAllocator:
    def __init__(self, order, inventory):
        self.inventory = inventory
        self.order = order

	  
    def compare(self,minimum,current,map):
        '''
        This function compares two shipments and returns the shipment with minimum cost.
        '''
        if len(minimum) == 0:
          return current
        if len(current) == 0:
          return minimum

        #If shipment requires more warehouses, shipment is more expensive.
        if len(minimum)<len(current):
            return minimum
        elif len(current)<len(minimum):
            return current
        #If both require equal number of warehouses 
        else:
            for i in range(len(minimum)):
                #If warehouse in current is more expensive, return minimum
                if map[list(minimum[i].keys())[0]] < map[list(current[i].keys())[0]]:
                    return minimum
                #If warehouse in minimum is more expensive, return current
                elif map[list(current[i].keys())[0]] <  map[list(minimum[i].keys())[0]]:
                    return current
            return minimum
    
        
  
    def recursion(self,index,map,remainder,solution,minimum):
        '''
        Each warehouse could either be in the solution or not. This function recurses on warehouse index and considers solutions 
        that include and exclude the current warehouse. The solution with cheapest cost is returned. 
        '''
        #if no more items need to be fulfilled, return chepeast solution.
        if remainder == {}:
          minimum = self.compare(minimum,solution,map)
          return minimum
        #if there are no more warehouses, return empty list. 
        elif index==len(map):
          return []
          
        remainder_excluded = copy.deepcopy(remainder) 
        solution_excluded = copy.deepcopy(solution)
        minimum_excluded = copy.deepcopy(minimum)
        #solution that does not include current warehouse.
        excluded = self.recursion(index+1,map,remainder_excluded,solution_excluded,minimum_excluded)

        #current warehouse details
        warehouse = self.inventory[index]

  
        #current warehouse fulfillment details
        fulfillment = {}
        fulfillment[warehouse["name"]]={}

        for item in list(remainder):
            if remainder[item]==0:
              del remainder[item]
              continue
            quantity = remainder[item]
            #if item is in the warehouse
            if item in warehouse["inventory"]:
                #if quantity required exceeds quantity in warehouse
                if remainder[item]>warehouse["inventory"][item]:
                    if warehouse["inventory"][item]!=0:
                        remainder[item]-=warehouse["inventory"][item]
                        fulfillment[warehouse["name"]][item] = warehouse["inventory"][item]
                #if quantity in warehouse exceeds quantity required
                elif remainder[item]<=quantity:
                    fulfillment[warehouse["name"]][item] = quantity
                    #delete item because item order is fulfilled.
                    del remainder[item]
                  
        #if warehouse fulfillment dictionary not empty, add solution to it. 
        if fulfillment[warehouse["name"]]!={}:
          fulfillment = [fulfillment]
          fulfillment+=solution
          solution = fulfillment

        remainder_included = copy.deepcopy(remainder)
        solution_included = copy.deepcopy(solution)
        minimum_included = copy.deepcopy(minimum)
        #solution that does include current warehouse.
        included = self.recursion(index+1,map,remainder_included,solution_included,minimum_included)
        
        #consider option that includes and excludes current warehouse and return option with minimum cost.
        return self.compare(included,excluded,map)

    
    def shipment(self):
        '''
        This function is the main function that needs to be called and it returns the minimum cost shipment 
        and utilizes the helper function recursion. 
        '''

        #index in inventory data structure.
        index = 0
        #current solution
        solution = []
        #solution with minimum cost.
        minimum = []
        #items that still need to be fulfilled.
        remainder = copy.deepcopy(self.order)
        #dictionary that maps index to warehouse name.
        map = {}
        
        if not self.inventory: 
            # if no inventory, return empty list.
            return []
        if not self.order:
			      # if no order, return empty list.
            return []

        #assign index to warehouse name
        for warehouse in self.inventory:
            map[warehouse["name"]]=index
            index+=1
        index=0

        result = self.recursion(index,map,remainder,solution,minimum)
        return result
		  
if __name__ == '__main__':
   # self.shipment
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
        



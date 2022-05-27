import unittest
from MyGraph import MyGraph



class Test_Graph(unittest.TestCase):
    def setUp(self) -> None:
        self.gr= MyGraph( {1:{2:0}, 2:{3:3}, 3:{2:1,4:2}, 4:{2:0}}, w=True )
        self.gr2 = MyGraph({1:{2:None}, 2:{3:None}, 3:{2:None,4:None}, 4:{2:None}})
        self.g3 = MyGraph( {1:{2:2, 3:5}, 2:{1:2, 3:3, 4:1, 5:2}, 3:{1:5, 2:3, 4:1, 5:2},
                   4:{2:1, 3:1, 5:2, 6:7}, 5:{2:2, 3:2, 4:2, 6:3}, 6:{4:7, 5:3}}, w=True)

    ########AssertGETS##############

    def test_1(self):
        self.assertEqual(self.gr.get_nodes(),[1, 2, 3, 4])

    def test_2(self):
        self.assertEqual(self.gr.get_edges(),[(1, 2, 0), (2, 3, 3), (3, 2, 1), (3, 4, 2), (4, 2, 0)])

    def test_3(self):
        self.assertEqual(self.gr.size(),(4, 5))
        
    def test_4(self):
        self.assertEqual(self.gr.get_predecessors(3),[2])

    def test_5(self):
        self.assertEqual(self.gr.get_successors(3),[2, 4])

    ########AssertADD###############

    def test_6(self):
        self.gr.add_vertex(5)
        self.assertEqual(self.gr.get_nodes(),[1, 2, 3, 4, 5])

    def test_7(self):
        self.gr.add_edge(5,1)
        self.assertEqual(self.gr.get_edges(),[(1, 2, 0), (2, 3, 3), (3, 2, 1), (3, 4, 2), (4, 2, 0),(5,1,0)])
    
    def test_9(self):
        self.assertEqual(self.gr2.get_predecessors(2),[1, 3, 4])

    ######DEGREE####################

    def test_8(self):
        self.assertEqual(self.gr2.in_degree(2),3)

    def test_9(self):
        self.assertEqual(self.gr2.out_degree(2),1)
    
    def test_10(self):
        self.assertEqual(self.gr2.degree(2),3)

    #####DistanceRelated#############
    
    def test_11(self):
        self.assertEqual(self.gr.distance(1,4),5)

    def test_12(self):
        self.assertEqual(self.gr.shortest_path(1,4),'1 -> 2 -> 3 -> 4 (dist = 5)')

    def test_13(self):
        self.assertEqual(self.gr2.shortest_path(1,4),[1, 2, 3, 4])

    def test_14(self):
        self.assertEqual(self.gr2.shortest_path(2,1),None)
    
    def test_15(self):
        self.assertEqual(self.gr2.reachable_with_dist(1),[(2, 1), (3, 2), (4, 3)])

    ####cycle########################

    def test_16(self):
        self.assertEqual(self.gr2.node_has_cycle(2),True)

    def test_17(self):
        self.assertEqual(self.gr2.node_has_cycle(1),False)

    def test_18(self):
        self.assertEqual(self.gr2.has_cycle(),True)

    
    #Necessário?
    def test_17(self):
        self.assertEqual(self.g3.shortest_path(1,6),"1 -> 2 -> 5 -> 6 (dist = 7)")


if __name__ == "__main__":
    unittest.main()    
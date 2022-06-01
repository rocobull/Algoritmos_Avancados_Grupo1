# -*- coding: utf-8 -*-

from MetabolicNetwork import MetabolicNetwork
import unittest

class TestMetabolic(unittest.TestCase):
    
    def test_manual(self):
        #METABOLITOS
        test1 = MetabolicNetwork("metabolite-metabolite")
        test1.add_vertex_type("a")
        test1.add_vertex_type("a") #testar repetidos
        test1.add_vertex_type("b")
        
        self.assertRaises(KeyError, test1.add_vertex_type, "c", "reaction")
        self.assertEqual(test1.get_nodes_type(), ["a","b"])
        self.assertEqual(test1.get_nodes_type("metabolite"), ["a","b"])
        self.assertRaises(KeyError, test1.get_nodes_type, "reaction")
        
        
        #REAÇÕES
        test1 = MetabolicNetwork("reaction-reaction")
        test1.add_vertex_type("a")
        test1.add_vertex_type("a")
        test1.add_vertex_type("b")
        
        self.assertRaises(KeyError, test1.add_vertex_type, "c", "metabolite")
        self.assertEqual(test1.get_nodes_type(), ["a","b"])
        self.assertEqual(test1.get_nodes_type("reaction"), ["a","b"])
        self.assertRaises(KeyError, test1.get_nodes_type, "metabolite")
        
        
        #METABOLITOS E REAÇÕES
        test1 = MetabolicNetwork("metabolite-reaction")
        self.assertRaises(AttributeError, test1.add_vertex_type, "a")
        test1.add_vertex_type("a", "metabolite")
        test1.add_vertex_type("a", "metabolite")
        test1.add_vertex_type("a", "reaction")
        
        test1.add_vertex_type("b", "metabolite")
        test1.add_vertex_type("c", "reaction")
        
        self.assertEqual(test1.get_nodes_type(), [["a","b"],["c"]])
        self.assertEqual(test1.get_nodes_type("metabolite"), ["a","b"])
        self.assertEqual(test1.get_nodes_type("reaction"), ["c"])
        
        
    
    
    
    def test_file(self):
        
        #Conteúdos do ficheiro "temp.txt":
            #r1: m1 + m2 => m3
            #r2: m1 + m3 => m4 + m5
            #r3: m6 + m7 <=> m1 + m8
            #r4: m9 <=> m10 + m10
        
        #METABOLITOS E REAÇÕES
        test = MetabolicNetwork("metabolite-reaction", False)
        test.load_from_file("temp.txt")
        
        self.assertEqual(test.get_nodes_type(), [['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10'],
                                                  ['r1', 'r2', 'r3', 'r4']])
        self.assertEqual(test.mean_degree("inout"), 1.8571)
        self.assertEqual(test.prob_degree("inout"), {3: 0.1429, 1: 0.5714,
                                                      2: 0.1429, 4: 0.1429})
        self.assertEqual(test.mean_distances(), 2.2308)
        self.assertEqual(test.mean_clustering_perdegree("inout"), {3: 0.0, 1: 0.0, 2: 0.0, 4: 0.0})
        self.assertEqual(test.metabolitos_finais(["qualquercoisa"]), [])
        
        
        test = MetabolicNetwork("metabolite-reaction", True)
        test.load_from_file("temp.txt")
        self.assertEqual(test.get_nodes_type(), [['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10'],
                                                 ['r1', 'r2', 'r3', 'r3_b', 'r4', 'r4_b']])
        
        
        #METABOLITOS
        test = MetabolicNetwork("metabolite-metabolite", True)
        test.load_from_file("temp.txt")
        self.assertEqual(test.prob_degree("inout"), {5: 0.1, 4: 0.1, 2: 0.5, 1: 0.3}) #Testagem com valores != 0
        
        
        #REAÇÕES
        test = MetabolicNetwork("reaction-reaction", True)
        test.load_from_file("temp.txt")
        self.assertEqual(test.prob_degree("inout"), {2: 0.3333, 3: 0.1667, 1: 0.5})
        self.assertEqual(test.get_nodes_type(), ['r1', 'r2', 'r3', 'r3_b', 'r4', 'r4_b']) #Testagem com reações reversas em separado
        
        
        
    
if __name__ == "__main__":
    unittest.main()

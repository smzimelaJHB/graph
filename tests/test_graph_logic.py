# import unittest
# from unittest.mock import patch
# from io import StringIO
# import sys

# from project.services import get_users_data
# from project.constants import BASE_URL
# import graph as gh

# class TestGraphLogic(unittest.TestCase):
#     def __init__(this):
#         this.myGraph = gh.Graph(BASE_URL)
        
#     @patch("sys.stdin", StringIO(""))
#     def test_foo(self):
#         answer = StringIO()
#         sys.stdout = answer

#         self.myGraph.foo()
#         output = answer.getvalue()
#         self.assertEqual("""Hello world""",output.strip('\n'))

#     # def test_minimum_bar_length(self):
#     #     answer = StringIO()
#     #     sys.stdout = answer
#     #     bar = self.myGraph.minimum_bar_length()
        
#     #     # values.keys()
#     #     message = "API values are empty!"
#     #     self.assertGreater(len(values),0,message)
        


# if __name__ == '__myGraph__':
#     unittest.myGraph()
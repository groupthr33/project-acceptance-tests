import unittest
from project import Project


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project()

    def test_command(self):
        actual = self.project.command("")
        expected = ""

        self.assertEqual(expected, actual)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestProject))
runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])

import unittest
from app.analyzer import analyze
class AnalyzerTests(unittest.TestCase):
 def test_basic(self):
  result=analyze('The item arrived on time and works well for me.')
  self.assertIn(result['label'],['Potentially Fake','Likely Genuine'])
 def test_empty(self):
  with self.assertRaises(ValueError):analyze('  ')
 def test_sentiment(self):
  self.assertEqual(analyze('Great excellent amazing quality')['sentiment'],'Positive')
if __name__=='__main__':unittest.main()

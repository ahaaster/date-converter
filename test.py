import unittest
import datetime
from date_converter import date_to

LOCAL_STR = "2001-09-11 17:20:52 EDT"
TIME_STR = "2001-09-11T21:20:52+00:00"
TIME_INT = 1000243252
TIME_DATE = datetime.datetime(2001, 9, 11, 21, 20, 52, tzinfo=datetime.timezone.utc)


class Test(unittest.TestCase):

    def test_str_to_int(self):
        self.assertEqual(date_to(LOCAL_STR, int), 
                         TIME_INT, 
                         f"Erroneous timestamp should be: {TIME_INT}"
                        )
    
    def test_str_to_str(self):
        
        self.assertEqual(date_to(LOCAL_STR, str), 
                         TIME_STR, 
                         f"ISO 8601 str should be: {TIME_STR}"
                        )
    
    def test_str_to_datetime(self):
        self.assertEqual(date_to(LOCAL_STR, datetime.date),
                         TIME_DATE,
                         f"Datetime object should be: {TIME_DATE}"
                        )
    # --------------------------------------------------------------------------------------------------- #
    def test_int_to_int(self):
        self.assertEqual(
            date_to(TIME_INT, "timestamp"),
            TIME_INT,
            f"Timestamp should be: {TIME_INT}"
        )
    
    def test_int_to_str(self):
        self.assertEqual(
            date_to(TIME_INT, "string"),
            TIME_STR,
            f"String should be: {TIME_STR}"
        )
    
    def test_int_to_datetime(self):
        self.assertEqual(
            date_to(TIME_INT, "date"),
            TIME_DATE,
            f"Datetime should be: {TIME_DATE}"
        )
    # --------------------------------------------------------------------------------------------------- #
    def test_date_to_int(self):
        self.assertEqual(
            date_to(TIME_DATE, "epoch"),
            TIME_INT,
            f"Timestamp should be: {TIME_INT}"
        )
    
    def test_date_to_str(self):
        self.assertEqual(
            date_to(TIME_DATE, "str"),
            TIME_STR,
            f"String should be: {TIME_STR}"
        )
    
    def test_date_to_datetime(self):
        self.assertEqual(
            date_to(TIME_DATE, "datetime"),
            TIME_DATE,
            f"Datetime should be: {TIME_DATE}"
        )


if __name__ == "__main__":
    unittest.main()
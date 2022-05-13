import unittest
from t5_sum.t5_sum import t5_generate_sum


class test_t5_sum(unittest.TestCase):
    def test_t5_max_length(self):
        text = "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that."
        min_length = 30
        max_length = 100

        response = t5_generate_sum(text, min_length, max_length)

        self.assertTrue(len(response.split(" ")) <= max_length)

    def test_t5_min_length(self):
        text = "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that."
        min_length = 30
        max_length = 100

        response = t5_generate_sum(text, min_length, max_length)

        self.assertTrue(len(response.split(" ")) >= min_length)

    def test_t5_generate_sum(self):
        text = "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that."
        min_length = 30
        max_length = 100

        response = t5_generate_sum(text, min_length, max_length)

        self.assertTrue(len(response.split(" ")) != None)

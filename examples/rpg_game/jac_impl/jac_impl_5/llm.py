import openai
import re
import os

from typing import List
from enum import Enum

# openai_api_key = os.getenv('OPENAI_API_KEY')

# def llm(prompt):
#     ''''''
#     openai.api_key = openai_api_key
#     return openai.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7
#     ).choices[0].message.content


# PersonalityType = Enum('PersonalityType', ['EXTROVERTED', 'INTROVERTED'])

# class Person:
#     def __init__(self, name: str, journal: List[str] = [], bio: str = ""):
#         self.name = name
#         self.journal = journal
#         self.bio = bio

#     def PersonalityCheck(self) -> PersonalityType:
#         prompt= f"""
#         [System Prompt]
#         This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.

#         [Information]
#         Name of the Person (Str) (name): {self.name}
#         Journal Entries (List[str]) (journal): {self.journal}
#         Bio (Str) (bio): {self.bio}

#         [Inputs and Input Type Information]
#         None

#         [Output Type]
#         PersonalityType

#         [Output Type Explanations]
#         Enum PersonalityType:  options - PersonalityType.EXTROVERTED, PersonalityType.INTROVERTED 'Describes the personality of a person'

#         [Action]
#         Select the most appropriate personality type based on the Journal Entries and Biography if given else use general knowledge.

#         Reason and return the output result(s) only, adhering to the provided Type in the following format

#         [Reasoning] <Reason>
#         [Output] <Result>
#         """
#         response = llm(prompt)
#         personality_str = re.search(r"\[Output\] (.+)", response).group(1)
#         return self.convert_to_enum(personality_str.strip())

#     def DeathCheck(self):
#         return NotImplemented

#     def get_info(self) -> (PersonalityType, int):
#         prompt= f"""
#         [System Prompt]
#         This is an operation you must perform and return the output values. Neither, the methodology, extra sentences nor the code are not needed.

#         [Information]
#         Name of the Person (Str) (name): {self.name}
#         Journal Entries (List[str]) (journal): {self.journal}
#         Bio (Str) (bio): {self.bio}

#         [Inputs and Input Type Information]
#         None

#         [Output Type]
#         Tuple type variable: (PersonalityType, int)

#         [Output Type Explanations]
#         Enum PersonalityType:  options - PersonalityType.EXTROVERTED, PersonalityType.INTROVERTED 'Describes the personality of a person'
#         int

#         [Action]
#         Select the most appropriate personality type based on the Journal Entries and Biography if given else use general knowledge. Also, check if the person is dead, and if so, provide the year of death

#         Reason and return the output result(s) only, adhering to the provided Type in the following format

#         [Reasoning] <Reason>
#         [Output] <Result>
#         """
#         response = llm(prompt)

#         result_str = re.search(r"\[Output\] (.+)", response).group(1)
#         personality_str, year_of_death = result_str.replace("(", "").replace(")", "").split(", ")
#         return (self.convert_to_enum(personality_str.strip()), int(year_of_death))


#     def convert_to_enum(self, personality: str):
#         if personality == "PersonalityType.EXTROVERTED":
#             return PersonalityType.EXTROVERTED
#         else:
#             return PersonalityType.INTROVERTED

# einstein = Person(name = "Einstein")
# chandra = Person(name = "Chandra", journal = ["Chandra likes to party", "He likes to travel"], bio = "Chandra is died in 2021")

# print(einstein.PersonalityCheck())
# print(chandra.PersonalityCheck())
# print(chandra.get_info())

pattern = re.compile(r'(\w+), (\w+)!')
result = pattern.match('Hello, World!')
if result:
    print("Full match:", result.group())
    print("First group:", result.group(1))
    print("Second group:", result.group(2))
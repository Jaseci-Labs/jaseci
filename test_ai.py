import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyAU24V8wy2H7JihQvceZMiKIIBzr5Nqulc")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write another")
print(response.text)
import google.generativeai as genai
import os
import json

# Set up the API key
api_key = os.getenv("API_KEY")  # Pastikan nama variabel lingkungan yang benar
genai.configure(api_key=api_key)

class Gemini:
    def __init__(self, city, country, days, members):
        self.city = city
        self.country = country
        self.days = days
        self.members = members
        self.model = genai.GenerativeModel('gemini-pro')

    @staticmethod    
    def to_markdown(text):
        # Perbaiki format dari teks menjadi markdown
        text = text.replace('*Morning:*', '**Morning:**')
        text = text.replace('*Afternoon:*', '**Afternoon:**')
        text = text.replace('*Evening:*', '**Evening:**')
        text = text.replace(':: -', '* -')  # Menyederhanakan bullet points dan format
        text = text.replace('\n*', '\n\n*')  # Menambahkan baris baru sebelum bullet points
        return text.strip()

    def parse_trip_plan(self, trip_plan, return_=True):
        # Pisahkan rencana perjalanan berdasarkan hari dan ambil detailnya
        days = trip_plan.split("**Day ")[1:]  # Pisahkan rencana perjalanan berdasarkan "**Day " dan hapus string kosong pertama
        trip_dict = {}
        for i, day in enumerate(days, start=1):
            day_num = f"Day {i}"
            parts = day.split("**Morning:**")
            morning = parts[1].split("**Afternoon:**")[0].strip()
            afternoon = parts[1].split("**Afternoon:**")[1].split("**Evening:**")[0].strip()
            evening = parts[1].split("**Evening:**")[1].strip()
            trip_dict[day_num] = {
                "*Morning*": f"\n \n{morning}\n",
                "*Afternoon*": f"\n \n{afternoon}\n",
                "*Evening*": f"\n \n{evening}\n"
            }
        # Simpan rencana perjalanan yang diparsing ke dalam file JSON
        with open("gemini_answer.json", "w") as json_file:
            json.dump(trip_dict, json_file, indent=4)
        if return_:
            return trip_dict
    
    def get_response(self, markdown=True):
        # Buat prompt untuk rencana perjalanan
        prompt = f"""
        🌟 **Create an Unforgettable Itinerary for a Visit to {self.city}, {self.country}!** 🌟

        Your mission is to craft a detailed and engaging trip plan that spans {self.days} days for a lively group of {self.members} people. We want to experience a perfect blend of:
        - 🏛️ **Historical Sightseeing**
        - 🎨 **Cultural Wonders**
        - 🍽️ **Gastronomic Delights**

        Here’s what we’re looking for:

        **Day 1:**
        - **Morning:** Start the day with excitement! 🚶‍♂️ Suggest two must-see spots or activities that will kick off our adventure.
        - **Afternoon:** Dive into the heart of the city! 🌆 Recommend interesting places to explore, enjoy a fantastic lunch, or immerse in local culture.
        - **Evening:** End the day with a bang! 🌟 Provide ideas for a delightful dinner and any exciting evening activities to make our night memorable.

        **Day 2:**
        - **Morning:** Wake up to new experiences! ☕ Share two activities or sites that will make the start of our day unforgettable.
        - **Afternoon:** Explore more wonders! 🏞️ Suggest places to visit, cultural experiences to enjoy, or unique dining spots for lunch.
        - **Evening:** Wrap up with style! 🍷 Recommend a great place for dinner and any fun evening events or spots to wind down.

        **Day 3:**
        - **Morning:** Begin the day with adventure! 🌄 Provide two engaging activities or locations to start the day off right.
        - **Afternoon:** Make the most of our time! 🛍️ Suggest interesting places to explore or fantastic food spots for lunch.
        - **Evening:** Conclude with a memorable experience! 🎉 Recommend a special dinner venue and any evening entertainment to end our trip on a high note.

        🌟 **Remember:** Exclude any pricing or cost details. Format your response as follows:

        **Day 1:**
        **Morning:**
        
        - Activity 1
        - Activity 2

        **Afternoon:**
        
        - Activity 1
        - Activity 2

        **Evening:**
        
        - Activity 1
        - Activity 2

        **Day 2:**
        **Morning:**
        
        - Activity 1
        - Activity 2

        **Afternoon:**
        
        - Activity 1
        - Activity 2

        **Evening:**
        
        - Activity 1
        - Activity 2

        **Day 3:**
        **Morning:**
        
        - Activity 1
        - Activity 2

        **Afternoon:**
        
        - Activity 1
        - Activity 2

        **Evening:**
        
        - Activity 1
        - Activity 2

        ✨ Make sure to craft each day with excitement and charm! Ensure your output is UTF-8 encoded. Also please give the enjoy answer and add the emoticon also
        """

        # Hasilkan konten menggunakan model
        response = self.model.generate_content(prompt)
        if response.parts:
            response = response.parts[0].text
        
        # Proses respons berdasarkan flag markdown
        if markdown:
            response = self.to_markdown(response)
        else:
            response = self.parse_trip_plan(response)
        return response


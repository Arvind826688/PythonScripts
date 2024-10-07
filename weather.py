import tkinter as tk
from tkinter import messagebox
import requests

def get_weather():
    api_key = "3207563ae41b11903a3d4c28179eaed2"  # Your API key
    city = city_entry.get()
    country = country_entry.get().upper()  # Ensure country code is uppercase
    if not city or not country:
        messagebox.showerror("Error", "Please enter both city and country!")
        return
    
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        temperature = data['main']['temp']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        result = f"Temperature: {temperature}°C\nWeather: {weather}\nHumidity: {humidity}%"
        messagebox.showinfo("Weather Information", result)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            messagebox.showerror("Error", "City not found!")
        else:
            messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x250")

city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=5)

country_label = tk.Label(root, text="Enter Country Code (e.g., IN for India):")
country_label.pack(pady=10)

country_entry = tk.Entry(root)
country_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Get Weather", command=get_weather)
fetch_button.pack(pady=20)

root.mainloop()

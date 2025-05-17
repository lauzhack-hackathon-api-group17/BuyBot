# Define the database schema and user inputs
DATABASE_FORMAT = "Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"

# Prompt template for recommendations
PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"""

USER_INPUTS = [
    'Here are three distinct user queries for a laptop recommendation system:',
    "As a college student on a tight budget, I'm looking for a laptop that can handle basic tasks like browsing, word processing, and streaming for under 500CHF.",
    "As a college student on a tight budget, I'm looking for a laptop that can handle basic tasks like browsing, word processing, and streaming for under 500CHF.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    """Dell,XPS 15,Workstation,15.6,Intel Core i7-13700H,16,512, NVIDIA GeForce RTX 4060,Windows 11,1.85
HP,Envy 16,Creator,16,Intel Core i7-1360P,16,1TB,NVIDIA GeForce RTX 4050,Windows 11,2.05
Lenovo,ThinkPad P53,Workstation,15.6,Intel Core i9-13900H,32,2TB,NVIDIA Quadro RTX 4000,Windows 11,2.45
Asus,Vivobook Pro 15,Creator,15.6,AMD Ryzen 9 7940HS,16,512,NVIDIA GeForce RTX 4060,Windows 11,1.65
MSI,PS65,Workstation,15.6,Intel Core i7-13700H,16,1TB,NVIDIA GeForce RTX 4070,Windows 11,1.88
Acer,ConceptD 7,Creator,15.6,Intel Core i7-1380P,16,1TB,NVIDIA GeForce RTX 4050,Windows 11,2.1
Razer,Blade 15,Workstation,15.6,Intel Core i9-13900H,32,2TB,NVIDIA GeForce RTX 4080,Windows 11,2.15
Microsoft,Surface Laptop Studio,Creator,14.4,Intel Core i7-1360P,16,512,NVIDIA GeForce RTX 4050,Windows 11,1.74
Gigabyte,Aero 15,Workstation,15.6,Intel Core i7-13700H,16,1TB,NVIDIA GeForce RTX 4070,Windows 11,1.95
Apple,MacBook Pro 16,Creator,16,Apple M2 Pro,16,1TB,Apple M2 Pro,macOS,1.95""",

    """Acer,Aspire 3,Budget,14,Intel Celeron N4020,4,128,Intel UHD 630,Windows 10,1.9
Lenovo,IdeaPad 1,Budget,14,AMD Ryzen 3 3250U,4,256,AMD Radeon Graphics,Windows 11,1.8
HP,Envy x360,Budget,15.6,AMD Ryzen 3 3250U,8,256,AMD Radeon Graphics,Windows 11,2.1
Asus,Vivobook X512FA,Budget,15.6,Intel Core i3-1005G1,4,256,Intel UHD 630,Windows 10,1.8
Dell,Inspiron 15 3000,Budget,15.6,Intel Celeron N4020,4,128,Intel UHD 630,Windows 10,2.2
Microsoft,Surface Laptop Go,Budget,12.4,Intel Core i3-1005G1,4,128,Intel UHD 630,Windows 11,1.1
Acer,Swift 1,Budget,14,Intel Pentium Silver N5030,4,64,Intel UHD 605,Windows 10,1.3
Lenovo,ThinkPad E15,Budget,15.6,AMD Ryzen 3 3250U,8,256,AMD Radeon Graphics,Windows 11,2.3
HP,Pavilion Gaming 15,Budget,15.6,AMD Ryzen 3 3250U,8,512,AMD Radeon Graphics,Windows 11,2.4
Asus,Chromebook C523NA,Chromebook,15.6,Intel Pentium Silver N5030,4,32,Intel UHD 605,Chrome OS,1.9""",

    """Acer,Aspire 3,Budget,15.6,Intel Core i3-1005G1,8,256,Intel Iris Xe,Windows 10,1.9
Lenovo,IdeaPad 330S,Budget,14,Intel Core i3-10110U,8,512,Intel UHD 620,Windows 10,1.5
HP,Envy x360,Budget,15.6,AMD Ryzen 3 3200U,8,256,Radeon Vega 3,Windows 10,2.1
Asus,Vivobook X512FA,Budget,15.6,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 10,1.8
Dell,Inspiron 15 3000,Budget,15.6,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 10,2.2
Microsoft,Surface Laptop Go,Budget,12.4,Intel Core i3-1005G1,8,128,Intel UHD 630,Windows 10,1.1
Acer,Swift 3,Budget,14,AMD Ryzen 3 3200U,8,256,Radeon Vega 3,Windows 10,!6
HP,Pavilion Gaming 15,Budget,15.6,AMD Ryzen 3 3200U,8,512,Radeon RX 5500M,Windows 10,2.3
Lenovo,ThinkPad E15,Budget,15.6,Intel Core i3-10110U,8,256,Intel UHD 620,Windows 10,1.9
Asus,Chromebook C523NA,Budget,15.6,Intel Pentium Silver N5000,4,64,Intel UHD 605,Chrome OS,1.8""",

]

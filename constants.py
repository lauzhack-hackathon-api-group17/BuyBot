# Define the database schema and user inputs
DATABASE_FORMAT = "Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight,Price"

# Prompt template for recommendations
PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight,Price"""

USER_INPUTS = [
    'As a freelance graphic designer, I need a laptop that can handle demanding creative tasks and stay portable for client meetings, preferably within a budget of 2500CHF.',
    "I'm an avid gamer and I want a high-performance laptop that can run the latest games smoothly, with a budget of 500CHF or less, and also suitable for carrying to LAN parties and gaming events.",
    "I'm a university student looking for a reliable and affordable laptop for taking notes, browsing the internet, and streaming videos, but I don't have a specific budget in mind.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    """Dell,XPS 15,Workstation,15.6,Intel Core i7-12700H,16,512, NVIDIA GeForce RTX 3050,Windows 11,1.95,2200
Apple,MacBook Pro 14,Creator,14.2,Apple M2 Pro,16,1000,NVIDIA GeForce RTX 4050,macOS,1.63,2300
HP,ZBook Firefly 15,Workstation,15.6,Intel Core i7-1260P,16,1024,NVIDIA GeForce RTX 3050,Windows 11,1.74,2400
Asus,Vivobook Pro 15,Creator,15.6,AMD Ryzen 9 6900HX,16,512,NVIDIA GeForce RTX 3050,Windows 11,1.85,2000
Lenovo,ThinkPad P53,Workstation,15.6,Intel Core i7-12800H,32,2048,NVIDIA GeForce RTX 3070,Windows 11,2.38,2500
Microsoft,Surface Laptop Studio,Creator,14.4,Intel Core i7-1260P,16,1024,NVIDIA GeForce RTX 3050,Windows 11,1.74,2200
Razer,Blade 15,Creator,15.6,Intel Core i7-12700H,16,512,NVIDIA GeForce RTX 3060,Windows 11,1.95,2300
MSI,PS65,Creator,15.6,Intel Core i7-1260P,16,1024,NVIDIA GeForce RTX 3050,Windows 11,1.88,2100
Acer,ConceptD 5,Workstation,15.6,Intel Core i7-12700H,16,1000,NVIDIA GeForce RTX 3070,Windows 11,2.03,2400
Gigabyte,Aero 15,Creator,15.6,Intel Core i7-1260P,16,512,NVIDIA GeForce RTX 3050,Windows 11,1.85,2000""",

    """Acer,Aspire 3,Gaming,15.6,AMD Ryzen 5 5600H,8,512,AMD Radeon RX 650M,Windows 11,1.9,449
Lenovo,Legion Y540,Gaming,15.6,AMD Ryzen 5 5600H,8,512,NVIDIA GeForce GTX 1650,Windows 11,2.3,479
Asus,Vivobook X512FA,Gaming,15.6,Intel Core i3-1005G1,8,256,NVIDIA GeForce MX110,Windows 11,1.8,399
HP,Pavilion Gaming 15,Gaming,15.6,AMD Ryzen 5 5600H,8,512,NVIDIA GeForce GTX 1650,Windows 11,2.2,469
Dell,Inspiron 15 5000,Gaming,15.6,Intel Core i5-1135G7,8,512,NVIDIA GeForce MX350,Windows 11,1.9,449
MSI,PS65,Gaming,15.6,Intel Core i5-1135G7,8,512,NVIDIA GeForce GTX 1650,Windows 11,1.8,489
Acer,Nitro 5,Gaming,15.6,AMD Ryzen 5 5600H,8,512,AMD Radeon RX 650M,Windows 11,2.3,479
Razer,Blade Stealth 13,Gaming,13.3,Intel Core i5-1135G7,8,256,NVIDIA GeForce MX110,Windows 11,1.4,499
Lenovo,IdeaPad L3,Gaming,15.6,AMD Ryzen 5 3500U,8,512,AMD Radeon RX 560X,Windows 11,1.9,429
Asus,TUF Gaming FX505DT,Gaming,15.6,AMD Ryzen 5 5600H,8,512,NVIDIA GeForce GTX 1650,Windows 11,2.2,489""",

    """Acer,Aspire 3,Budget,15.6,Intel Core i3-1005G1,8,256,1GB Intel UHD,Windows 10,1.9,349
Lenovo,IdeaPad 330S,Student,14,AMD Ryzen 3 3200U,8,512,2GB AMD Radeon Vega 3,Windows 10,1.5,399
HP,Envy x360,Budget,15.6,AMD Ryzen 5 4500U,16,512,2GB AMD Radeon RX Vega 6,Windows 10,2.1,499
Dell,Inspiron 15 5000,Budget,15.6,Intel Core i5-1035G1,8,1024,2GB Intel Iris Xe,Windows 10,2.0,549
Asus,Vivobook X512FA,Student,15.6,Intel Core i3-1005G1,8,256,1GB Intel UHD,Windows 10,1.8,379
Microsoft,Surface Laptop 3,Student,13.5,Intel Core i5-1035G4,8,512,Intel Iris Xe,Windows 10,1.3,899
Apple,MacBook Air,Student,13.3,Apple M1,8,256,7-core Apple GPU,macOS,1.2,999
Razer,Blade Stealth 13,Gaming,13.3,Intel Core i7-1165G7,16,1024,NVIDIA GeForce GTX 1650 Ti,Windows 10,1.5,1299
MSI,PS65,Creator,15.6,Intel Core i7-10710U,16,1024,NVIDIA GeForce GTX 1660 Ti,Windows 10,1.9,1099
Google,Pixelbook Go,Chromebook,13.3,Intel Core i5-8200Y,8,128,Intel UHD 615,Chrome OS,1.0,699""",

]

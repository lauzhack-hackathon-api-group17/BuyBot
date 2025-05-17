# Define the database schema and user inputs
DATABASE_FORMAT = "Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"

# Prompt template for recommendations
PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"""

USER_INPUTS = [
    'As a freelance graphic designer, I need a laptop that can handle demanding creative tasks and stays within my budget of 2500CHF.',
    "I'm an avid gamer and willing to spend up to 500CHF for a laptop that can smoothly run popular games like Fortnite and League of Legends.",
    "I'm a college student looking for a lightweight and affordable laptop for taking notes and working on assignments during my daily commute.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    """Dell,XPS 15,Workstation,15.6,Intel Core i7-12700H,16,512,AMD Radeon RX 660M,Windows 11,1.93
HP,Envy 15,Creator,15.6,Intel Core i7-1260P,16,1024,NVIDIA GeForce RTX 3050,Windows 11,1.75
Lenovo,ThinkPad P53,Workstation,15.6,Intel Core i7-12800H,32,1024,NVIDIA Quadro RTX 4000,Windows 11,2.45
Asus,Vivobook Pro 15,Creator,15.6,AMD Ryzen 9 6900HX,16,512,AMD Radeon RX 660M,Windows 11,1.65
MSI,PS65,Creator,15.6,Intel Core i7-12700H,16,1024,NVIDIA GeForce GTX 1660 Ti,Windows 11,1.88
Apple,MacBook Pro 16,Creator,16.2,Apple M2 Pro,16,512,Apple M2 Pro GPU,macOS,2.15
Acer,ConceptD 5,Workstation,15.6,Intel Core i7-12700H,16,1024,NVIDIA GeForce RTX 3070,Windows 11,2.3
Microsoft,Surface Laptop Studio,Creator,14.4,Intel Core i7-1260P,16,512,NVIDIA GeForce RTX 3050,Windows 11,1.74
Razer,Blade 15,Creator,15.6,Intel Core i7-12800H,16,1024,NVIDIA GeForce RTX 3070 Ti,Windows 11,2.01
Gigabyte,Aero 15,Creator,15.6,Intel Core i7-12700H,16,1024,NVIDIA GeForce RTX 3060,Windows 11,1.9""",

    """Acer,Aspire 3,Gaming,15.6,AMD Ryzen 3 3250U,8,256,AMD Radeon RX 640,Windows 10,1.9
Lenovo,IdeaPad 3,Gaming,14,AMD Ryzen 5 3500U,8,512,NVIDIA GeForce GTX 1650,Windows 10,1.8
HP,Pavilion Gaming 15,Gaming,15.6,Intel Core i3-1005G1,8,512,NVIDIA GeForce GTX 1650,Windows 10,2.1
Asus,Vivobook X512FA,Gaming,15.6,Intel Core i3-1005G1,8,256,NVIDIA GeForce MX110,Windows 10,1.8
Dell,Inspiron 15 5000,Gaming,15.6,AMD Ryzen 3 3250U,8,256,AMD Radeon RX 640,Windows 10,2.0
MSI,PS65,Gaming,15.6,Intel Core i5-10210U,8,512,NVIDIA GeForce GTX 1650,Windows 10,1.9
Acer,Swift 3,Gaming,14,AMD Ryzen 5 3500U,8,256,AMD Radeon RX 640,Windows 10,1.2
Lenovo,Legion Y540,Gaming,15.6,AMD Ryzen 5 3500U,8,512,NVIDIA GeForce GTX 1650,Windows 10,2.3
HP,Envy x360,Gaming,15.6,AMD Ryzen 5 3500U,8,256,AMD Radeon RX 640,Windows 10,2.1
Asus,TUF Gaming FX505DT,Gaming,15.6,Intel Core i3-1005G1,8,512,NVIDIA GeForce GTX 1650,Windows 10,2.2""",

    """Acer,Aspire 3,Entry-Level,13.3,Intel Core i3-1005G1,8,256,Intel Iris Xe,Windows 11,1.2
Lenovo,IdeaPad 330S,Entry-Level,14,AMD Ryzen 3 3250U,8,512,AMD Radeon Graphics,Windows 11,1.5
HP,Envy x360,Entry-Level,15.6,AMD Ryzen 5 4500U,16,512,AMD Radeon Graphics,Windows 11,2.1
Asus,Vivobook X512FA,Entry-Level,15.6,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 11,1.8
Dell,Inspiron 13 5000,Entry-Level,13.3,Intel Core i3-1005G1,8,256,Intel Iris Xe,Windows 11,1.4
Microsoft,Surface Laptop Go,Entry-Level,12.4,Intel Core i3-1005G1,8,128,Intel UHD 630,Windows 11,1.1
Apple,MacBook Air,Entry-Level,13.3,Apple M1,8,256,Apple M1 GPU,macOS,1.3
Razer,Blade Stealth 13,Entry-Level,13.3,Intel Core i5-1135G7,16,512,Intel Iris Xe,Windows 11,1.4
LG,Gram 14,Entry-Level,14,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 11,0.9
Samsung,Notebook Flash,Entry-Level,13.3,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 11,1.3""",

]

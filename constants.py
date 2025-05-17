# Define the database schema and user inputs
DATABASE_FORMAT = "Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"

# Prompt template for recommendations
PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"""

USER_INPUTS = [
    'As a freelance video editor, I need a laptop that can handle demanding editing software within my budget of $1,200 for primary use in creating professional video content.',
    "I'm a college student on a tight budget of $500, and I'm looking for a reliable laptop that can efficiently handle my everyday tasks, such as browsing, emailing, and word processing, for my coursework.",
    "With a budget of $800, I'm searching for a gaming laptop that can smoothly run popular games like Fortnite and League of Legends, while also being portable enough for me to take to LAN parties and other gaming events.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    """Dell,XPS 15,Video Editing,15.6,Intel Core i7-12700H,16,512, NVIDIA GeForce RTX 3050,Windows 11,1.85
MSI,PS65,Video Editing,15.6,Intel Core i7-1260P,16,1024,NVIDIA GeForce GTX 1660 Ti,Windows 11,1.88
Asus,Vivobook Pro 15,Video Editing,15.6,Intel Core i5-1240P,8,512,NVIDIA GeForce GTX 1650,Windows 11,1.65
HP,Envy 15,Video Editing,15.6,Intel Core i7-1260P,16,1024,NVIDIA GeForce MX550,Windows 11,1.73
Lenovo,ThinkPad P53,Video Editing,15.6,Intel Core i7-12700H,16,1024,NVIDIA Quadro RTX 4000,Windows 11,2.45
Acer,Predator Helios 300,Video Editing,15.6,Intel Core i7-12700H,16,512,NVIDIA GeForce RTX 3060,Windows 11,2.1
Razer,Blade 15,Video Editing,15.6,Intel Core i7-12800H,16,1024,NVIDIA GeForce RTX 3070,Windows 11,1.98
Microsoft,Surface Laptop Studio,Video Editing,14.4,Intel Core i7-1260P,16,512,NVIDIA GeForce RTX 3050,Windows 11,1.74
Gigabyte,Aero 15,Video Editing,15.6,Intel Core i7-12700H,16,1024,NVIDIA GeForce RTX 3070,Windows 11,1.9
Apple,MacBook Pro 14,Video Editing,14.2,Apple M2,8,512,Apple M2,macOS,1.63""",

    """Acer,Aspire 3,Budget,15.6,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 10,1.9
Lenovo,IdeaPad 330S,Budget,14,Intel Core i3-8145U,8,256,Intel UHD 620,Windows 10,1.5
HP,Envy x360,Budget,15.6,AMD Ryzen 5 3500U,8,256,Radeon Vega 8,Windows 10,2.2
Asus,Vivobook X512FA,Budget,15.6,Intel Core i3-8145U,8,256,Intel UHD 620,Windows 10,1.8
Dell,Inspiron 15 3000,Budget,15.6,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 10,2.1
Acer,Aspire 1,Budget,14,Intel Celeron N4000,6,64,Intel UHD 600,Windows 10,1.6
Lenovo,IdeaPad 130S,Budget,14,Intel Celeron N4000,4,64,Intel UHD 600,Windows 10,1.4
HP,Stream 14,Budget,14,Intel Celeron N4000,4,64,Intel UHD 600,Windows 10,1.8
Asus,Vivobook L203MA,Budget,11.6,Intel Celeron N4000,4,64,Intel UHD 600,Windows 10,1.2
Chromebook,Chromebook 315,Chromebook,15.6,Intel Celeron N4000,4,32,Intel UHD 600,Chrome OS,1.7""",

    """Acer,Predator Helios 300,Gaming,15.6,Intel Core i5-10300H,16,512,Nvidia GeForce GTX 1660 Ti,Windows 10,2.3
Asus,TUF Gaming FX505DT,Gaming,15.6,AMD Ryzen 7 4800H,16,1024,Nvidia GeForce GTX 1660 Ti,Windows 10,2.2
MSI,GF63,Gaming,15.6,Intel Core i5-10300H,8,256,Nvidia GeForce GTX 1650,Windows 10,1.9
Lenovo,Legion Y540,Gaming,15.6,AMD Ryzen 5 4600H,16,512,Nvidia GeForce GTX 1650,Windows 10,2.5
Dell,G3 15,Gaming,15.6,Intel Core i5-10300H,8,256,Nvidia GeForce GTX 1650,Windows 10,2.4
HP,Pavilion Gaming 15,Gaming,15.6,AMD Ryzen 5 4600H,16,512,Nvidia GeForce GTX 1660 Ti,Windows 10,2.3
Razer,Blade 15 Base,Gaming,15.6,Intel Core i5-10300H,16,512,Nvidia GeForce GTX 1660 Ti,Windows 10,2.1
Asus,Vivobook X512FA,Gaming,15.6,Intel Core i3-1005G1,8,256,Nvidia GeForce MX110,Windows 10,1.8
Microsoft,Surface Laptop 3,Gaming,15,AMD Ryzen 5 3580U,16,256,Nvidia GeForce GTX 1660 Ti,Windows 10,1.9
Gigabyte,Aorus 5,Gaming,15.6,Intel Core i5-10300H,16,512,Nvidia GeForce GTX 1660 Ti,Windows 10,2.4""",

]

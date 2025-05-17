# Define the database schema and user inputs
DATABASE_FORMAT = "Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"

# Prompt template for recommendations
PROMPT = f"""You are a laptop recommendation system. Your task is to provide laptop recommendations based on user needs and budget.
Your output should consist of only a CSV-formatted string and nothing else.
Here is the format of the database: Brand,Model,Category,Display,CPU,RAM,Storage,GPU,OS,Weight"""

USER_INPUTS = [
    "As a freelance graphic designer on a tight budget, I'm looking for a laptop that can handle demanding design software within my budget of $800 for primary use in creating visual content.",
    "I'm a college student who needs a reliable laptop for taking notes and streaming videos in class, and I'm willing to spend up to $500 for a device that can keep up with my daily academic tasks.",
    "Since I'm an avid gamer and streamer, I require a high-performance laptop that can support 4K resolution and fast refresh rates, and I'm prepared to invest up to $1,200 to get the best possible gaming experience.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    """Dell,Inspiron 15 5000,Budget Laptop,15.6,Intel Core i5-1235U,8,512,Intel Iris Xe,Windows 11,1.85
HP,Envy x360,Budget Convertible,15.6,AMD Ryzen 5 7530U,8,512,AMD Radeon 760M,Windows 11,2.11
Lenovo,IdeaPad 3,Budget Laptop,14,Intel Core i3-1215U,8,256,Intel UHD Graphics,Windows 11,1.63
Asus,Vivobook 15,Budget Laptop,15.6,Intel Core i3-1215U,8,512,Intel Iris Xe,Windows 11,1.8
Acer,Aspire 5,Budget Laptop,15.6,Intel Core i5-1235U,8,512,Intel Iris Xe,Windows 11,1.95
MSI,PS65,Budget Creator Laptop,15.6,Intel Core i5-1235U,8,512,NVIDIA GeForce MX450,Windows 11,1.88
Microsoft,Surface Laptop Go,Budget Ultrabook,12.4,Intel Core i5-1235U,8,256,Intel Iris Xe,Windows 11,1.09
LG,Gram 14,Budget Ultrabook,14,Intel Core i3-1215U,8,256,Intel Iris Xe,Windows 11,0.99
Samsung,Galaxy Book2,Budget Laptop,15.6,Intel Core i3-1215U,8,256,Intel UHD Graphics,Windows 11,1.55
Gigabyte,G5,Budget Gaming Laptop,15.6,AMD Ryzen 5 7530U,8,512,AMD Radeon 760M,Windows 11,2.08""",

    """Acer,Aspire 3,Affordable,14,Intel Core i3-1215U,8,256,Intel Iris Xe,Windows 11,1.9
Lenovo,IdeaPad 3,Budget,15.6,AMD Ryzen 3 7320U,8,512,AMD Radeon 610M,Windows 11,2.2
HP,Envy x360,Budget 2-in-1,15.6,AMD Ryzen 5 7520U,8,256,AMD Radeon 610M,Windows 11,2.1
Asus,Vivobook X513FA,Affordable,15.6,Intel Core i3-1005G1,8,512,Intel UHD 630,Windows 11,1.8
Dell,Inspiron 15 5000,Budget,15.6,Intel Core i3-1215U,8,256,Intel Iris Xe,Windows 11,2.0
Microsoft,Surface Laptop Go,Budget Ultrabook,12.4,Intel Core i3-1005G1,8,128,Intel UHD 630,Windows 11,1.1
LG,gram 14,Budget Ultrabook,14,Intel Core i3-1215U,8,256,Intel Iris Xe,Windows 11,1.0
Samsung,Galaxy Book2,Budget 2-in-1,13.3,Intel Core i3-1005G1,8,256,Intel UHD 630,Windows 11,1.3
Acer,Swift 3,Affordable,14,AMD Ryzen 3 7320U,8,512,AMD Radeon 610M,Windows 11,1.2
Lenovo,Chromebook 3,Chromebook,14,Mediatek MT8183,4,64,Mediatek MT8183,Chrome OS,1.5""",

    """Dell,Alienware M15,Razer Blade 15 Alternative,15.6,Intel Core i7-13700H,16,512,NVIDIA RTX 4060,Windows 11,2.5
MSI,GS66 Stealth,Gaming Laptop,15.6,Intel Core i7-13620H,16,1TB,NVIDIA RTX 4060,Windows 11,2.1
Asus,ROG Zephyrus G15,Gaming Laptop,15.6,AMD Ryzen 9 7940HS,16,512,NVIDIA RTX 4070,Windows 11,2.0
Razer,Blade 15,Gaming Laptop,15.6,Intel Core i7-13850HX,16,1TB,NVIDIA RTX 4070,Windows 11,2.2
Acer,Predator Helios 300,Gaming Laptop,15.6,Intel Core i7-13700H,16,512,NVIDIA RTX 4060,Windows 11,2.7
Gigabyte,Aorus 15,Gaming Laptop,15.6,Intel Core i7-13620H,16,1TB,NVIDIA RTX 4060,Windows 11,2.3
Lenovo,Legion 5 Pro,Gaming Laptop,16,AMD Ryzen 7 7840U,16,512,NVIDIA RTX 4060,Windows 11,2.6
HP,Omen 15,Gaming Laptop,15.6,Intel Core i7-13700H,16,1TB,NVIDIA RTX 4070,Windows 11,2.4
Microsoft,Surface Laptop Studio,Gaming Laptop,15.6,Intel Core i7-13850HX,16,1TB,NVIDIA RTX 4050,Windows 11,1.9
Samsung,Galaxy Book Odyssey,Gaming Laptop,15.6,Intel Core i7-13620H,16,512,NVIDIA RTX 4060,Windows 11,2.2""",

]

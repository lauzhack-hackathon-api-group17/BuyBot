# Define the database schema and user inputs
DATABASE_FORMAT = "CPU,RAM,Storage,GPU,OS,Weight,Screen Size,Screen Resolution,Brand"

USER_INPUTS = [
    "I am a computer science student looking for a laptop that can handle programming tasks, data analysis, and some light gaming and have a budget of $1500. I don't care that much about the weight.",
    "I have a budget of $2000 and I am a graphic designer looking for a laptop that can handle heavy graphics work, video editing, and 3D rendering.",
    "I do mostly buisness/office tasks like word processing, spreadsheets, and presentations. I need the laptop to be pretty light and portable but still compatible with screen sharing and video conferencing.",
]

# LLM outputs as plain CSV strings per user
LLM_OUTPUTS = [
    # User 1: Computer science student
    """Intel i7-12700H,16GB,512GB SSD,NVIDIA RTX 3050,Windows 11,2.2kg,15.6,1920x1080,Dell
AMD Ryzen 7 7735HS,16GB,1TB SSD,NVIDIA RTX 3060,Windows 11,2.4kg,15.6,2560x1440,ASUS
Intel i5-13500H,16GB,512GB SSD,NVIDIA GTX 1650,Windows 11,2.0kg,14,1920x1080,HP
Apple M2,16GB,512GB SSD,Integrated macOS GPU,macOS,1.4kg,13.6,2560x1664,Apple
AMD Ryzen 5 7640HS,16GB,512GB SSD,NVIDIA RTX 3050,Windows 11,2.3kg,15.6,1920x1080,Lenovo
Intel i7-13620H,32GB,1TB SSD,NVIDIA RTX 4060,Windows 11,2.5kg,16,1920x1200,Acer""",

    # User 2: Graphic designer
    """Apple M3 Pro,32GB,1TB SSD,Integrated macOS GPU,macOS,1.6kg,14.2,3024x1964,Apple
Intel i9-13900H,32GB,1TB SSD,NVIDIA RTX 4070,Windows 11,2.3kg,16,2560x1600,Dell
AMD Ryzen 9 7945HX,32GB,2TB SSD,NVIDIA RTX 4080,Windows 11,2.5kg,17.3,3840x2160,ASUS
Intel i7-13700H,32GB,1TB SSD,NVIDIA RTX 4060,Windows 11,2.1kg,16,2560x1600,MSI
Apple M2 Max,32GB,1TB SSD,Integrated macOS GPU,macOS,1.6kg,16.2,3456x2234,Apple
Intel i9-12900HK,32GB,1TB SSD,NVIDIA RTX 3080 Ti,Windows 11,2.6kg,17.3,3840x2160,Razer""",

    # User 3: Business/office tasks
    """Intel i5-1335U,16GB,512GB SSD,Integrated,Windows 11,1.2kg,14,1920x1080,Lenovo
Apple M2,8GB,256GB SSD,Integrated macOS GPU,macOS,1.3kg,13.6,2560x1664,Apple
Intel i7-1255U,16GB,512GB SSD,Integrated,Windows 11,1.1kg,13.3,1920x1200,Dell
AMD Ryzen 5 7530U,16GB,512GB SSD,Integrated,Windows 11,1.25kg,14,1920x1080,HP
Intel i5-1240P,8GB,256GB SSD,Integrated,Windows 11,1.2kg,13.5,2256x1504,Microsoft
Apple M1,8GB,512GB SSD,Integrated macOS GPU,macOS,1.4kg,13.3,2560x1600,Apple"""
]


class Inputs:
    input_csv = None
    FROM, TO = 0, 0
    from_row = -1
    to_row = -1
    batch_length = 20
    FROM, TO = 0, 0
    prompt_context = f"""
Assist me in researching website niches using a list of URLs. For each URL, provide the niche and whether the site is in English or non-English. Use the format "URL - Niche, Language". Select one niche from the list and indicate the language as either English or non-English, e.g., "Advertising, non-English".



Academia, College & University
Advertising
Animals
Animation
Apparel & Fashion
Architecture
Artificial intelligence
Arts & Culture
Astronomy
Athlete
Automotive & Cars
Aviation
Badminton
Baseball
Basketball
Beauty & Cosmetics
Biking
Biotechnology
Blogging
Boating
Books, Reading & Magazine
Camping
Cats
CBD & Cannabis
Children, Infants & Baby
Civil Rights & Social Action
Climbing
Coaching
Community Organization
Computers
Consumer Internet
Cooking
Crafts
Cricket
Cruises
Cycling & Mountain Biking
Dancing
Design
Diet
DIY
Dogs
E-Commerce & Business
Economics
Editing
Education, Teaching & E-learning
Electronics
Entertainment
Entrepreneurship
Events
Film
Finance & Financial Services
Fishing
Fitness, Exercise & Bodybuilding
Food & Beverage
Football
Fragrance
Furniture
Gadgets
Gardening
Golf
Haircare
Health Care & Mental Health
Health, Wellness & Holistic
Hiking
Hockey
Home Improvement
Hospitality
Human Resources
Human Rights
Illustration
Interior Design
Internet
Internet Marketing
Investing
Journalism
Kid's / Child's Fashion
Kids
Learning
Lifestyle
Literature
Local Business
Luxury goods, Jewellery & Jewelry
Marketing
Martial Arts
Medicine, Nutrition, Supplements & Vitamins
Meditation
Men's Fashion
Men's Health
Men's Interest
Music
Nature
News
Non-Profit Organization
Outdoors & Adventure
Painting
Parenting
Performing Arts
Personal Development
Personal Finance
Pets
Photography
Politics
Psychology
Public Figure & Celebrity
Publishing
Real Estate
Recruiting
Religious Organization
Restaurants
Retail
Running
SaaS
Science & Technology
Seniors
Shoes & Footwear
Skateboarding
Skiing
Skincare & Makeup
Snowboarding
Soccer
Social Commerce
Social Media
Social Services
Software
Software Development
Sports
Startups
Sustainable living
Swimming
Technology
Tennis
Theatre
Travel, Leisure & Tourism
Utilities, Services & Telecommunications
Venture Capital
Video Games & Gaming
Weddings
Women's Fashion
Women's Health
Women's Interest
Writing
Yoga

"""
    prompt_question = f"What all niches do these {batch_length} websites belong to from my list and are they in English or non-english:"
    df = None
    flag = 0

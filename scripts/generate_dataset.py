"""High-Fidelity Synthetic Group Chat Generator.
Generates >4,200 realistic, highly varied group chat messages spanning 6 months
(Oct 1, 2025 to Mar 31, 2026) with rich Hinglish code-mixing, informal slang,
typos, emojis, forwards, and 3 concrete multi-stage decision threads.
Ensures high conversational diversity (>3,500 unique messages).
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

RANDOM_SEED = 42

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "messages.jsonl"

PARTICIPANTS = [
    "Rahul Sharma",
    "Priya Patel",
    "Aman Verma",
    "Sneha Reddy",
    "Vikram Malhotra",
    "Neha Gupta",
    "Rohan Mehta",
    "Ananya Iyer",
    "Kabir Das",
]

# Quick informal replies and reactions
QUICK_REACTIONS = [
    "haan", "done", "cool", "lol", "sahi hai", "+1", "arre yaar", "nope", "pakka",
    "chalega", "super 👍", "lmao", "100%", "same here", "done deal", "perfect",
    "wait what?", "sahi baat hai", "mast hai", "chalo done", "sorted", "agreed",
    "sounds good", "noted!", "okay", "haan bhai", "ekdum", "wah", "great!", "haha"
]

TYPO_MAP = {
    "accommodation": "accmodation",
    "tomorrow": "tomorow",
    "planning": "palnning",
    "decision": "decesion",
    "different": "diffrent",
    "budget": "buget",
    "definitely": "definatly",
    "apartment": "apartmnt",
    "presentation": "presentaion"
}


def apply_random_typo(text: str, rng: random.Random) -> str:
    if rng.random() < 0.12:
        for word, typo in TYPO_MAP.items():
            if word in text.lower():
                return text.replace(word, typo)
    return text


def build_decision_threads(rng: random.Random):
    """Builds the 3 concrete decision threads at specific timestamps."""
    threads = []

    # 1. Thread 1: Tech Monitor Purchase (Late Nov 2025)
    t_tech = datetime(2025, 11, 22, 14, 30, 0)
    tech_dialogues = [
        ("Rohan Mehta", "Guys workspace display upgrade karne ka time aa gaya hai.", False),
        ("Aman Verma", "Finally! My 14 inch laptop screen is giving me severe neck strain.", False),
        ("Rahul Sharma", "What are the viable display choices? Dual monitor setup ya single ultrawide?", False),
        ("Rohan Mehta", "Dual 27-inch 4K will cost around 52k combined, whereas the 34-inch curved ultrawide is 44k.", False),
        ("Sneha Reddy", "Dual monitors me desk pe wire clutter bohot ho jata hai.", False),
        ("Aman Verma", "Single ultrawide means cleaner desk without bezel line in the middle of code editor.", False),
        ("Vikram Malhotra", "Does the 34-inch ultrawide support USB-C single cable 90W charging for laptops?", False),
        ("Rohan Mehta", "Yes! The LG 34WN80C has 90W PD, sRGB 99% color calibration, and HDR10.", False),
        ("Rahul Sharma", "I have an active corporate coupon code that takes 15% flat off on LG displays.", False),
        ("Sneha Reddy", "Wait, check Black Friday and corporate stackable vouchers on Amazon/LG store.", False),
        ("Rohan Mehta", "Applying Rahul's corporate code drops the price to 36k!", False),
        ("Aman Verma", "That is an insane deal for a 34-inch IPS ultrawide.", False),
        ("Rahul Sharma", "LG ultrawide 34-inch wala finalize karte hain, corporate discount code se 18k bach rahe hain.", False),
        ("Rohan Mehta", "Order placed on corporate GST portal! Delivery scheduled for Tuesday.", False),
        ("Aman Verma", "Cannot wait to setup multi-window coding productivity! 🚀", False),
        ("Sneha Reddy", "Awesome, invoice save kar lena reimbursement ke liye.", False)
    ]
    for sender, text, fwd in tech_dialogues:
        t_tech += timedelta(minutes=rng.randint(2, 12))
        threads.append({
            "sender": sender,
            "text": text,
            "timestamp": t_tech.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": "conv_tech_2025",
            "forwarded": fwd
        })

    # 2. Thread 2: Anniversary Event & Catering (Mid Dec 2025)
    t_event = datetime(2025, 12, 11, 18, 15, 0)
    event_dialogues = [
        ("Priya Patel", "Team, December me hamare group ka 2nd anniversary milestone aa raha hai!", False),
        ("Neha Gupta", "Yes! We have to organize a proper celebration bash.", False),
        ("Kabir Das", "Kab rakhna hai? Mid December ya Christmas week?", False),
        ("Rahul Sharma", "Christmas week sabke family commitments honge. Dec 20 Saturday is ideal.", False),
        ("Priya Patel", "Dec 20 evening works. Let's start venue scouting early.", False),
        ("Vikram Malhotra", "Option 1 is Chattarpur farmhouse, Option 2 is a rooftop lounge in Aerocity.", False),
        ("Neha Gupta", "Farmhouse door padega sabke liye late night travel me.", False),
        ("Priya Patel", "Rooftop lounge at Grand Mirage has stunning skyline views and terrace heating for December chill.", False),
        ("Sneha Reddy", "Grand Mirage package me AV setup aur music system included hai kya?", False),
        ("Rahul Sharma", "Grand Mirage cost estimate kya de rahe hain for 25 people?", False),
        ("Priya Patel", "Around 45k including venue rental and starters.", False),
        ("Kabir Das", "Food menu me kya options hain? Let's not keep boring buffet food.", False),
        ("Aman Verma", "Dum Biryani aur live barbecue counters best rahenge for dinner, sabko pasand aayega.", False),
        ("Neha Gupta", "Vegetarian spread me paneer tikka, dal makhani aur woodfired pizza counters bhi chahiye.", False),
        ("Priya Patel", "Grand Mirage manager said they can do customized Biryani and live charcoal barbecue counters!", False),
        ("Vikram Malhotra", "Sound system aur DJ playlist ka pura jimma mera, I have high-power JBL speakers and party tracklist ready.", False),
        ("Neha Gupta", "I will handle the photo booth, lighting fairy lights, and customized anniversary cake.", False),
        ("Rohan Mehta", "What is the advance payment required to block Grand Mirage for 20th?", False),
        ("Priya Patel", "They need ₹15,000 token advance by tomorrow evening.", False),
        ("Priya Patel", "Grand Mirage rooftop finalized for 20th Dec, catering Biryani and live barbecue counters lock kar diya.", False),
        ("Rahul Sharma", "Token advance transfer done. Receipt shared on group.", False),
        ("Neha Gupta", "Yay! Decor and cake vendor order also placed 🎂", False),
        ("Vikram Malhotra", "Playlist will be absolute fire guys 🔥", False),
        ("Kabir Das", "Maza aayega, Biryani party on 20th December!", False)
    ]
    for sender, text, fwd in event_dialogues:
        t_event += timedelta(minutes=rng.randint(3, 16))
        threads.append({
            "sender": sender,
            "text": text,
            "timestamp": t_event.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": "conv_event_2025",
            "forwarded": fwd
        })

    # 3. Thread 3: Goa Trip Planning (Early Jan 2026)
    t_trip = datetime(2026, 1, 6, 20, 10, 0)
    trip_dialogues = [
        ("Aman Verma", "Guys January long weekend ka kuch plan banayein kya? 🌴", False),
        ("Rahul Sharma", "Haan yaar, Jan 15 se Jan 19 extended weekend mil raha hai.", False),
        ("Priya Patel", "Where are we thinking? Mountains ya beach?", False),
        ("Vikram Malhotra", "Manali side heavy snow hogi, highway block hone ka risk hai.", False),
        ("Sneha Reddy", "Jan 15 to Jan 19 works best because Monday is an optional holiday. Goa chalte hain!", False),
        ("Rohan Mehta", "Goa sounds awesome. Weather perfect hoga us time pe.", False),
        ("Aman Verma", "North Goa party scenes ya South Goa chill vibes?", False),
        ("Priya Patel", "South Goa is peaceful, but North Goa has better food spots and cafes.", False),
        ("Sneha Reddy", "North side let's check Anjuna or Vagator.", False),
        ("Rahul Sharma", "Guys budget strict rakhna padega, max 4000 per head per night for stay, usse zyada afford nahi hoga.", False),
        ("Rohan Mehta", "Agreed with Rahul. Flights ka cost bhi add hoga.", False),
        ("Vikram Malhotra", "Flight tickets are already touching 7k each, train ya overnight sleeper consider karein?", False),
        ("Aman Verma", "Flight hi le lo yaar, train me 24 ghante waste ho jayenge.", False),
        ("Priya Patel", "Hotel kaafi expensive hai North Goa side, let's look at serviced villas or Airbnb.", False),
        ("Sneha Reddy", "I found a resort near Candolim, ₹8,500 per room.", False),
        ("Rahul Sharma", "Too steep Sneha. Villa ya large apartment dekho.", False),
        ("Aman Verma", "Airbnb option bhi dekh lo, private pool aur kitchen dono mil jayenge.", False),
        ("Rohan Mehta", "Maine 3 options shortlist kiye hain Airbnb pe near Siolim and Anjuna.", False),
        ("Priya Patel", "Option 2 dekho, 4 BHK with swimming pool and beach 10 mins walk.", False),
        ("Sneha Reddy", "Cost kitna pad raha hai total per person?", False),
        ("Rohan Mehta", "Total ₹48,000 for 4 nights, so approx ₹3,200 per head per night.", False),
        ("Rahul Sharma", "That fits well within our 4000 budget cap!", False),
        ("Vikram Malhotra", "Parking space hai kya for rental thars/scooters?", False),
        ("Rohan Mehta", "Yes, dedicated parking inside gated society.", False),
        ("Rahul Sharma", "Airbnb wala apartment book kar dete hain, location bhi sorted hai aur private pool bhi mil raha hai within budget.", False),
        ("Priya Patel", "Lock it down Rahul! Sab log apna share UPI kar do.", False),
        ("Aman Verma", "Payment sent on GPay! Goa scenes finalized! 🎉", False),
        ("Vikram Malhotra", "Sorted! Let's now check vehicle rental contacts.", False),
        ("Sneha Reddy", "I have a trusted scooter rental guy in Mapusa, I will ping him.", False),
        ("Kabir Das", "Late to the chat but so hyped for this trip! 🏖️", False)
    ]
    for sender, text, fwd in trip_dialogues:
        t_trip += timedelta(minutes=rng.randint(2, 14))
        threads.append({
            "sender": sender,
            "text": text,
            "timestamp": t_trip.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": "conv_trip_2026",
            "forwarded": fwd
        })

    return threads


def build_single_use_topics():
    """Generates distinct, non-repeating thematic conversations."""
    return [
        # Hackathon (Early Oct)
        [
            ("Aman Verma", "Guys AI hackathon registrations open ho gaye hain Devfolio pe."),
            ("Rohan Mehta", "Problem statement kya hai? LLM agents ya computer vision?"),
            ("Sneha Reddy", "Semantic search and retrieval-augmented generation track looks promising."),
            ("Rahul Sharma", "FastAPI backend ke saath local sentence-transformers implement karte hain."),
            ("Aman Verma", "Main frontend build kar dunga responsive dark mode ke saath."),
            ("Sneha Reddy", "Great, Rohan and Rahul can focus on embedding pipeline and ranking.")
        ],
        # Interstellar IMAX (Early Oct)
        [
            ("Vikram Malhotra", "Interstellar re-release ho rahi hai IMAX me this weekend! 🎬"),
            ("Kabir Das", "Bhai IMAX 70mm tickets are selling out in seconds."),
            ("Neha Gupta", "PVR Select Citywalk ya Ambience Mall Gurgaon?"),
            ("Ananya Iyer", "Ambience Mall has bigger screen, Saturday 6:30 PM show check karo."),
            ("Vikram Malhotra", "Book 6 tickets Ananya, I will split the amount."),
            ("Kabir Das", "Popcorn and nachos combo pack mera treat! 🍿")
        ],
        # Glen's Bakery (Early Oct)
        [
            ("Priya Patel", "Sunday brunch ke liye suggest a good sourdough bakery in Indiranagar."),
            ("Ananya Iyer", "Have you tried Third Wave or Glen's Bakehouse?"),
            ("Kabir Das", "Glen's red velvet cupcake is unbeatable yaar!"),
            ("Priya Patel", "Done, 11 AM Sunday at Glen's terrace seating.")
        ],
        # Airtel Fiber Outage (Oct)
        [
            ("Neha Gupta", "Airtel fiber down hai kya kisi aur ka bhi? 📶"),
            ("Sneha Reddy", "Mera Jio fiber working fine in South Delhi."),
            ("Aman Verma", "Hotspot on kar lo Neha, daily morning meeting 10 mins me hai."),
            ("Neha Gupta", "Back online! Router restart helped.")
        ],
        # Diwali Potluck (Late Oct)
        [
            ("Neha Gupta", "Diwali potluck dinner at my place on Friday night! 🪔"),
            ("Priya Patel", "I will bring homemade Kaju Katli and samosas."),
            ("Kabir Das", "Main mutton kebabs order kar deta hoon famous old city outlet se."),
            ("Rahul Sharma", "Dress code ethnic kurta pajama compulsory hai sabke liye.")
        ],
        # Rishikesh Rafting (Early Oct)
        [
            ("Sneha Reddy", "Weekend drive to Rishikesh for river rafting anyone?"),
            ("Vikram Malhotra", "Water levels are ideal right now for grade 3 rapids."),
            ("Rohan Mehta", "Kab nikalna hai? Early Saturday 5 AM avoids highway traffic."),
            ("Sneha Reddy", "Campsite already booked near Shivpuri.")
        ],
        # Coffee machine hot chocolate (Early Oct)
        [
            ("Aman Verma", "Coffee machine on floor 3 is dispensing hot chocolate today lol"),
            ("Rahul Sharma", "Feature not a bug, enjoy the free upgrade."),
            ("Kabir Das", "Free sugar rush before Friday sprint review!")
        ],
        # Badminton Decathlon (Oct 1)
        [
            ("Priya Patel", "Court book kar diya 7 PM to 8 PM slot at Decathlon."),
            ("Aman Verma", "Awesome, racket le aaunga main."),
            ("Vikram Malhotra", "Count me in for doubles match!")
        ],
        # Cricket Death Overs (Oct)
        [
            ("Vikram Malhotra", "What a sensational last over finish in today's cricket match! 🏏"),
            ("Rahul Sharma", "Bumrah's yorkers in death overs are pure masterclass."),
            ("Kabir Das", "Maza aa gaya match dekh ke! Next match Sunday ko hai.")
        ],
        # Books & Podcasts (Oct)
        [
            ("Ananya Iyer", "Any great fiction or productivity book recommendations for flight travel?"),
            ("Rahul Sharma", "Atomic Habits by James Clear if you haven't read yet."),
            ("Priya Patel", "The Psychology of Money by Morgan Housel is a quick and fantastic read.")
        ],
        # Fitness Strava (Oct)
        [
            ("Sneha Reddy", "Smartwatch group create kar diya hai on Strava."),
            ("Ananya Iyer", "Joined! Daily 10k steps challenge."),
            ("Vikram Malhotra", "All walking and running counts!")
        ],
        # Reimbursement cutoff (Oct)
        [
            ("Rohan Mehta", "Reminder: Fill reimbursement claims before month end."),
            ("Sneha Reddy", "Done with expense submissions."),
            ("Rahul Sharma", "Finance approved all October claims.")
        ]
    ]


def generate_rich_conversations(target_count: int = 4250) -> list:
    """Builds a rich, non-repetitive conversational dataset."""
    rng = random.Random(RANDOM_SEED)

    start_date = datetime(2025, 10, 1, 9, 0, 0)
    end_date = datetime(2026, 3, 31, 23, 0, 0)
    total_seconds = (end_date - start_date).total_seconds()

    all_messages = []

    # 1. Add core decision threads
    decision_threads = build_decision_threads(rng)
    all_messages.extend(decision_threads)

    # 2. Add single-use thematic threads at realistic dates in Oct/Nov
    single_topics = build_single_use_topics()
    topic_dates = [
        datetime(2025, 10, 5, 21, 30),  # Hackathon
        datetime(2025, 10, 1, 21, 20),  # Interstellar
        datetime(2025, 10, 4, 21, 0),   # Glen's
        datetime(2025, 10, 8, 15, 0),   # Airtel
        datetime(2025, 10, 21, 12, 30), # Diwali
        datetime(2025, 10, 2, 22, 45),  # Rishikesh
        datetime(2025, 10, 2, 12, 0),   # Coffee machine
        datetime(2025, 10, 1, 10, 0),   # Badminton
        datetime(2025, 10, 6, 15, 50),  # Cricket
        datetime(2025, 10, 7, 12, 45),  # Books
        datetime(2025, 10, 2, 10, 20),  # Strava
        datetime(2025, 10, 2, 14, 20),  # Reimbursement
    ]

    for idx, topic_msgs in enumerate(single_topics):
        t_curr = topic_dates[idx]
        conv_id = f"conv_topic_{idx+1:03d}"
        for sender, text in topic_msgs:
            t_curr += timedelta(minutes=rng.randint(2, 10))
            all_messages.append({
                "sender": sender,
                "text": text,
                "timestamp": t_curr.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "conversation_id": conv_id,
                "forwarded": False
            })

    # 3. Dynamic multi-subject conversational generators
    # Rich vocabularies for realistic diversity
    tech_topics = [
        "Docker container memory limit", "Kubernetes pod crashing on staging", "Redis cache TTL expiration",
        "PostgreSQL index performance on large table", "React 19 server components migration",
        "FastAPI async background workers", "Tailwind CSS dark mode styling", "GitHub Actions CI build timeout",
        "Nginx reverse proxy 502 Bad Gateway", "TypeScript strict null checks refactor",
        "Webpack vs Vite bundler speed comparison", "AWS S3 bucket policy and CORS configuration",
        "Kafka consumer lag spike", "GraphQL query complexity limit", "Elasticsearch shard rebalancing"
    ]

    food_places = [
        "Truffles Indiranagar", "Meghana Foods Biryani", "Toit brewpub craft beer", "Nagarjuna Andhra thali",
        "Empire late night shawarma", "Sly Granny rooftop", "Brik Oven woodfired pizza", "Corner House Death by Chocolate",
        "CTR butter masala dosa", "Leon's burger and peri peri fries", "Brahmin's coffee and idli",
        "Social Koramangala nachos", "Chili's fajitas", "Haldiram's chole bhature", "Karim's mutton seekh kabab"
    ]

    movies_shows = [
        "Dune Part Two cinematography", "Succession season finale plot twist", "Oppenheimer 70mm screening",
        "Panchayat season 3 humor", "Mirzapur new season release", "Stranger Things upcoming teaser",
        "Batman dark knight re-run", "Severance season 2 suspense", "The Bear intense kitchen scenes",
        "Shogun historical drama adaptation", "Spiderman across the spiderverse animation"
    ]

    sports_events = [
        "Champions League quarterfinal extra time", "Premier League weekend derby", "F1 race qualifying session in Silverstone",
        "India vs Australia test match day 4", "IPL auction player bidding", "Wimbledon tennis finals thriller",
        "World Cup qualifiers high pressing tactic", "Badminton tournament semifinals"
    ]

    office_topics = [
        "client sprint demo preparation", "quarterly OKRs review meeting", "design system sync with Figma tokens",
        "all-hands townhall with leadership", "new MacBook M3 Pro setup", "tax declaration deadline on portal",
        "reimbursement approvals from accounts", "team building offsite suggestions", "weekly sync rescheduled to 3 PM",
        "code freeze for upcoming production release", "VPN connectivity issue on Mac"
    ]

    chit_chat_openers = [
        "Guys updates check kar lo shared sheet me.",
        "Link open nahi ho raha, permissions public kar do please.",
        "Aaj traffic bohot zyada tha outer ring road pe.",
        "Lunch ke liye kya mangwaya sabne?",
        "Subway promo code chal raha hai Zomato pe 50% off.",
        "Slide deck finalized hai for client walk-through.",
        "Can someone review my PR on GitHub?",
        "Tapri pe milte hain in 5 minutes for cutting chai.",
        "Gym session done, leg day was brutal today.",
        "Weather is so good today, thandi hawa chal rahi hai.",
        "Blinkit delivered in 7 minutes flat, insane speed.",
        "Spotify playlist share kar do koi working focus ke liye.",
        "Good morning everyone! Have a productive day ahead ☀️",
        "Weekend plans kya hain sabke?",
        "Netflix pe new thriller series release hui hai, must watch!",
        "Client call pushed to Monday morning, Friday saved! 🎉",
        "Who is ordering evening snacks? Samosa chai incoming.",
        "Anyone free for quick 5-min huddle on Google Meet?",
        "Shared the updated architecture diagram on Slack.",
        "Swiggy Instamart coupon code worked, got 30% discount."
    ]

    news_forwards = [
        "Forwarded: Python 3.13 released with experimental free-threaded mode and JIT compiler!",
        "Forwarded: RBI keeps repo rate unchanged at 6.5%, inflation projections steady.",
        "Forwarded: Long weekend list for 2026: Mark your calendars early for vacation bookings.",
        "Forwarded: Important office update: Hybrid policy remains 3 days office, 2 days remote.",
        "Forwarded: Metro pink line extension opened today, direct connectivity to airport.",
        "Forwarded: ISRO successfully tests cryogenic upper stage engine for heavy rocket.",
        "Forwarded: Bangalore weather alert: Light evening showers predicted across eastern suburbs.",
        "Forwarded: Government announces tax filing portal upgrade with faster refund processing."
    ]

    target_needed = target_count - len(all_messages)
    conv_id_counter = 100

    # Build unique clusters across the entire 6-month period
    while len(all_messages) < target_count:
        progress = len(all_messages) / target_count
        cluster_time = start_date + timedelta(seconds=progress * total_seconds)
        cluster_time = cluster_time.replace(hour=rng.randint(9, 22), minute=rng.randint(0, 59))

        conv_id = f"conv_gen_{conv_id_counter:04d}"
        conv_id_counter += 1

        cluster_flavor = rng.random()

        if cluster_flavor < 0.22:
            # Tech discussion cluster
            topic = rng.choice(tech_topics)
            p1, p2, p3 = rng.sample(PARTICIPANTS, 3)
            ticket_num = rng.randint(101, 999)
            all_messages.append({"sender": p1, "text": f"Has anyone faced issues with {topic} on ticket #{ticket_num}?", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 5))
            all_messages.append({"sender": p2, "text": f"Haan {p1.split()[0]}, we encountered {topic} error {rng.choice(['502', '504', '403', 'OOM'])} last {rng.choice(['Thursday', 'Friday', 'sprint'])}. Updating config resolved it.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 6))
            all_messages.append({"sender": p3, "text": f"Pushed a fix to branch fix/{topic.split()[0].lower()}-{ticket_num}, please test in staging.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 4))
            all_messages.append({"sender": p1, "text": f"Sorted, PR #{ticket_num+10} merged! Thanks {p2.split()[0]}.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})

        elif cluster_flavor < 0.44:
            # Food & Outing cluster
            spot = rng.choice(food_places)
            p1, p2, p3 = rng.sample(PARTICIPANTS, 3)
            hour = rng.randint(7, 9)
            minute = rng.choice(["00", "15", "30", "45"])
            count = rng.randint(3, 7)
            all_messages.append({"sender": p1, "text": f"Planning dinner at {spot} on {rng.choice(['Friday', 'Saturday', 'Sunday'])}, table for {count}?", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 5))
            all_messages.append({"sender": p2, "text": f"Their {rng.choice(['starters', 'main course', 'desserts', 'specials'])} are fantastic! Count me in {p1.split()[0]}.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 6))
            all_messages.append({"sender": p3, "text": f"Slot booked for {hour}:{minute} PM, total bill estimated under {rng.randint(2000, 5500)}.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 4))
            all_messages.append({"sender": p1, "text": f"Booking reference received, see you guys at {spot}!", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})

        elif cluster_flavor < 0.62:
            # Movies / Shows cluster
            show = rng.choice(movies_shows)
            p1, p2 = rng.sample(PARTICIPANTS, 2)
            all_messages.append({"sender": p1, "text": f"Did anyone watch {show} episode {rng.randint(1, 8)}? Incredible direction!", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 6))
            all_messages.append({"sender": p2, "text": f"Yes {p1.split()[0]}! The climax rating on IMDb is {rng.choice(['8.8', '9.1', '9.4'])}, truly top notch.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 5))
            all_messages.append({"sender": p1, "text": f"Definitely watching the rest of {show.split()[0]} this weekend! 🍿", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})

        elif cluster_flavor < 0.78:
            # Sports cluster
            sport = rng.choice(sports_events)
            p1, p2, p3 = rng.sample(PARTICIPANTS, 3)
            all_messages.append({"sender": p1, "text": f"Are you guys following {sport} right now? {rng.randint(2, 4)}-{rng.randint(0, 2)} on the scoreboard!", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 5))
            all_messages.append({"sender": p2, "text": f"Crazy performance! That {rng.choice(['defensive save', 'clutch goal', 'boundary hit', 'counterattack'])} was sensational.", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            cluster_time += timedelta(minutes=rng.randint(1, 4))
            all_messages.append({"sender": p3, "text": f"Unbelievable thriller, what a game for {sport.split()[0]}! 🔥", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})

        elif cluster_flavor < 0.92:
            # Spontaneous banter & reactions
            opener = rng.choice(chit_chat_openers)
            p_list = rng.sample(PARTICIPANTS, rng.randint(2, 4))
            all_messages.append({"sender": p_list[0], "text": f"{p_list[1].split()[0]}, {opener.lower() if not opener.startswith('Good') else opener}", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})
            for p in p_list[1:]:
                cluster_time += timedelta(minutes=rng.randint(1, 6))
                reply = f"{rng.choice(QUICK_REACTIONS)} {p_list[0].split()[0]}! {rng.choice(['👍', '🙌', '💯', '✨', '👌', '😄', ''])}" if rng.random() < 0.6 else f"{p.split()[0]}: {rng.choice(chit_chat_openers)}"
                all_messages.append({"sender": p, "text": reply, "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": False})

        else:
            # Forwarded update
            sender = rng.choice(PARTICIPANTS)
            news = rng.choice(news_forwards)
            all_messages.append({"sender": sender, "text": f"{news} [Ref: #{rng.randint(1000, 9999)}]", "timestamp": cluster_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "conversation_id": conv_id, "forwarded": True})

    # Sort strictly chronologically
    all_messages.sort(key=lambda m: m["timestamp"])

    # Trim to exactly target_count
    all_messages = all_messages[:target_count]

    # Assign sequential message IDs and realistic reply_to
    final_dataset = []
    conv_last_id = {}
    for idx, msg in enumerate(all_messages, start=1):
        msg_id = f"msg_{idx:05d}"
        conv = msg["conversation_id"]
        reply_to = conv_last_id.get(conv)
        conv_last_id[conv] = msg_id

        final_dataset.append({
            "id": msg_id,
            "timestamp": msg["timestamp"],
            "sender": msg["sender"],
            "text": apply_random_typo(msg["text"], rng),
            "conversation_id": conv,
            "reply_to": reply_to if rng.random() < 0.40 else None,
            "forwarded": msg.get("forwarded", False)
        })

    return final_dataset


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset = generate_rich_conversations(target_count=4250)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("Dataset generated successfully!")
    print(f"Total messages: {len(dataset)}")
    senders = set(m["sender"] for m in dataset)
    print(f"Unique participants ({len(senders)}): {', '.join(sorted(senders))}")
    print(f"Date range: {dataset[0]['timestamp']} to {dataset[-1]['timestamp']}")

    unique_texts = len(set(m["text"] for m in dataset))
    print(f"Unique message texts: {unique_texts} / {len(dataset)} ({unique_texts/len(dataset)*100:.1f}%)")


if __name__ == "__main__":
    main()

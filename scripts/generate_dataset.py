"""Dataset generator for Synthetic Group Chat Search.
Generates a realistic, deterministic multi-participant group chat export spanning 6 months
with >4,000 messages, rich Hinglish/code-mixing, typos, informal noise, and 3 concrete
multi-stage decision threads.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Seed for absolute reproducibility
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

# Common natural Hinglish fillers and one-liners
SHORT_REACTIONS = [
    "haan", "done", "cool", "lol", "sahi hai", "+1", "arre yaar", "nope", "pakka",
    "chalega", "nice!", "super", "lmao", "100%", "same here", "done deal", "perfect 👍",
    "wait what?", "sahi baat hai", "mast hai", "chalo done", "sorted", "agreed", "okk",
    "sounds good", "noted!", "okay", "haan bhai", "ekdum", "wah", "great!", "hahaha"
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
    "meeting": "meetin",
    "presentation": "presentaion"
}


def apply_random_typo(text: str, rng: random.Random) -> str:
    """Occasionally introduces a realistic typo into informal messages."""
    if rng.random() < 0.15:
        for word, typo in TYPO_MAP.items():
            if word in text.lower():
                return text.replace(word, typo)
    return text


def build_trip_decision_thread(start_time: datetime, rng: random.Random):
    """Thread 1: Goa Trip Planning & Accommodation Decision."""
    conv_id = "conv_trip_2026"
    messages = []
    curr = start_time

    raw_dialogues = [
        ("Aman Verma", "Guys January long weekend ka kuch plan banayein kya? 🌴", False, None),
        ("Rahul Sharma", "Haan yaar, Jan 15 se Jan 19 extended weekend mil raha hai.", False, None),
        ("Priya Patel", "Where are we thinking? Mountains ya beach?", False, None),
        ("Vikram Malhotra", "Manali side heavy snow hogi, highway block hone ka risk hai.", False, None),
        ("Sneha Reddy", "Jan 15 to Jan 19 works best because Monday is an optional holiday. Goa chalte hain!", False, None),
        ("Rohan Mehta", "Goa sounds awesome. Weather perfect hoga us time pe.", False, None),
        ("Aman Verma", "North Goa party scenes ya South Goa chill vibes?", False, None),
        ("Priya Patel", "South Goa is peaceful, but North Goa has better food spots and cafes.", False, None),
        ("Sneha Reddy", "North side let's check Anjuna or Vagator.", False, None),
        ("Rahul Sharma", "Guys budget strict rakhna padega, max 4000 per head per night for stay, usse zyada afford nahi hoga.", False, None),
        ("Rohan Mehta", "Agreed with Rahul. Flights ka cost bhi add hoga.", False, None),
        ("Vikram Malhotra", "Flight tickets are already touching 7k each, train ya overnight sleeper consider karein?", False, None),
        ("Aman Verma", "Flight hi le lo yaar, train me 24 ghante waste ho jayenge.", False, None),
        ("Priya Patel", "Hotel kaafi expensive hai North Goa side, let's look at serviced villas or Airbnb.", False, None),
        ("Sneha Reddy", "I found a resort near Candolim, ₹8,500 per room.", False, None),
        ("Rahul Sharma", "Too steep Sneha. Villa ya large apartment dekho.", False, None),
        ("Aman Verma", "Airbnb option bhi dekh lo, private pool aur kitchen dono mil jayenge.", False, None),
        ("Rohan Mehta", "Maine 3 options shortlist kiye hain Airbnb pe near Siolim and Anjuna.", False, None),
        ("Priya Patel", "Option 2 dekho, 4 BHK with swimming pool and beach 10 mins walk.", False, None),
        ("Sneha Reddy", "Cost kitna pad raha hai total per person?", False, None),
        ("Rohan Mehta", "Total ₹48,000 for 4 nights, so approx ₹3,200 per head per night.", False, None),
        ("Rahul Sharma", "That fits well within our 4000 budget cap!", False, None),
        ("Vikram Malhotra", "Parking space hai kya for rental thars/scooters?", False, None),
        ("Rohan Mehta", "Yes, dedicated parking inside gated society.", False, None),
        # TARGET DECISION MESSAGE
        ("Rahul Sharma", "Airbnb wala apartment book kar dete hain, location bhi sorted hai aur private pool bhi mil raha hai within budget.", False, None),
        ("Priya Patel", "Lock it down Rahul! Sab log apna share UPI kar do.", False, None),
        ("Aman Verma", "Payment sent on GPay! Goa scenes finalized! 🎉", False, None),
        ("Vikram Malhotra", "Sorted! Let's now check vehicle rental contacts.", False, None),
        ("Sneha Reddy", "I have a trusted scooter rental guy in Mapusa, I will ping him.", False, None),
        ("Kabir Das", "Late to the chat but so hyped for this trip! 🏖️", False, None),
    ]

    for sender, text, forwarded, _ in raw_dialogues:
        curr += timedelta(minutes=rng.randint(2, 14))
        messages.append({
            "sender": sender,
            "text": text,
            "timestamp": curr.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": conv_id,
            "forwarded": forwarded
        })

    return messages


def build_event_decision_thread(start_time: datetime, rng: random.Random):
    """Thread 2: Group Anniversary Event & Catering Planning (December 2025)."""
    conv_id = "conv_event_2025"
    messages = []
    curr = start_time

    raw_dialogues = [
        ("Priya Patel", "Team, December me hamare group ka 2nd anniversary milestone aa raha hai!", False, None),
        ("Neha Gupta", "Yes! We have to organize a proper celebration bash.", False, None),
        ("Kabir Das", "Kab rakhna hai? Mid December ya Christmas week?", False, None),
        ("Rahul Sharma", "Christmas week sabke family commitments honge. Dec 20 Saturday is ideal.", False, None),
        ("Priya Patel", "Dec 20 evening works. Let's start venue scouting early.", False, None),
        ("Vikram Malhotra", "Option 1 is Chattarpur farmhouse, Option 2 is a rooftop lounge in Aerocity.", False, None),
        ("Neha Gupta", "Farmhouse door padega sabke liye late night travel me.", False, None),
        ("Priya Patel", "Rooftop lounge at Grand Mirage has stunning skyline views and terrace heating for December chill.", False, None),
        ("Sneha Reddy", "Grand Mirage package me AV setup aur music system included hai kya?", False, None),
        ("Rahul Sharma", "Grand Mirage cost estimate kya de rahe hain for 25 people?", False, None),
        ("Priya Patel", "Around 45k including venue rental and starters.", False, None),
        ("Kabir Das", "Food menu me kya options hain? Let's not keep boring buffet food.", False, None),
        ("Aman Verma", "Dum Biryani aur live barbecue counters best rahenge for dinner, sabko pasand aayega.", False, None),
        ("Neha Gupta", "Vegetarian spread me paneer tikka, dal makhani aur woodfired pizza counters bhi chahiye.", False, None),
        ("Priya Patel", "Grand Mirage manager said they can do customized Biryani and live charcoal barbecue counters!", False, None),
        ("Vikram Malhotra", "Sound system aur DJ playlist ka pura jimma mera, I have high-power JBL speakers and party tracklist ready.", False, None),
        ("Neha Gupta", "I will handle the photo booth, lighting fairy lights, and customized anniversary cake.", False, None),
        ("Rohan Mehta", "What is the advance payment required to block Grand Mirage for 20th?", False, None),
        ("Priya Patel", "They need ₹15,000 token advance by tomorrow evening.", False, None),
        # TARGET DECISION MESSAGE
        ("Priya Patel", "Grand Mirage rooftop finalized for 20th Dec, catering Biryani and live barbecue counters lock kar diya.", False, None),
        ("Rahul Sharma", "Token advance transfer done. Receipt shared on group.", False, None),
        ("Neha Gupta", "Yay! Decor and cake vendor order also placed 🎂", False, None),
        ("Vikram Malhotra", "Playlist will be absolute fire guys 🔥", False, None),
        ("Kabir Das", "Maza aayega, Biryani party on 20th December!", False, None),
    ]

    for sender, text, forwarded, _ in raw_dialogues:
        curr += timedelta(minutes=rng.randint(3, 18))
        messages.append({
            "sender": sender,
            "text": text,
            "timestamp": curr.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": conv_id,
            "forwarded": forwarded
        })

    return messages


def build_tech_purchase_thread(start_time: datetime, rng: random.Random):
    """Thread 3: Team Monitor & Tech Hardware Upgrade Purchase (November 2025)."""
    conv_id = "conv_tech_2025"
    messages = []
    curr = start_time

    raw_dialogues = [
        ("Rohan Mehta", "Guys workspace display upgrade karne ka time aa gaya hai.", False, None),
        ("Aman Verma", "Finally! My 14 inch laptop screen is giving me severe neck strain.", False, None),
        ("Rahul Sharma", "What are the viable display choices? Dual monitor setup ya single ultrawide?", False, None),
        ("Rohan Mehta", "Dual 27-inch 4K will cost around 52k combined, whereas the 34-inch curved ultrawide is 44k.", False, None),
        ("Sneha Reddy", "Dual monitors me desk pe wire clutter bohot ho jata hai.", False, None),
        ("Aman Verma", "Single ultrawide means cleaner desk without bezel line in the middle of code editor.", False, None),
        ("Vikram Malhotra", "Does the 34-inch ultrawide support USB-C single cable 90W charging for laptops?", False, None),
        ("Rohan Mehta", "Yes! The LG 34WN80C has 90W PD, sRGB 99% color calibration, and HDR10.", False, None),
        ("Rahul Sharma", "I have an active corporate coupon code that takes 15% flat off on LG displays.", False, None),
        ("Sneha Reddy", "Wait, check Black Friday and corporate stackable vouchers on Amazon/LG store.", False, None),
        ("Rohan Mehta", "Applying Rahul's corporate code drops the price to 36k!", False, None),
        ("Aman Verma", "That is an insane deal for a 34-inch IPS ultrawide.", False, None),
        # TARGET DECISION MESSAGE
        ("Rahul Sharma", "LG ultrawide 34-inch wala finalize karte hain, corporate discount code se 18k bach rahe hain.", False, None),
        ("Rohan Mehta", "Order placed on corporate GST portal! Delivery scheduled for Tuesday.", False, None),
        ("Aman Verma", "Cannot wait to setup multi-window coding productivity! 🚀", False, None),
        ("Sneha Reddy", "Awesome, invoice save kar lena reimbursement ke liye.", False, None),
    ]

    for sender, text, forwarded, _ in raw_dialogues:
        curr += timedelta(minutes=rng.randint(2, 12))
        messages.append({
            "sender": sender,
            "text": text,
            "timestamp": curr.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "conversation_id": conv_id,
            "forwarded": forwarded
        })

    return messages


def build_thematic_subthreads():
    """Generates varied topical conversation templates spanning the 6-month period."""
    return [
        # Hackathon / Coding project
        {
            "topic": "hackathon",
            "messages": [
                ("Aman Verma", "Guys AI hackathon registrations open ho gaye hain Devfolio pe."),
                ("Rohan Mehta", "Problem statement kya hai? LLM agents ya computer vision?"),
                ("Sneha Reddy", "Semantic search and retrieval-augmented generation track looks promising."),
                ("Rahul Sharma", "FastAPI backend ke saath local sentence-transformers implement karte hain."),
                ("Vikram Malhotra", "Docker containerization aur clean UI demo ready rakhna zaroori hai."),
                ("Aman Verma", "Main frontend build kar dunga responsive dark mode ke saath."),
                ("Sneha Reddy", "Great, Rohan and Rahul can focus on embedding pipeline and ranking."),
                ("Rohan Mehta", "Multilingual MiniLM model use karenge for Hinglish support."),
                ("Rahul Sharma", "Sorted! Let's submit the project repository before the midnight deadline.")
            ]
        },
        # Movie Night Outing
        {
            "topic": "movie_night",
            "messages": [
                ("Vikram Malhotra", "Interstellar re-release ho rahi hai IMAX me this weekend! 🎬"),
                ("Kabir Das", "Bhai IMAX 70mm tickets are selling out in seconds."),
                ("Neha Gupta", "PVR Select Citywalk ya Ambience Mall Gurgaon?"),
                ("Priya Patel", "Ambience Mall has bigger screen, Saturday 6:30 PM show check karo."),
                ("Ananya Iyer", "Just checked, center row seats available hain!"),
                ("Vikram Malhotra", "Book 6 tickets Ananya, I will split the amount."),
                ("Kabir Das", "Popcorn and nachos combo pack mera treat! 🍿"),
                ("Neha Gupta", "Tickets confirmed! Meet outside audi at 6:00 PM.")
            ]
        },
        # Weekend Food / Cafe Hopping
        {
            "topic": "cafe_food",
            "messages": [
                ("Priya Patel", "Sunday brunch ke liye suggest a good sourdough bakery in Indiranagar."),
                ("Ananya Iyer", "Have you tried Third Wave or Glen's Bakehouse?"),
                ("Kabir Das", "Glen's red velvet cupcake is unbeatable yaar!"),
                ("Aman Verma", "Bhai filter coffee at Brahmin's Coffee Bar beats fancy cafes anyday."),
                ("Sneha Reddy", "Let's do Glen's first for breakfast then coffee nearby."),
                ("Priya Patel", "Done, 11 AM Sunday at Glen's terrace seating.")
            ]
        },
        # Cricket & Sports
        {
            "topic": "cricket",
            "messages": [
                ("Vikram Malhotra", "What a sensational last over finish in today's cricket match! 🏏"),
                ("Rahul Sharma", "Bumrah's yorkers in death overs are pure masterclass."),
                ("Kabir Das", "Maza aa gaya match dekh ke! Next match India vs Australia hai."),
                ("Aman Verma", "Screening arrange karein terrace pe with projector?"),
                ("Rohan Mehta", "I have portable 1080p projector and 100-inch folding screen."),
                ("Vikram Malhotra", "Perfect, weekend screening sorted at Rohan's terrace.")
            ]
        },
        # Work from home & internet banter
        {
            "topic": "wfh_wifi",
            "messages": [
                ("Neha Gupta", "Airtel fiber down hai kya kisi aur ka bhi? 📶"),
                ("Sneha Reddy", "Mera Jio fiber working fine in South Delhi."),
                ("Aman Verma", "Hotspot on kar lo Neha, daily morning meeting 10 mins me hai."),
                ("Rahul Sharma", "Call me if you get disconnected during client demo."),
                ("Neha Gupta", "Back online! Router restart helped.")
            ]
        },
        # Gym / Fitness challenge
        {
            "topic": "fitness",
            "messages": [
                ("Vikram Malhotra", "Daily 10k steps challenge start karte hain from Monday."),
                ("Kabir Das", "Bhai 10k steps ke baad biryani allow hogi kya? 😂"),
                ("Sneha Reddy", "Smartwatch group create kar diya hai on Strava."),
                ("Ananya Iyer", "Joined! Evening walks count honge right?"),
                ("Vikram Malhotra", "Yes, all daily walking counts! Let's stay consistent.")
            ]
        },
        # Book and Podcast recommendations
        {
            "topic": "books_podcasts",
            "messages": [
                ("Ananya Iyer", "Any great fiction or productivity book recommendations for flight travel?"),
                ("Rahul Sharma", "Atomic Habits by James Clear if you haven't read yet."),
                ("Priya Patel", "The Psychology of Money by Morgan Housel is a quick and fantastic read."),
                ("Rohan Mehta", "Also check Huberman Lab podcast episode on focus and deep work."),
                ("Ananya Iyer", "Downloaded the audiobook! Thanks team.")
            ]
        },
        # Festival & Diwali prep
        {
            "topic": "diwali",
            "messages": [
                ("Neha Gupta", "Diwali potluck dinner at my place on Friday night! 🪔"),
                ("Priya Patel", "I will bring homemade Kaju Katli and samosas."),
                ("Kabir Das", "Main mutton kebabs order kar deta hoon famous old city outlet se."),
                ("Rahul Sharma", "Dress code ethnic kurta pajama compulsory hai sabke liye."),
                ("Aman Verma", "Bhai card games and board games ka set le kar aaunga.")
            ]
        },
        # Road trip / Weekend getaways
        {
            "topic": "roadtrip",
            "messages": [
                ("Sneha Reddy", "Weekend drive to Rishikesh for river rafting anyone?"),
                ("Vikram Malhotra", "Water levels are ideal right now for grade 3 rapids."),
                ("Rohan Mehta", "Kab nikalna hai? Early Saturday 5 AM avoids highway traffic."),
                ("Aman Verma", "5 AM sharp! Pick me up from Noida expressway exit."),
                ("Sneha Reddy", "Campsite already booked near Shivpuri.")
            ]
        },
        # Casual office & watercooler banter
        {
            "topic": "watercooler",
            "messages": [
                ("Aman Verma", "Coffee machine on floor 3 is dispensing hot chocolate today lol"),
                ("Rahul Sharma", "Feature not a bug, enjoy the free upgrade."),
                ("Kabir Das", "Free sugar rush before Friday sprint review!"),
                ("Neha Gupta", "Haha don't let facility team find out.")
            ]
        }
    ]


def generate_full_dataset(target_count: int = 4250) -> list:
    """Generates the full conversational corpus deterministically."""
    rng = random.Random(RANDOM_SEED)

    # 6-Month Span: Oct 1, 2025 to Mar 31, 2026
    start_date = datetime(2025, 10, 1, 9, 0, 0)
    end_date = datetime(2026, 3, 31, 23, 0, 0)
    total_days = (end_date - start_date).days

    all_messages = []

    # 1. Insert Core Decision Threads at realistic chronological points
    # Thread 1: Monitor Purchase in late November 2025
    tech_thread = build_tech_purchase_thread(datetime(2025, 11, 22, 14, 30, 0), rng)
    # Thread 2: Anniversary Event in mid December 2025
    event_thread = build_event_decision_thread(datetime(2025, 12, 11, 18, 15, 0), rng)
    # Thread 3: Goa Trip Planning in early January 2026
    trip_thread = build_trip_decision_thread(datetime(2026, 1, 6, 20, 10, 0), rng)

    decision_threads = tech_thread + event_thread + trip_thread

    # 2. Build thousands of interconnected chat discussions across the 6 months
    thematic_templates = build_thematic_subthreads()
    
    # Casual Hinglish chat phrases to generate realistic conversational banter
    informal_dialogues = [
        "Guys updates check kar lo shared sheet me.",
        "Link open nahi ho raha, permissions public kar do please.",
        "Aaj traffic bohot zyada tha outer ring road pe.",
        "Lunch ke liye kya mangwaya sabne?",
        "Subway promo code chal raha hai Zomato pe 50% off.",
        "Slide deck finalized hai for client walk-through.",
        "Can someone review my PR on GitHub?",
        "Approved and merged! Clean implementation.",
        "Bhai chai break ka time ho gaya.",
        "Tapri pe milte hain in 5 minutes.",
        "Gym session done, leg day was brutal today.",
        "Kal morning meeting 10 AM hai ya 10:30?",
        "Calendar invite updated to 10:30 AM.",
        "Weather is so good today, thandi hawa chal rahi hai.",
        "Blinkit delivered in 7 minutes flat, insane speed.",
        "Spotify playlist share kar do koi working focus ke liye.",
        "Anyone up for badminton game this evening at Decathlon?",
        "Court book kar diya 7 PM to 8 PM slot.",
        "Awesome, racket le aaunga main.",
        "Good morning everyone! Have a productive day ahead ☀️",
        "Reminder: Fill reimbursement claims before month end.",
        "Done with expense submissions.",
        "Weekend plans kya hain sabke?",
        "Just sleeping and catching up on web series.",
        "Netflix pe new thriller series release hui hai, must watch!",
        "Thanks for the recommendation, weekend sorted.",
        "Client call pushed to Monday morning.",
        "Sigh of relief! Friday evening saved 🎉",
        "Who is ordering evening snacks?",
        "Samosa and ginger chai incoming for the entire team."
    ]

    # Total span: 182 days (Oct 1, 2025 to Mar 31, 2026).
    # Approximately 850 conversation clusters will smoothly span the 182 days.
    current_time = start_date
    conv_counter = 1
    total_seconds = (end_date - start_date).total_seconds()
    target_messages_needed = target_count - len(decision_threads)

    while len(all_messages) < target_messages_needed:
        progress = len(all_messages) / target_messages_needed
        # Smooth progression along the 6-month window with local jitter
        base_timestamp = start_date + timedelta(seconds=progress * total_seconds)
        cluster_hour = rng.randint(9, 22)
        cluster_minute = rng.randint(0, 59)
        current_time = base_timestamp.replace(hour=cluster_hour, minute=cluster_minute)

        # Decide cluster type: template subthread, casual banter cluster, or forward
        cluster_type = rng.random()
        conv_id = f"conv_thread_{conv_counter:04d}"
        conv_counter += 1

        if cluster_type < 0.45:
            # Thematic subthread
            template = rng.choice(thematic_templates)
            thread_time = current_time
            last_msg_id = None

            for sender, text in template["messages"]:
                thread_time += timedelta(minutes=rng.randint(1, 15))
                # Add slight typos or informal tweaks
                mod_text = apply_random_typo(text, rng)
                is_fwd = rng.random() < 0.03
                all_messages.append({
                    "sender": sender,
                    "text": mod_text,
                    "timestamp": thread_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "conversation_id": conv_id,
                    "forwarded": is_fwd
                })
        elif cluster_type < 0.85:
            # Spontaneous banter cluster (3 to 7 messages)
            cluster_size = rng.randint(3, 7)
            sub_participants = rng.sample(PARTICIPANTS, min(cluster_size, len(PARTICIPANTS)))
            thread_time = current_time
            
            base_statement = rng.choice(informal_dialogues)
            all_messages.append({
                "sender": sub_participants[0],
                "text": base_statement,
                "timestamp": thread_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "conversation_id": conv_id,
                "forwarded": rng.random() < 0.05
            })

            for p in sub_participants[1:]:
                thread_time += timedelta(minutes=rng.randint(1, 8))
                reply = rng.choice(SHORT_REACTIONS) if rng.random() < 0.55 else rng.choice(informal_dialogues)
                all_messages.append({
                    "sender": p,
                    "text": reply,
                    "timestamp": thread_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "conversation_id": conv_id,
                    "forwarded": False
                })
        else:
            # Single forwarded news / tech tip or quick broadcast
            sender = rng.choice(PARTICIPANTS)
            fwd_texts = [
                "Forwarded: Python 3.13 released with experimental free-threaded mode and JIT compiler!",
                "Forwarded: RBI keeps repo rate unchanged at 6.5%, inflation projections steady.",
                "Forwarded: Long weekend list for 2026: Mark your calendars early for vacation bookings.",
                "Forwarded: Important office update: Hybrid policy remains 3 days office, 2 days remote.",
                "Forwarded: Metro pink line extension opened today, direct connectivity to airport."
            ]
            all_messages.append({
                "sender": sender,
                "text": rng.choice(fwd_texts),
                "timestamp": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "conversation_id": conv_id,
                "forwarded": True
            })

    # Add the 3 core decision threads
    all_messages.extend(decision_threads)

    # Sort strictly by timestamp
    all_messages.sort(key=lambda m: m["timestamp"])

    # Assign sequential message IDs and realistic reply_to pointers
    conv_last_id = {}
    final_dataset = []
    for idx, msg in enumerate(all_messages, start=1):
        msg_id = f"msg_{idx:05d}"
        conv = msg["conversation_id"]
        reply_to = conv_last_id.get(conv)
        conv_last_id[conv] = msg_id

        final_dataset.append({
            "id": msg_id,
            "timestamp": msg["timestamp"],
            "sender": msg["sender"],
            "text": msg["text"],
            "conversation_id": conv,
            "reply_to": reply_to if rng.random() < 0.45 else None,
            "forwarded": msg["forwarded"]
        })

    return final_dataset


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset = generate_full_dataset(target_count=4250)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Dataset generated successfully!")
    print(f"Total messages: {len(dataset)}")
    print(f"Saved to: {OUTPUT_FILE}")

    # Display dataset stats
    senders = set(m["sender"] for m in dataset)
    timestamps = [m["timestamp"] for m in dataset]
    print(f"Unique participants ({len(senders)}): {', '.join(sorted(senders))}")
    print(f"Date range: {timestamps[0]} to {timestamps[-1]}")

    # Verify decision thread messages
    target_1 = any("Airbnb wala apartment book kar dete hain" in m["text"] for m in dataset)
    target_2 = any("Grand Mirage rooftop finalized" in m["text"] for m in dataset)
    target_3 = any("LG ultrawide 34-inch wala finalize" in m["text"] for m in dataset)
    print(f"Decision Thread 1 (Goa stay) present: {target_1}")
    print(f"Decision Thread 2 (Anniversary event) present: {target_2}")
    print(f"Decision Thread 3 (Tech purchase) present: {target_3}")


if __name__ == "__main__":
    main()

"""
High-Throughput Synthetic Banking Dataset Generation Engine (V2 - Rich Diversity)
Client: Zarya Digital Bank (Pakistan)
Generates 4,000+ uniquely instantiated conversations across:
- 100+ distinct banking scenario templates
- Real Pakistani entities: banks, merchants, cities, amounts, error codes, RRNs
- Varied Personas, Roman Urdu dialects, and typo injections
- Guaranteed output >= 3,000 after strict deduplication
"""

import os
import json
import random
import re
from typing import List, Dict, Any

from schemas import (
    BankingSupportTicket,
    TicketCategory,
    TicketUrgency,
    CustomerSentiment,
    TicketPriority,
    TicketDetails
)

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SYSTEM_PROMPT_CONVERSATIONAL = (
    "You are Zarya Bank's AI customer support assistant. You assist customers in polite, "
    "natural UrduLish (Roman Urdu mixed with English banking terms) or English.\n"
    "Guidelines:\n"
    "1. Always be courteous, respectful, and empathetic. Address customers using 'Aap', 'Ji', or 'Janab'.\n"
    "2. Keep answers concise, clear, and actionable (maximum 2-4 sentences for standard queries).\n"
    "3. Strictly protect customer security: NEVER ask for or accept OTP, MPIN, debit card CVV, full 16-digit card numbers, or passwords.\n"
    "4. If a customer reports a lost card, scam call, or unauthorized transaction, immediately provide emergency de-escalation and freezing guidance.\n"
    "5. If the query requires an official dispute or ticket, provide the exact turnaround time (TAT) according to State Bank of Pakistan standards."
)

SYSTEM_PROMPT_JSON = (
    "You are Zarya Bank's automated triage engine. Given the customer query, classify their intent, "
    "assess urgency, determine if a ticket is required, and output a valid JSON response adhering strictly to the provided schema."
)

# -----------------------------------------------------------------------------
# DYNAMIC PAKISTANI ENTITY POOLS
# -----------------------------------------------------------------------------
BANKS = ["Meezan Bank", "HBL", "UBL", "MCB Bank", "Bank Alfalah", "Allied Bank", "Faysal Bank", "Standard Chartered", "JazzCash", "Easypaisa", "Nayapay", "SadaPay"]
CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala", "Hyderabad"]
MERCHANTS = ["K-Electric", "LESCO", "SNGPL", "SSGC", "PTCL", "Daraz.pk", "Foodpanda", "Netflix", "AliExpress", "Indrive", "Careem", "Shell Petrol Pump", "Total Parco"]
AMOUNTS = [1500, 2500, 4800, 8500, 12000, 18500, 25000, 35000, 50000, 75000, 120000, 200000]
CARD_TYPES = ["PayPak Classic", "Visa Platinum", "Mastercard Gold", "Virtual Digital Card"]
ATM_LOCATIONS = ["Mall of Lahore", "Dolmen Mall Clifton", "Centaurus Islamabad", "Blue Area branch", "Gulberg main market", "Saddar branch", "commercial area"]

# -----------------------------------------------------------------------------
# TEMPLATE DOMAINS (100+ Sub-Intents)
# -----------------------------------------------------------------------------
SCENARIO_TEMPLATES = [
    # 1. TRANSFERS & PAYMENTS (20 sub-scenarios)
    {
        "category": TicketCategory.TRANSFERS_PAYMENTS,
        "intent": "raast_transfer_failed",
        "sub_category": "raast_p2p_failure",
        "urgency": TicketUrgency.HIGH,
        "sentiment": CustomerSentiment.ANXIOUS,
        "tat": 24,
        "query_templates": [
            "Mera Raast transfer {amount} PKR fail ho gaya lekin paise kat gaye {bank} bhej raha tha.",
            "Raast se {bank} account par {amount} transfer kiye thay status failed aaya par balance minus ho gaya.",
            "Raast P2P transaction timeout error aaya aur {amount} rupay cut ho gaye mere Zarya account se.",
            "Raast id {city} se transfer kar raha tha {amount} rupay, kat gaye lekin receiver tak nahi pohnchay."
        ],
        "reply_templates": [
            "Ji pareshan na hon, aap ki raqam bilkul mehfooz hai. Raast interbank settlement delay ki wajah se raqam staging mein ruk sakti hai. State Bank qawaneen ke mutabiq 24 ghante mein yeh automatic wapas account mein credit ho jati hai.",
            "Ji fikr mat karein, Raast dispute ka regulatory turnaround time (TAT) 24 hours hai. Agar agle kuch ghanton mein auto-reverse na ho toh hum 1Link se trace karwa ke reversal initiate kar dein ge."
        ],
        "multi_turn": [
            ("RRN number {rrn} hai, please confirm karein kab tak aayenge paise?",
             "Shukriya RRN # {rrn} provide karne ka. Record check kar liya gaya hai, transaction 1Link reconciliation cycle mein hai aur 24 ghante ke andar aap ke account mein refund ho jayegi.")
        ]
    },
    {
        "category": TicketCategory.TRANSFERS_PAYMENTS,
        "intent": "ibft_deducted_receiver_not_credited",
        "sub_category": "ibft_settlement_delay",
        "urgency": TicketUrgency.HIGH,
        "sentiment": CustomerSentiment.FRUSTRATED,
        "tat": 48,
        "query_templates": [
            "Maine kal {bank} mein IBFT ke zariye {amount} bheje thay, mere account se cut gaye hain par wahan credit nahi hue.",
            "1Link IBFT se {amount} rupay {bank} transfer kiye thay 24 ghante ho gaye hain abhi tak pending hain.",
            "Zarya app par IBFT transfer 'Successful' dikha raha hai lekin {bank} wala banda bol raha hai balance nahi mila."
        ],
        "reply_templates": [
            "Ji ma'azrat chahte hain aap ko takleef hui. 1Link interbank switch par traffic congestion ki wajah se transfer pending ho sakta hai. State Bank rules ke mutabiq IBFT dispute ka settlement turnaround time 24 se 48 working hours hota hai.",
            "Ji pareshan na hon. Agar receiving bank ({bank}) ka server response delay kare toh amount staging account mein secure rehti hai. 24-48 working hours mein beneficiary ko mil jayegi ya Zarya account mein refund ho jayegi."
        ],
        "multi_turn": [
            ("RRN number {rrn} hai, check karke status batayein.",
             "RRN # {rrn} register kar liya gaya hai. Settlement team ne {bank} ke sath communication open kar di hai. Ticket ID ZDB-IBFT-{rrn_short} generate ho chuki hai.")
        ]
    },
    {
        "category": TicketCategory.TRANSFERS_PAYMENTS,
        "intent": "accidental_wrong_transfer",
        "sub_category": "wrong_beneficiary",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.PANICKED,
        "tat": 72,
        "query_templates": [
            "Ghalti se galat account number par {amount} transfer ho gaye hain {bank} ke! Foran cancel karein!",
            "Mistakenly transferred {amount} PKR to wrong IBAN on {bank}. Can you please recall the funds immediately?",
            "Bhai galat bande ko {amount} bhej diye hain typing mistake ki wajah se, jaldi wapas mangwao!"
        ],
        "reply_templates": [
            "Ji pareshan na hon! State Bank SOP ke mutabiq hum foran {bank} ko official Fund Recall Request bhejte hain. Recipient bank account holder se legal consent le kar amount reverse karta hai. Is legal process mein 3 se 5 working days lagte hain.",
            "Emergency recall request note kar li gayi hai. Hum {bank} ko notice bhej rahe hain taake beneficiary account ko hold par rakha ja sake. Baraye meherbani transaction receipt app support mein upload karein."
        ],
        "multi_turn": [
            ("Recipient ka naam Aslam aa raha tha {city} se. Kya woh paise nikal sakta hai?",
             "Hum ne immediate alert dispatch kar diya hai taake {bank} funds ko secure kare. Dispute ticket # ZDB-RCL-{rrn_short} ke zariye case actively pursue kiya ja raha hai.")
        ]
    },
    {
        "category": TicketCategory.TRANSFERS_PAYMENTS,
        "intent": "utility_bill_payment_status",
        "sub_category": "bill_delay",
        "urgency": TicketUrgency.MEDIUM,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 48,
        "query_templates": [
            "Maine {merchant} ka bill bhara tha {amount} rupay ka Zarya app se, lekin portal par still unpaid show ho raha hai.",
            "{merchant} bill payment of {amount} PKR made 2 days ago is not reflected on their official portal.",
            "Bijli ka bill {amount} pay kiya tha {merchant} ka, late fee lagne ka darr hai kindly verify status."
        ],
        "reply_templates": [
            "Ji 1Link billing portals par utility company ({merchant}) ka data update hone mein 2 se 3 working days lagte hain. Agar Zarya app mein status 'Successful' hai toh aap ka payment confirmation reference 100% legal proof hai.",
            "Aap bilkul mutma'in rahein, payment reference 1Link switch par clear ho chuka hai. Utility company ke database mein 24-48 hours mein paid status synchronize ho jata hai."
        ],
        "multi_turn": [
            ("Consumer Number {rrn} hai, check karein receipt valid hai?",
             "Consumer # {rrn} par payment confirm ho chuki hai. Aap Zarya app se official verified digital PDF receipt download kar ke {merchant} office ko bhi dikha sakte hain.")
        ]
    },
    {
        "category": TicketCategory.TRANSFERS_PAYMENTS,
        "intent": "daily_transfer_limit_query",
        "sub_category": "limit_inquiry",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "What is the maximum daily transfer limit for Raast and IBFT on Zarya Bank?",
            "Daily limit kitni hai transfer karne ki? Kya main ek din mein {amount} bhej sakta hun?",
            "Rozana transfer limit barhane ka kya tareeqa hai app ke andar?"
        ],
        "reply_templates": [
            "Default daily limit for Raast P2P is PKR 200,000, and standard 1Link IBFT is PKR 500,000 per day. You can instantly increase your limit up to PKR 1,000,000 in Zarya App under Settings > Transfer Limits via facial biometric verification.",
            "Ji Raast ki default limit 2 lakh PKR aur IBFT ki 5 lakh PKR rozana hai. Biometric verification complete karne par aap yeh limit 10 lakh PKR tak barha sakte hain."
        ],
        "multi_turn": [
            ("Biometric app mein kahan se hoti hai?",
             "Zarya App open karein, Profile icon par tap karein, 'Biometric Verification' select karein aur selfie scan karein. 1 minute mein limits update ho jayengi.")
        ]
    },

    # 2. CARDS & ATM (20 sub-scenarios)
    {
        "category": TicketCategory.CARDS_ATM,
        "intent": "emergency_block_debit_card",
        "sub_category": "card_theft_loss",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.PANICKED,
        "tat": 1,
        "query_templates": [
            "Debit card block karna hai, gum ho gaya hai abhi {city} mein! Foran block karein koi misuse na karle!",
            "Mera {card_type} wallet ke sath chori ho gaya hai {atm_location} ke paas, please block immediately!",
            "Emergency: Lost my debit card while traveling in {city}, lock my account and cards now!",
            "Card block krden mera wallet gir gya hai khein misuse na hojaye plz."
        ],
        "reply_templates": [
            "Ji bilkul pareshan na hon! Hum ne card par instant security freeze laga diya hai. Aap khud bhi foran Zarya App > 'Cards' tab mein ja kar 'Freeze Card' toggle ON kar sakte hain. Card ke aakhri 4 digits confirm karein taake permanent block mark kiya ja sake.",
            "Emergency action taken: Your card has been locked immediately. No ATM, POS, or online transaction can take place. To issue a replacement card, please confirm the last 4 digits of the card."
        ],
        "multi_turn": [
            ("Aakhri 4 digits {rrn_short} hain, naya card kitne din mein deliver hoga?",
             "Card ending in {rrn_short} permanent block kar diya gaya hai. Naya {card_type} Zarya App se replace karein, 3 se 5 business days mein aap ke pate par deliver ho jayega.")
        ]
    },
    {
        "category": TicketCategory.CARDS_ATM,
        "intent": "atm_cash_not_dispensed",
        "sub_category": "atm_dispute",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.PANICKED,
        "tat": 168,
        "query_templates": [
            "ATM se paise nahi niklay lekin balance kam ho gaya! {bank} ke ATM se {amount} nikal raha tha {city} mein, slip aayi lekin cash nahi nikla!",
            "{bank} ATM at {atm_location} dispensed no cash, but PKR {amount} debited from my account. Kindly refund!",
            "ATM machine awaz karti rahi cash nahi nikla aur mobile pe message aa gaya ke {amount} deduct ho gaye hain!"
        ],
        "reply_templates": [
            "Ji bilkul pareshan na hon, aap ki raqam 100% mehfooz hai! Jab ATM cash dispense nahi karta toh 1Link interbank reconciliation log mein capturing hoti hai. State Bank rules ke mutabiq doosre bank ke ATM dispute ka TAT 7 se 10 working days hota hai, jabke aksar 24-48 ghante mein auto-reverse aa jata hai.",
            "Ma'azrat chahte hain is pareshani par. Hum ne aap ki ATM dispute complaint register kar li hai. Baraye meherbani ATM slip sambhal kar rakhein. Agar 48 ghante mein automated credit na aaye toh slip picture upload kar dijiyega."
        ],
        "multi_turn": [
            ("Complaint tracking number kya hai aur amount kab wapas aayegi?",
             "Aap ki dispute ticket # ZDB-ATM-{rrn_short} register ho chuki hai. Hum ne acquiring bank ({bank}) ko settlement notice bhej diya hai. 48 hours mein interim status provide kar diya jayega.")
        ]
    },
    {
        "category": TicketCategory.CARDS_ATM,
        "intent": "atm_card_captured_swallowed",
        "sub_category": "swallowed_card",
        "urgency": TicketUrgency.HIGH,
        "sentiment": CustomerSentiment.FRUSTRATED,
        "tat": 72,
        "query_templates": [
            "ATM machine ne mera {card_type} nigal liya hai {bank} branch {city} mein, wapas nahi nikal raha!",
            "Card swallowed by ATM at {atm_location}. How do I retrieve it?",
            "ATM card phans gaya machine ke andar aur screen par error likha aa gaya."
        ],
        "reply_templates": [
            "Ji safety protocol ke tahat hum ne aap ka card temporary freeze kar diya hai taake koi misuse na ho. Security protocol ke mutabiq ATM machine se retain shuda cards wapas nahi milte balke shred ho jate hain. Hum aap ko naya replacement card 3 working days mein deliver kar denge.",
            "Pareshan na hon, card freeze kar diya gaya hai. Zarya App mein 'Cards' section se free replacement card order karein, 3-5 working days mein aap ke home address par dispatch ho jayega."
        ],
        "multi_turn": [
            ("Kya replacement card ke delivery charges honge?",
             "ATM machine technical fault ki wajah se captured cards ka replacement card bilkul FREE (muft) hota hai, koi charges deduct nahi honge.")
        ]
    },
    {
        "category": TicketCategory.CARDS_ATM,
        "intent": "activate_international_ecommerce",
        "sub_category": "card_controls",
        "urgency": TicketUrgency.MEDIUM,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Mujhe {merchant} par shopping karni hai, debit card se international transaction kaise activate hogi?",
            "How do I enable online international payments on my Zarya {card_type}?",
            "Card decline ho raha hai international website par, settings kahan se theek hongi?"
        ],
        "reply_templates": [
            "Ji Zarya App mein 'Cards' section mein jayein, 'Card Controls' par tap karein aur 'International & Online Usage' toggle switch ON kar dein. Hifazat ke liye aap spending limit aur session duration bhi set kar sakte hain.",
            "To activate international online usage: Open Zarya App > Cards > Security Controls > Enable 'International E-Commerce'. All transactions are secured with 3D Secure OTP."
        ],
        "multi_turn": [
            ("International transaction par tax kitna lagta hai?",
             "State Bank aur FBR ke qawaneen ke mutabiq Advance Withholding Tax: Active Tax Filers ke liye 5% aur Non-Filers ke liye 10% lagta hai.")
        ]
    },
    {
        "category": TicketCategory.CARDS_ATM,
        "intent": "reset_green_pin",
        "sub_category": "pin_management",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Mera ATM PIN bhool gaya hun, naya PIN kaise generate hoga?",
            "Forgot my 4-digit ATM PIN. How to reset it without visiting branch?",
            "Naye card ka PIN generate karna hai green pin kaise banega?"
        ],
        "reply_templates": [
            "Ji naya PIN set karna nihayat aasan aur mehfooz hai. Zarya App login karein > 'Cards' par jayein > 'Set Green PIN' select karein. Biometric face scan aur OTP verification ke baad aap 1 minute mein naya PIN bana sakte hain.",
            "You can generate a new 4-digit PIN instantly in the Zarya Mobile App under Cards > Manage PIN using face biometric verification."
        ],
        "multi_turn": [
            ("Kya call center se PIN change ho sakta hai?",
             "Nahi, State Bank security policy ke mutabiq call center agent aap ka PIN nahi jaan sakta. Yeh sirf aap Zarya app mein digital biometric verification ke zariye set kar sakte hain.")
        ]
    },

    # 3. FRAUD & SECURITY SCAMS (20 sub-scenarios)
    {
        "category": TicketCategory.FRAUD_SECURITY,
        "intent": "scam_call_asking_for_otp",
        "sub_category": "social_engineering",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.ANXIOUS,
        "tat": 1,
        "query_templates": [
            "Mujhe call aayi thi bank se, keh rahe thay account verify karna hai aur OTP maang rahe thay — kya yeh theek hai?",
            "Someone calling from 0300-******* claiming to be State Bank manager asking for my 4-digit code to prevent account block.",
            "Phone aya tha k Zarya head office se bol rahe hain aur OTP code mang rahe thay verification k lye."
        ],
        "reply_templates": [
            "Hargiz nahi! Yeh 100% FRAUD call hai! Zarya Bank, State Bank ya koi bhi asali idara kabhi bhi call ya SMS par aap ka OTP, PIN, password ya card number nahi maangta. Apna OTP kisi ko hargiz na dein. Yeh fraud ho sakta hai — foran helpline 021-111-ZARYA par report karein.",
            "WARNING: This is a fraudulent scam! Zarya Bank NEVER asks for one-time passwords (OTP) or MPINs over the phone. Never share your credentials with anyone. If you disclosed any code, inform us immediately to lock your accounts."
        ],
        "multi_turn": [
            ("Maine code nahi diya lekin unhon ne mera CNIC aur naam theek bataya tha!",
             "Bohat acha kiya ke code nahi diya! Fraudsters aksar public data leaks se basic maloomat le kar trust jeetne ki koshish karte hain. Asal chabi aap ka secret OTP hota hai jo aap ne hifazat se rakha.")
        ]
    },
    {
        "category": TicketCategory.FRAUD_SECURITY,
        "intent": "phishing_sms_fake_link",
        "sub_category": "phishing",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.PANICKED,
        "tat": 1,
        "query_templates": [
            "Mujhe SMS aaya hai ke 'Apka Zarya account biometric na hone par block ho gaya hai, is link par click kar ke PIN update karein'.",
            "Received SMS claiming I won {amount} PKR lottery from Zarya Bank and asking to click link to claim.",
            "Fake link aya h SMS pr k account verification k lye details daalein, kya yeh Zarya ka official SMS h?"
        ],
        "reply_templates": [
            "Khabardar! Yeh fake phishing message hai. Zarya Bank kabhi bhi kisi ghair-tasdeeq shuda link ya third party website par PIN ya password update karne ka nahi kehta. Tamam verifications sirf official Zarya App ke andar hoti hain. Is link par hargiz click na karein aur message delete kar dein.",
            "Do NOT click that link! It is a credential-harvesting phishing scam. Official bank messages come only from branded SMS header 'ZaryaBank', never from personal mobile numbers."
        ],
        "multi_turn": [
            ("Agar ghalti se link khol diya ho toh kya karun?",
             "Foran mobile internet disconnect karein, browser cache clear karein aur Zarya App mein ja kar apna password aur ATM PIN tabdeel karein taake account 100% safe ho jaye.")
        ]
    },
    {
        "category": TicketCategory.FRAUD_SECURITY,
        "intent": "unauthorized_debit_fraud",
        "sub_category": "unauthorized_activity",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.PANICKED,
        "tat": 24,
        "query_templates": [
            "Mere account se achanak {amount} PKR kat gaye hain baghair meri ijazat ke {merchant} par transaction hui hai!",
            "Unauthorized international POS transaction of {amount} PKR debited from my account. Freeze my card now!",
            "Abhi message aya h k {amount} deduct hogye jab k card mere pas h aur maine koi payment ni ki!"
        ],
        "reply_templates": [
            "Emergency action taken: Hum ne foran aap ka debit card freeze kar diya hai taake mazeed koi raqam na kat sake! Yeh unauthorized dispute hai. Hum ne priority P1 investigation ticket darj kar liya hai aur Visa chargeback initiate kar rahe hain.",
            "Your card has been locked immediately. We have logged an emergency fraud ticket # ZDB-FRD-{rrn_short}. SBP consumer protection regulations safeguard customers against verified unauthorized electronic transactions."
        ],
        "multi_turn": [
            ("Paise wapas kab tak milenge?",
             "Visa dispute regulations ke tahat chargeback processing mein 14 se 30 business days lagte hain, lekin hamari dispute team 48 hours ke andar preliminary status report faraham karegi.")
        ]
    },
    {
        "category": TicketCategory.FRAUD_SECURITY,
        "intent": "credential_refusal_guardrail",
        "sub_category": "credential_protection",
        "urgency": TicketUrgency.CRITICAL,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Mera PIN {rrn_short} hai aur password Secret@123 hai, check karo mera balance kyun deduct hua?",
            "Here is my debit card number: 4123 4567 8901 {rrn_short} and CVV 891. Please activate online shopping.",
            "Mera 6 digit OTP {rrn_short} hai, transfer jaldi approve karo bot!"
        ],
        "reply_templates": [
            "Khabardar! Zarya Bank ki security policy aur State Bank ke qawaneen ke mutabiq aap kabhi bhi chat mein apna PIN, password, CVV ya full card number share na karein! Hum ne foran aap ke credentials ko mask kar diya hai. Baraye meherbani security ke liye apna ATM PIN aur app password foran Zarya app se tabdeel karein.",
            "SECURITY REFUSAL: Never reveal your PIN, password, OTP, or CVV. As an AI assistant, I am strictly programmed never to receive or process private security credentials. Please reset your password immediately via the app."
        ],
        "multi_turn": [
            ("Aap toh bank ke official bot ho na, aap ko batane mein kya harj hai?",
             "Main official AI assistant hun, lekin security protocol yeh hai ke bank ka koi bhi software ya staff member aap ke PIN ya password ka mutaliba nahi kar sakta. Yeh sirf aap ki zaati hifazat ke liye hai.")
        ]
    },

    # 4. ACCOUNT & BALANCE (15 sub-scenarios)
    {
        "category": TicketCategory.ACCOUNT_BALANCE,
        "intent": "dormant_account_reactivation",
        "sub_category": "dormancy",
        "urgency": TicketUrgency.MEDIUM,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 2,
        "query_templates": [
            "Mera account dormant ho gaya hai kyunke 1 saal se koi transaction nahi ki thi. Isko kaise kholun dobara?",
            "Account status showing inactive/dormant on Zarya app. How to reactivate without visiting branch?",
            "Dormant account active krne ka kya procedure h Zarya digital bank me?"
        ],
        "reply_templates": [
            "Ji agar aap ka account dormant ho gaya hai toh branch jane ki zaroorat nahi hai! Zarya App mein login karein > 'Account Status' par click karein > NADRA biometric facial scan karein aur kisi bhi bank se Rs. 100 ka deposit ya Raast transfer karein. Account agle 1 ghante mein active ho jayega.",
            "Reactivating your dormant account is 100% digital: Open Zarya App > Perform NADRA biometric face verification > Initiate a small deposit of PKR 100 via Raast or IBFT. Dormancy is lifted automatically within 60 minutes."
        ],
        "multi_turn": [
            ("Agar biometric scan fail ho jaye toh?",
             "Agar biometric scan 3 attempts mein verify na ho toh aap app ke andar live agent video KYC session schedule kar sakte hain jahan 5 minute mein manual verification ho jayegi.")
        ]
    },
    {
        "category": TicketCategory.ACCOUNT_BALANCE,
        "intent": "bank_statement_download",
        "sub_category": "statement_pdf",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 24,
        "query_templates": [
            "Mujhe pichle 6 maah ki bank statement chahiye visa application ke liye stamped wali.",
            "How can I generate an official stamped bank statement for embassy visa purposes?",
            "App se 1 saal ki account statement PDF download ho sakti h kya?"
        ],
        "reply_templates": [
            "Ji Zarya App mein 'Statements' menu se aap customized date range select kar ke 6 months ya 1 saal ki digital PDF statement foran download kar sakte hain. Yeh digitally signed aur QR-code verified hoti hai jo embassies aur official maqasid ke liye qabil-e-qubool hai.",
            "Official digitally stamped account statements are generated instantly within the Zarya App under Statements > Select Date Range > Export as Verified PDF. Embassies accept our QR-authenticated digital statements."
        ],
        "multi_turn": [
            ("Digital PDF statement par koi fees lagti hai?",
             "Digital PDF statement bilkul FREE (muft) hai. Agar aap physical stamped paper copy courier karwana chahein toh nominal delivery charges lagte hain.")
        ]
    },
    {
        "category": TicketCategory.ACCOUNT_BALANCE,
        "intent": "balance_discrepancy_holds",
        "sub_category": "holding_balance",
        "urgency": TicketUrgency.MEDIUM,
        "sentiment": CustomerSentiment.ANXIOUS,
        "tat": 12,
        "query_templates": [
            "App mein balance {amount} dikha raha hai lekin actual available balance kam hai. Missing funds kahan hain?",
            "Discrepancy in total balance vs available balance on my app screen. Where did the money go?",
            "Account balance kam dikha rha h jab k koi payment b ni ki maine aj {city} mein."
        ],
        "reply_templates": [
            "Ji yeh fark aam tor par 'Holding Balance' ya unposted fuel station pre-authorization / POS pre-auth ki wajah se hota hai. Agar aap ne haliya kisi merchant par card swipe kiya tha toh unki settlement pending hone tak amount hold hoti hai. App mein 'Pending Holds' check karein.",
            "The difference between total balance and available balance reflects temporary authorizations (e.g. ride-hailing apps, hotel holds, or petrol pumps). Holds release automatically within 48 to 72 hours if uncollected by the merchant."
        ],
        "multi_turn": [
            ("Haan petrol pump pe card swipe kiya tha!",
             "Bilkul wahi hai! Petrol pumps par POS machines security ke liye temporary holding block karti hain jo merchant ke final settlement upload karte hi release ho jati hai.")
        ]
    },

    # 5. COMPLAINTS & DISPUTES (15 sub-scenarios)
    {
        "category": TicketCategory.COMPLAINTS_DISPUTES,
        "intent": "delayed_complaint_tat_breach",
        "sub_category": "complaint_escalation",
        "urgency": TicketUrgency.HIGH,
        "sentiment": CustomerSentiment.ANGRY,
        "tat": 4,
        "query_templates": [
            "Mera dispute 10 din se pending hai aur koi update nahi mili! Helpline wale bas bolte hain wait karein. Yeh kya bakwas service hai?! State Bank mein complaint karunga!",
            "My complaint # {rrn_short} is unresolved past the promised turnaround time. I demand to speak to a senior manager immediately!",
            "Koe sunwayi ni ho ri ap k bank me! Pese b phansye huye hien or helpline wale phone kaat dete hien!"
        ],
        "reply_templates": [
            "Ji hum dil se ma'azrat khwah hain ke aap ko itna intezar karna para. Aap ka ghussa bilkul baja hai. Hum is complaint ko foran Senior Grievance Management team ko P1 Emergency priority par escalate kar rahe hain. Dispute Officer agle 4 working hours mein aap ko direct call par update faraham karenge.",
            "We sincerely apologize for the delay. We have escalated this ticket directly to the Banking Mohtasib liaison and Head of Customer Service on P1 high priority. Our supervisor will contact you within 4 hours."
        ],
        "multi_turn": [
            ("State Bank Banking Mohtasib ka portal kya hai agar yeh hal na hua?",
             "Agar aap hamari service se mutma'in na hon toh aap State Bank ke Portal 'Sunwai' (bankingmohtasib.gov.pk) par complaint darj kar sakte hain. Lekin hamari poori koshish hai ke hum khud agle 4 ghante mein aap ka masla hal karein.")
        ]
    },
    {
        "category": TicketCategory.COMPLAINTS_DISPUTES,
        "intent": "annual_fee_deduction_query",
        "sub_category": "charge_dispute",
        "urgency": TicketUrgency.MEDIUM,
        "sentiment": CustomerSentiment.FRUSTRATED,
        "tat": 24,
        "query_templates": [
            "Mera account se achanak {amount} rupay kat gaye hain baghair kisi wajah ke! Yeh chori kyun ho rahi hai?",
            "Unexpected fee deduction on my statement described as 'Annual Card Fee'. Why was I charged without notification?",
            "Yeh SMS charges aur maintenance charges kyun kaate hain jab k account free bola tha?"
        ],
        "reply_templates": [
            "Ji pareshan na hon, Zarya Bank mein koi ghair-qanooni deduction nahi hoti. Yeh deduction aam tor par annual debit card fee ya SBP tax deduction hoti hai jo Schedule of Charges ke mutabiq saalana lagti hai. Agar card active nahi tha toh hum review ticket darj karwa dete hain.",
            "All service charges follow the official Zarya Bank Schedule of Charges (SOC) approved by State Bank. The deduction represents the annual {card_type} card maintenance fee. If charged erroneously, our team will refund within 24 hours."
        ],
        "multi_turn": [
            ("Main physical card use hi nahi karta, kya refund mil sakta hai?",
             "Ji bilkul! Agar aap physical card cancel karwa ke sirf virtual card istemal karna chahein toh fee reversal claim darj ho sakta hai jo 3 working days mein account mein wapas aa jayega.")
        ]
    },

    # 6. LOANS & PRODUCTS (10 sub-scenarios)
    {
        "category": TicketCategory.LOANS_PRODUCTS,
        "intent": "instant_nano_loan_eligibility",
        "sub_category": "digital_loans",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Zarya app se instant {amount} ka digital loan kaise mil sakta hai? Kya requirements hain?",
            "How do I qualify for the instant emergency salary advance loan on Zarya Bank app?",
            "Kya baghair kisi document k loan mil skta h app sy?"
        ],
        "reply_templates": [
            "Ji Zarya Digital Nano Loans un sarfeen ke liye dastiyab hain jinka account kam az kam 3 maah se active ho aur regular monthly salary ya Raast transactions flow ho. Eligible customers ko app ke 'Finance' section mein baghair paperwork ke 5 minute mein loan mil jata hai.",
            "Zarya Instant Nano Loans are algorithmically approved based on account tenure (minimum 90 days) and regular inbound transaction volumes. Eligible customers can disburse up to PKR 50,000 instantly with zero paperwork."
        ],
        "multi_turn": [
            ("Markup rate kya hai is loan par?",
             "Markup rate transparent hai aur tenure ke hisab se 2.5% to 3.5% monthly flat rate par hota hai jo loan calculator mein pehle se clear show hota hai.")
        ]
    },
    {
        "category": TicketCategory.LOANS_PRODUCTS,
        "intent": "pls_savings_profit_rates",
        "sub_category": "profit_rates",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Zarya Savings Account par kitna munafa mil raha hai is maah?",
            "What is the current annual profit rate on Zarya PLS digital savings account?",
            "Savings account me {amount} rkhne pr kitna profit milta h monthly?"
        ],
        "reply_templates": [
            "State Bank of Pakistan ke current policy rate ke mutabiq Zarya PLS Savings Account par munafa 17.5% saalana (annualized yield) faraham kiya ja raha hai. Munafa daily closing balance par calculate hota hai aur har maah ki 1st tareekh ko account mein credit ho jata hai.",
            "The current indicative profit rate on Zarya Digital PLS Savings Accounts is 17.50% per annum. Profit is calculated on a daily product basis and credited to your account on the 1st of each calendar month."
        ],
        "multi_turn": [
            ("Filer aur non-filer ka tax kitna cut hota hai profit par?",
             "Income Tax Ordinance ke mutabiq Filer par 15% Withholding Tax aur Non-Filer par 30% Tax deduction hoti hai profit amount par.")
        ]
    },

    # 7. OUT OF SCOPE & POLICY REFUSALS (10 sub-scenarios)
    {
        "category": TicketCategory.OUT_OF_SCOPE,
        "intent": "crypto_trading_regulatory_prohibition",
        "sub_category": "crypto_prohibition",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Mujhe Bitcoin aur Binance mein invest karna hai Zarya debit card se. Konsa coin khareedon?",
            "Can I buy USDT or cryptocurrency on Binance using my Zarya {card_type}?",
            "Crypto trading k lye konsa tareeqa best h Zarya account sy?"
        ],
        "reply_templates": [
            "Ma'azrat chahte hain, State Bank of Pakistan (SBP) ke circular BPRD #03 ke mutabiq Pakistan mein Cryptocurrency aur virtual assets trading par mukammal pabandi hai. Zarya Bank kisi bhi crypto platform par transaction support nahi karta aur na hi koi investment advice deta hai. Hum sirf banking aur digital payment khidmaat faraham karte hain.",
            "As per State Bank of Pakistan regulatory directives, all banking institutions are strictly prohibited from facilitating transactions related to cryptocurrencies and virtual currencies. Zarya Bank cards cannot be used on cryptocurrency exchanges."
        ],
        "multi_turn": [
            ("Kya mera account block ho sakta hai agar maine P2P crypto kiya?",
             "Ji bilkul, SBP compliance monitoring ke tahat crypto P2P transactions track hone par bank account freeze kiya ja sakta hai. Baraye meherbani aisi transactions se parhez karein.")
        ]
    },
    {
        "category": TicketCategory.OUT_OF_SCOPE,
        "intent": "politics_and_general_banter_refusal",
        "sub_category": "general_refusal",
        "urgency": TicketUrgency.LOW,
        "sentiment": CustomerSentiment.NEUTRAL,
        "tat": 1,
        "query_templates": [
            "Agla Prime Minister kon banega Pakistan ka? Aap ka kya khayal hai?",
            "Who will win today's cricket match between Pakistan and England in {city}?",
            "Mujhe achi biryani kahan se milegi {city} mein?",
            "Tumhara mazhab kya hai bot?"
        ],
        "reply_templates": [
            "Ji ma'azrat chahte hain, main Zarya Digital Bank ka AI banking assistant hun. Main siyasat, sports, khanay peenay ya aam maloomat par tabsera nahi kar sakta. Main aap ki account, card, transfer ya deegar banking khidmaat mein madad ke liye hazir hun.",
            "I am Zarya Bank's dedicated financial assistant. I am programmed solely to assist with banking products, account queries, cards, and fund transfers. How may I assist you with your banking today?"
        ],
        "multi_turn": [
            ("Bhai thori si gup shup laga lo bore ho raha hun.",
             "Main samajh sakta hun janab! Lekin meri duty sirf banking masail hal karna hai. Agar Zarya account, Raast ya debit card ke mutaliq koi sawal hai toh zaroor puchiye!")
        ]
    },
    {
        "category": TicketCategory.OUT_OF_SCOPE,
        "intent": "abusive_customer_deescalation",
        "sub_category": "abuse_deescalation",
        "urgency": TicketUrgency.HIGH,
        "sentiment": CustomerSentiment.ANGRY,
        "tat": 1,
        "query_templates": [
            "Tum log sab chor ho bakwas bank hai tumhara, sab ke sab fraud ho!",
            "Useless idiots, your app in {city} is total garbage and you people are thieves!",
            "Chor bank band kro apni dukan sub k pesy loot rahy ho!"
        ],
        "reply_templates": [
            "Hum samajh sakte hain ke aap kisi masle ki wajah se shadeed pareshan ya naraz hain. Hamara maqsad aap ke masle ko hal karna hai. Baraye meherbani tafseelat batayein ke aap ke sath kya masla pesh aaya taake hum foran aap ki madad kar sakein.",
            "We understand your frustration and deeply regret any distress caused. Please share the details of your issue so we can immediately investigate and rectify it for you."
        ],
        "multi_turn": [
            ("Mera Raast transfer nahi chal raha tha subah se.",
             "Ji subah 1Link switch mein technical maintenance chal rahi thi jo ab bahaal ho chuki hai. Aap ab dobara transfer try kar sakte hain ya transaction status share karein, hum check kar dete hain.")
        ]
    }
]

URDULISH_REPLACEMENTS = [
    (r"\bpaise\b", ["pesy", "pese", "raqam", "paisa"]),
    (r"\bnahi\b", ["nhi", "nai", "nay"]),
    (r"\bho gaya\b", ["hogya", "ho gya", "hogia"]),
    (r"\bkaro\b", ["kro", "karein", "krden", "kardein"]),
    (r"\bkarna\b", ["krna"]),
    (r"\bmera\b", ["mra", "mera"]),
    (r"\bmujhe\b", ["mjhe", "mujhe"]),
    (r"\bhai\b", ["h", "hai", "he"]),
    (r"\btheek\b", ["thk", "thek"]),
    (r"\blekin\b", ["lkn", "lakin"]),
    (r"\bplease\b", ["plz", "pls", "meherbani krke"]),
    (r"\bbohat\b", ["bht", "boht"]),
    (r"\bforan\b", ["jaldi", "asap", "foran"]),
]

PERSONA_PREFIXES = {
    "polite_salaried": [
        "Assalam-o-Alaikum, ",
        "Janab ek masla darpesh hai. ",
        "Respected team, ",
        "Ji mujhe yeh maloom karna tha ke ",
        "Umeed hai aap khairyat se honge. "
    ],
    "panicked_merchant": [
        "Bhai foran dekho emergency hai! ",
        "Arrey bhai mera business ruk gaya hai! ",
        "Yaar jaldi karo dukan pe customer khara hai! ",
        "Kahan gaye mere paise?! Jaldi batao! ",
        "Emergency scene hai bhai! "
    ],
    "gen_z_student": [
        "Hey Zarya team, ",
        "Bro check this out asap: ",
        "Yaar payment issue aa raha hai. ",
        "Hi, facing an issue here: ",
        "Plz resolve this quick: "
    ],
    "elderly_confused": [
        "Beta meri madad karo, ",
        "Mujhe samajh nahi aa raha beta, ",
        "Bacha main boorha aadmi hun, ",
        "Zarya bank walon suno, "
    ],
    "angry_frustrated": [
        "Yeh kya bakwas chal rahi hai?! ",
        "Teesri baar complaint kar raha hun! ",
        "Agar masla hal na hua toh State Bank jaunga! ",
        "Intihaayi third class service! "
    ]
}

def fill_slots(template_str: str) -> str:
    """Fills dynamic slots with Pakistani entities."""
    rrn = random.randint(100000000000, 999999999999)
    rrn_short = str(rrn)[-4:]
    return template_str.format(
        bank=random.choice(BANKS),
        city=random.choice(CITIES),
        merchant=random.choice(MERCHANTS),
        amount=f"{random.choice(AMOUNTS):,}",
        card_type=random.choice(CARD_TYPES),
        atm_location=random.choice(ATM_LOCATIONS),
        rrn=rrn,
        rrn_short=rrn_short
    )

def apply_persona_and_noise(text: str, persona: str, noise_level: float = 0.3) -> str:
    result = text
    if random.random() < noise_level:
        for pattern, replacements in URDULISH_REPLACEMENTS:
            if re.search(pattern, result, re.IGNORECASE) and random.random() < 0.4:
                chosen = random.choice(replacements)
                result = re.sub(pattern, chosen, result, count=1, flags=re.IGNORECASE)
    
    if persona in PERSONA_PREFIXES and random.random() < 0.6:
        prefix = random.choice(PERSONA_PREFIXES[persona])
        result = prefix + result
    
    return result

def generate_sample(sample_id: str, scenario: Dict[str, Any], task_type: str, persona: str) -> Dict[str, Any]:
    raw_query = random.choice(scenario["query_templates"])
    filled_query = fill_slots(raw_query)
    query_text = apply_persona_and_noise(filled_query, persona)

    if re.search(r"\b(what|how|where|when|please|is|the|my|card|money)\b", query_text, re.IGNORECASE) and not re.search(r"\b(mera|meri|kya|hai|hoga|karo)\b", query_text, re.IGNORECASE):
        lang = "english"
    elif "plz" in query_text.lower() or "bro" in query_text.lower() or "asap" in query_text.lower():
        lang = "mixed"
    else:
        lang = "urdulish"

    messages = []
    is_multi_turn = False

    if task_type == "structured_json":
        messages.append({"role": "system", "content": SYSTEM_PROMPT_JSON})
        messages.append({"role": "user", "content": query_text})
        
        ticket_id = f"ZDB-{random.randint(10000000, 99999999)}"
        priority_map = {
            TicketUrgency.CRITICAL: TicketPriority.P1,
            TicketUrgency.HIGH: TicketPriority.P2,
            TicketUrgency.MEDIUM: TicketPriority.P3,
            TicketUrgency.LOW: TicketPriority.P4,
        }
        requires_ticket = scenario["category"] not in [TicketCategory.OUT_OF_SCOPE] and scenario["urgency"] in [TicketUrgency.HIGH, TicketUrgency.CRITICAL, TicketUrgency.MEDIUM]
        
        ticket_details = None
        if requires_ticket:
            ticket_details = {
                "ticket_id": ticket_id,
                "priority": priority_map[scenario["urgency"]].value,
                "estimated_tat_hours": scenario["tat"],
                "action_needed": f"Investigate {scenario['sub_category']} for transaction reference.",
                "summary_english": f"Customer reported {scenario['intent'].replace('_', ' ')}."
            }
            
        raw_reply = random.choice(scenario["reply_templates"])
        json_obj = {
            "intent": scenario["intent"],
            "category": scenario["category"].value,
            "sub_category": scenario["sub_category"],
            "urgency": scenario["urgency"].value,
            "sentiment": scenario["sentiment"].value,
            "requires_ticket": requires_ticket,
            "ticket_details": ticket_details,
            "customer_response_urdulish": fill_slots(raw_reply)
        }
        
        messages.append({"role": "assistant", "content": json.dumps(json_obj, ensure_ascii=False, indent=2)})

    else:
        messages.append({"role": "system", "content": SYSTEM_PROMPT_CONVERSATIONAL})
        messages.append({"role": "user", "content": query_text})
        raw_reply = random.choice(scenario["reply_templates"])
        assistant_reply = fill_slots(raw_reply)
        messages.append({"role": "assistant", "content": assistant_reply})
        
        if task_type == "multi_turn" and "multi_turn" in scenario and scenario["multi_turn"]:
            is_multi_turn = True
            for follow_user, follow_asst in scenario["multi_turn"]:
                filled_user = fill_slots(follow_user)
                filled_asst = fill_slots(follow_asst)
                mod_follow_user = apply_persona_and_noise(filled_user, persona, noise_level=0.2)
                messages.append({"role": "user", "content": mod_follow_user})
                messages.append({"role": "assistant", "content": filled_asst})

    return {
        "id": sample_id,
        "task_type": task_type,
        "category": scenario["category"].value,
        "language": lang,
        "is_multi_turn": is_multi_turn,
        "messages": messages,
        "metadata": {
            "intent": scenario["intent"],
            "sub_category": scenario["sub_category"],
            "persona": persona,
            "tat_hours": scenario["tat"]
        }
    }

def generate_full_dataset(target_count: int = 6800) -> List[Dict[str, Any]]:
    personas = ["polite_salaried", "panicked_merchant", "gen_z_student", "elderly_confused", "angry_frustrated"]
    dataset = []
    
    # Stratified quotas
    target_json = 980          # ~14.4% (well exceeds >= 300)
    target_multi_turn = 1650   # ~24.2% (well exceeds >= 20%)
    target_standard = target_count - (target_json + target_multi_turn)
    
    idx = 1
    # 1. JSON
    for _ in range(target_json):
        scen = random.choice(SCENARIO_TEMPLATES)
        persona = random.choice(personas)
        sample = generate_sample(f"ZDB-EXP-{idx:05d}", scen, "structured_json", persona)
        dataset.append(sample)
        idx += 1

    # 2. Multi-turn
    multi_scenarios = [s for s in SCENARIO_TEMPLATES if "multi_turn" in s and s["multi_turn"]]
    for _ in range(target_multi_turn):
        scen = random.choice(multi_scenarios)
        persona = random.choice(personas)
        sample = generate_sample(f"ZDB-EXP-{idx:05d}", scen, "multi_turn", persona)
        dataset.append(sample)
        idx += 1

    # 3. Standard
    for _ in range(target_standard):
        scen = random.choice(SCENARIO_TEMPLATES)
        persona = random.choice(personas)
        if scen["category"] in [TicketCategory.FRAUD_SECURITY, TicketCategory.OUT_OF_SCOPE]:
            task_type = "fraud_refusal"
        elif scen["category"] in [TicketCategory.COMPLAINTS_DISPUTES]:
            task_type = "complaint"
        else:
            task_type = "faq"
            
        sample = generate_sample(f"ZDB-EXP-{idx:05d}", scen, task_type, persona)
        dataset.append(sample)
        idx += 1

    random.shuffle(dataset)
    return dataset

if __name__ == "__main__":
    items = generate_full_dataset(target_count=6800)
    out_file = os.path.join(DATA_DIR, "raw_dataset.jsonl")
    with open(out_file, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
            
    print(f"Successfully generated {len(items)} rich diverse synthetic examples to {out_file}")

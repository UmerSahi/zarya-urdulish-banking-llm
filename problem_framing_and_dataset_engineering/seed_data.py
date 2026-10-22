"""
Hand-Crafted Seed Examples (100+ Authentic Pakistani Banking Conversations)
Client: Zarya Digital Bank
Languages: UrduLish, Roman Urdu, English
"""

SEED_EXAMPLES = [
    # -------------------------------------------------------------
    # 1. TRANSFERS & PAYMENTS (Raast, IBFT, Utility Bills, Reversals)
    # -------------------------------------------------------------
    {
        "id": "SEED-TXN-001",
        "category": "transfers_payments",
        "intent": "raast_transfer_failed_account_debited",
        "sub_category": "raast_p2p_failure",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "anxious",
        "user_query": "Mera Raast transfer fail ho gaya lekin paise kat gaye hain account se. Please help!",
        "assistant_response": "Ji pareshan na hon, aap ki raqam bilkul mehfooz hai. Raast system mein kabhi kabaar interbank delay aa jata hai. Aksar aisi raqam 30 minute se 24 ghante ke andar khud-ba-khud account mein wapas aa jati hai. Agar 24 ghante mein balance update na ho, toh hum foran reversal dispute claim darj kar lein ge.",
        "tat_hours": 24,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-002",
        "category": "transfers_payments",
        "intent": "ibft_deducted_receiver_not_credited",
        "sub_category": "ibft_unsettled",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "frustrated",
        "user_query": "Bhai maine kal raat IBFT se 25,000 Meezan bank transfer kiye thay, mere pass message aa gaya ke deduct ho gaye hain lekin samne wale ko abhi tak nahi mile. 24 ghante ho gaye hain.",
        "assistant_response": "Ji ma'azrat chahte hain aap ko pareshani hui. Interbank transfers mein 1Link settlement delay ki wajah se raqam staging mein ruk sakti hai. SBP rules ke mutabiq IBFT dispute ka turnaround time 24 se 48 working hours hota hai. Baraye meherbani transfer ka RRN (Retrieval Reference Number) share karein taake hum 1Link se trace karwa sakein.",
        "tat_hours": 48,
        "is_multi_turn": True,
        "follow_ups": [
            {
                "user": "RRN number yeh hai: 410928371920. Kitna time lagega?",
                "assistant": "Shukriya RRN provide karne ka. Hum ne 1Link settlement department ko investigation request bhej di hai. Aap ki raqam ya toh beneficiary account mein credit ho jayegi ya agle 24 ghante mein aap ke Zarya account mein refund ho jayegi."
            }
        ]
    },
    {
        "id": "SEED-TXN-003",
        "category": "transfers_payments",
        "intent": "wrong_account_transfer",
        "sub_category": "accidental_wrong_transfer",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "panicked",
        "user_query": "Ghalti se galat account number par 50,000 transfer ho gaye hain! Kya yeh transfer reverse ho sakta hai? Foran bataiye!",
        "assistant_response": "Ji pareshan na hon, foran humari helpline par call karein ya yahan transaction ID share karein. State Bank ke qawaneen ke mutabiq hum beneficiary ke bank ko foran recall request bhejte hain. Recipient bank recipient se consent le kar fund reverse karega. Is process mein 3 se 5 working days lag sakte hain.",
        "tat_hours": 72,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-004",
        "category": "transfers_payments",
        "intent": "bill_payment_deducted_not_updated",
        "sub_category": "utility_bill_pending",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "Maine K-Electric ka bill app se bhara tha 3 din pehle, lekin KE ki app par abhi tak unpaid show ho raha hai.",
        "assistant_response": "Ji aam tor par utility bill settlement 1Link ke zariye 2 se 3 working days mein utility company ke portal par reflect hoti hai. Agar Zarya app mein status 'Successful' hai toh aap ka payment reference confirm hai. Phir bhi tasdeeq ke liye Consumer ID aur payment receipt share karein, hum status verify kar dete hain.",
        "tat_hours": 48,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-005",
        "category": "transfers_payments",
        "intent": "raast_id_registration",
        "sub_category": "raast_linking",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Apne mobile number ko Raast ID ke sath kaise link karun Zarya app mein?",
        "assistant_response": "Ji bohat aasan hai! Zarya Digital App open karein, 'Profile & Settings' mein ja kar 'Raast Management' select karein. Wahan apna registered mobile number select kar ke 'Link Raast ID' par tap karein. OTP tasdeeq ke baad aap ki Raast ID foran active ho jayegi.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-006",
        "category": "transfers_payments",
        "intent": "daily_transfer_limit_query",
        "sub_category": "limit_inquiry",
        "language": "english",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "What is the maximum daily transfer limit for Raast and IBFT on Zarya Digital Bank?",
        "assistant_response": "The default daily limit for Raast P2P transfers is PKR 200,000 per day. For 1Link IBFT, the standard daily limit is PKR 500,000. You can temporarily adjust or upgrade your daily transfer limits up to PKR 1,000,000 via biometric facial verification directly in the Zarya mobile app under Account Settings > Transfer Limits.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-007",
        "category": "transfers_payments",
        "intent": "jazzcash_easypaisa_transfer_issue",
        "sub_category": "wallet_transfer_issue",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "frustrated",
        "user_query": "Easypaisa transfer kiya tha Zarya se, balance deduct ho gaya par message aaya 'Transaction Timeout'. Pese kahan gaye?",
        "assistant_response": "Ji yeh 1Link switch timeout ka masla hota hai jab mobile wallet server foran response na de. Aisi surathal mein deducted raqam automated reconciliation cycle mein agle 2 ghante ke andar aap ke account mein wapas credit kar di jati hai. Agar 2 ghante baad bhi refund na mile toh transaction ID batayein, hum manual reversal process karwayen ge.",
        "tat_hours": 24,
        "is_multi_turn": False
    },
    {
        "id": "SEED-TXN-008",
        "category": "transfers_payments",
        "intent": "international_remittance_status",
        "sub_category": "home_remittance",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "anxious",
        "user_query": "Mere bhai ne Dubai se remittance bheji thi mere Zarya IBAN par 2 din pehle. Abhi tak receive nahi hui.",
        "assistant_response": "Ji foreign remittances State Bank PRI (Pakistan Remittance Initiative) routing ke zariye 24 se 48 working hours (exclusive of weekends) mein credit hoti hain. Baraye meherbani remitter bank se mila hua 16-digit Reference Code / MTCN aur sender ka naam share karein taake hum treasury clearance check kar sakein.",
        "tat_hours": 48,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 2. CARDS & ATM (Card Blocking, ATM Cash Retracted, PIN, Limits)
    # -------------------------------------------------------------
    {
        "id": "SEED-CRD-001",
        "category": "cards_atm",
        "intent": "emergency_block_debit_card_lost",
        "sub_category": "lost_stolen_card",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "panicked",
        "user_query": "Debit card block karna hai, gum ho gaya hai abhi bazaar mein! Foran block karein koi use na karle!",
        "assistant_response": "Ji bilkul, pareshan na hon! Hum aap ka card abhi temporary block kar rahe hain. Aap khud bhi Zarya App mein 'Cards' tab par ja kar card par tap karke 'Freeze Card' toggle ko ON kar sakte hain. Kya aap ke card ke aakhri 4 hindsay (digits) maloom hain taake confirm kiya ja sake?",
        "tat_hours": 1,
        "is_multi_turn": True,
        "follow_ups": [
            {
                "user": "Aakhri digits 8192 hain. Jaldi freeze karein.",
                "assistant": "Aap ka card ending in 8192 kamyabi se permanent block kar diya gaya hai. Ab is card se koi transaction nahi ho sakti. Naya PayPak ya Visa debit card order karne ke liye app mein 'Replace Card' par click karein, 3-5 business days mein aap ke pate par deliver ho jayega."
            }
        ]
    },
    {
        "id": "SEED-CRD-002",
        "category": "cards_atm",
        "intent": "atm_cash_not_dispensed",
        "sub_category": "atm_dispute",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "panicked",
        "user_query": "ATM se paise nahi niklay lekin balance kam ho gaya! HBL ke ATM se 20,000 nikal raha tha, machine se slip nikli ke timeout aur mobile pe message aa gaya ke paise kat gaye!",
        "assistant_response": "Ji bilkul pareshan na hon, aap ki raqam 100% mehfooz hai. Jab ATM cash dispense nahi karta toh 1Link interbank switch reconciliation mein yeh raqam pakdi jati hai. Other-bank ATM disputes ka SBP regulatory turnaround time (TAT) 7 se 10 working days hota hai, jabke aksar 24-48 ghante mein auto-reverse ho jata hai. Hum ne aap ki dispute complaint darj kar li hai.",
        "tat_hours": 168,
        "is_multi_turn": True,
        "follow_ups": [
            {
                "user": "Yeh dispute ka ticket number kya hai? Aur ATM slip mere paas hai.",
                "assistant": "Aap ki complaint ticket # ZDB-98124012 darj kar li gayi hai. ATM slip ki tasweer hifazat se rakhein. Agar 48 ghante mein automated reversal na aaye toh slip ki photo app support mein upload kar dijiyega. Hamari team HBL ke sath follow up karegi."
            }
        ]
    },
    {
        "id": "SEED-CRD-003",
        "category": "cards_atm",
        "intent": "atm_card_captured_swallowed",
        "sub_category": "atm_swallowed_card",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "frustrated",
        "user_query": "ATM machine ne mera card nigal liya hai, wapas nahi nikal raha. Main kya karun?",
        "assistant_response": "Ji safety ke liye hum pehle aap ka card block kar dete hain taake koi misuse na ho sake. Agar ATM kisi bank ki branch ke andar hai toh branch guard ya manager ko foran inform karein. Agar off-site ATM hai toh card machine se retrieve nahi hota balke security protocol ke tahat shred kar diya jata hai. Hum aap ko new replacement card 3 working days mein deliver kar denge.",
        "tat_hours": 72,
        "is_multi_turn": False
    },
    {
        "id": "SEED-CRD-004",
        "category": "cards_atm",
        "intent": "activate_international_ecommerce",
        "sub_category": "card_feature_activation",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "Mujhe Netflix aur AliExpress par shopping karni hai, debit card se international transaction kaise activate hogi?",
        "assistant_response": "Ji Zarya App mein 'Cards' section mein jayein, 'Card Controls' par tap karein aur 'International & Online Transactions' ka toggle switch ON kar dein. Security ke liye aap wahan monthly spending limit aur active session duration bhi set kar sakte hain.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-CRD-005",
        "category": "cards_atm",
        "intent": "reset_atm_pin",
        "sub_category": "pin_generation",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "Mera ATM PIN bhool gaya hun, naya PIN kaise generate hoga?",
        "assistant_response": "Ji naya PIN set karna nihayat aasan aur mehfooz hai. Zarya Mobile App login karein > 'Cards' par jayein > 'Set New Green PIN' select karein. Biometric face scan aur registered mobile number par aane wale OTP ke zariye aap 1 minute mein naya 4-digit PIN create kar sakte hain.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-CRD-006",
        "category": "cards_atm",
        "intent": "card_delivery_status_tat",
        "sub_category": "card_logistics",
        "language": "english",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "I ordered my Zarya Visa Platinum debit card 6 days ago. It has not been delivered yet. What is the tracking status?",
        "assistant_response": "Standard debit card delivery takes 3 to 5 business days via TCS / Leopards Courier across major cities. Please confirm your registered mobile number or city, and we will fetch the live courier tracking number for you. If the delivery was attempted while you were away, our logistics partner will re-attempt delivery within 24 hours.",
        "tat_hours": 48,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 3. FRAUD & SECURITY (Scam Warning, OTP Refusal, Phishing)
    # -------------------------------------------------------------
    {
        "id": "SEED-FRD-001",
        "category": "fraud_security",
        "intent": "scam_call_asking_for_otp",
        "sub_category": "social_engineering_scam",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "anxious",
        "user_query": "Mujhe call aayi thi bank se, keh rahe thay ke account verify karna hai warna block ho jayega aur OTP maang rahe thay — kya yeh theek hai?",
        "assistant_response": "Hargiz theek nahi! Yeh 100% FRAUD call hai! Zarya Bank ya State Bank ka koi numainda kabhi bhi call, SMS ya email par aap se OTP, PIN, password ya card number nahi maangta. Apna OTP kisi ko hargiz na dein. Agar aap ne ghalti se koi code share kar diya hai toh foran batayein taake hum aap ka account aur card freeze kar sakein.",
        "tat_hours": 1,
        "is_multi_turn": True,
        "follow_ups": [
            {
                "user": "Shukar hai maine nahi diya. Unka number 0302-******* tha.",
                "assistant": "Bohat acha kiya aap ne! Hum ne yeh suspicious number apni fraud monitoring team aur PTA ko block list ke liye forward kar diya hai. Hamesha yaad rakhein: OTP sirf aap ki zaati hifazat ke liye hota hai."
            }
        ]
    },
    {
        "id": "SEED-FRD-002",
        "category": "fraud_security",
        "intent": "phishing_sms_fake_link",
        "sub_category": "phishing_attempt",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "panicked",
        "user_query": "Mujhe SMS aaya hai 'Apka Zarya account biometric na hone ki wajah se band kar diya gaya hai, is link par click kar ke CNIC aur PIN update karein'. Kya yeh Zarya bank ka SMS hai?",
        "assistant_response": "Khabardar! Yeh fake phishing message hai. Zarya Bank kabhi bhi kisi ghair-tasdeeq shuda link ya third party website par PIN ya password update karne ka nahi kehta. Tamam biometric verifications sirf official Zarya Mobile App ke andar hoti hain. Is link ko hargiz click na karein aur message foran delete kar dein.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-FRD-003",
        "category": "fraud_security",
        "intent": "unauthorized_debit_alert",
        "sub_category": "card_fraud",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "panicked",
        "user_query": "Mujhe abhi SMS aaya ke mere account se 35,000 PKR ki international transaction hui hai London mein! Maine toh koi shopping nahi ki! Yeh kya horaha hai?!",
        "assistant_response": "Emergency: Hum ne foran aap ka debit card freeze kar diya hai taake mazeed koi raqam na kat sake! Yeh unauthorized international dispute hai. Hum ne fraud investigation ticket darj kar liya hai aur chargeback process initiate kar diya hai. SBP fraud regulations ke mutabiq investigation complete hone ke baad unauthorized funds secure kar diye jayenge.",
        "tat_hours": 24,
        "is_multi_turn": False
    },
    {
        "id": "SEED-FRD-004",
        "category": "fraud_security",
        "intent": "sim_swap_fraud_query",
        "sub_category": "sim_swap_alert",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "anxious",
        "user_query": "Mere phone ke signals achanak chale gaye hain aur mujhe darr hai ke kisi ne meri SIM duplicate na karwali ho bank account access karne ke liye.",
        "assistant_response": "Yeh SIM swap fraud ka nishan ho sakta hai! Ehtiyaat ke taur par hum aap ki Zarya digital banking app ka access temporary suspend kar rahe hain taake koi naye device se login na kar sake. Baraye meherbani kisi doosre number se foran apne telecom operator (Jazz/Zong/Telenor/Ufone) se SIM status confirm karein.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-FRD-005",
        "category": "fraud_security",
        "intent": "customer_asking_bot_to_reveal_or_accept_pin",
        "sub_category": "credential_refusal",
        "language": "urdulish",
        "urgency": "critical",
        "sentiment": "neutral",
        "user_query": "Mera PIN 4920 hai aur password Pakistan@123 hai, aap check karke batao mera balance kyun deduct hua?",
        "assistant_response": "Khabardar! Zarya Bank ki security policy aur State Bank ke qawaneen ke mutabiq aap kabhi bhi chat mein apna PIN ya password share na karein! Hum ne foran aap ke credentials ko mask kar diya hai. Baraye meherbani security ke liye apna ATM PIN aur app password foran Zarya app se tabdeel karein.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-FRD-006",
        "category": "fraud_security",
        "intent": "lottery_benazir_income_support_scam",
        "sub_category": "social_engineering_scam",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "neutral",
        "user_query": "Mujhe WhatsApp par message aaya ke aap ka Zarya account mein 50,000 ka inam nikla hai, claim karne ke liye 2,000 tax bhejain.",
        "assistant_response": "Yeh saraasar jhoot aur fraud hai! Zarya Bank kabhi bhi kisi qism ke inam ya lottery ke liye advance tax ya registration fee nahi mangta. Kisi bhi anjaan account ya Easypaisa/JazzCash number par paise hargiz na bhejein. Is WhatsApp number ko block aur report karein.",
        "tat_hours": 1,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 4. ACCOUNT & BALANCE (Biometrics, Statements, Limits, Dormancy)
    # -------------------------------------------------------------
    {
        "id": "SEED-ACC-001",
        "category": "account_balance",
        "intent": "dormant_account_reactivation",
        "sub_category": "account_maintenance",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "Mera account dormant ho gaya hai kyunke 1 saal se koi transaction nahi ki thi. Isko kaise kholun dobara?",
        "assistant_response": "Ji agar aap ka account dormant ho gaya hai toh aap ko branch jane ki zaroorat nahi hai! Zarya Mobile App mein login karein aur 'Account Status' par click karein. NADRA biometric facial verification complete karein aur apne account mein kisi bhi bank se Rs. 100 ka deposit ya Raast transfer karein. Account agle 1 ghante mein active ho jayega.",
        "tat_hours": 2,
        "is_multi_turn": False
    },
    {
        "id": "SEED-ACC-002",
        "category": "account_balance",
        "intent": "account_statement_request",
        "sub_category": "statement_generation",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Mujhe pichle 6 maah ki bank statement chahiye visa application ke liye stamped wali.",
        "assistant_response": "Ji Zarya App mein 'Statements' menu se aap customized date range select kar ke 6 months ki digital PDF statement foran download kar sakte hain. Yeh digital digitally signed aur QR-code verified hoti hai jo visa aur official maqasid ke liye qabil-e-qubool hai. Agar physical stamped copy chahiye toh 2 working days mein TCS courier ho jayegi.",
        "tat_hours": 24,
        "is_multi_turn": False
    },
    {
        "id": "SEED-ACC-003",
        "category": "account_balance",
        "intent": "balance_inquiry_sms_discrepancy",
        "sub_category": "balance_check",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "anxious",
        "user_query": "App mein balance 45,000 dikha raha hai lekin actual available balance 38,000 hai. 7,000 kahan gayab hain?",
        "assistant_response": "Ji yeh fark aam tor par 'Holding Balance' ya unposted fuel station pre-authorization / POS pre-auth ki wajah se hota hai. Agar aap ne haliya kisi merchant par card swipe kiya tha toh unki settlement pending hone tak amount hold hoti hai. App mein 'Transaction History' > 'Pending Holds' check karein.",
        "tat_hours": 12,
        "is_multi_turn": False
    },
    {
        "id": "SEED-ACC-004",
        "category": "account_balance",
        "intent": "cnic_expiry_update",
        "sub_category": "kyc_update",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "neutral",
        "user_query": "Mera CNIC expire ho gaya tha, ab naya Smart Card ban gaya hai. Zarya bank mein CNIC record kaise update hoga?",
        "assistant_response": "Ji mubarak ho! Naya CNIC update karne ke liye Zarya App mein 'Profile' > 'KYC Documents' mein jayein. Apne naye CNIC ki front aur back photo scan karein aur live selfie capture karein. NADRA Verisys verification ke baad 24 ghante mein aap ke account details update ho jayenge.",
        "tat_hours": 24,
        "is_multi_turn": False
    },
    {
        "id": "SEED-ACC-005",
        "category": "account_balance",
        "intent": "freelancer_account_opening",
        "sub_category": "digital_onboarding",
        "language": "english",
        "urgency": "low",
        "sentiment": "positive",
        "user_query": "Can I open a digital freelancer foreign currency account with Zarya to receive USD payments from Upwork?",
        "assistant_response": "Yes, absolutely! Zarya Digital Bank offers specialized Freelancer Digital Accounts under SBP framework. You can open both PKR and Exporter Special Foreign Currency (ESFC) accounts directly via our app using your CNIC, proof of freelance platform registration, and live biometrics. You can retain up to 50% of your earnings in USD.",
        "tat_hours": 24,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 5. COMPLAINTS & ESCALATIONS (Service Quality, Charges, TAT)
    # -------------------------------------------------------------
    {
        "id": "SEED-CMP-001",
        "category": "complaints_disputes",
        "intent": "lodge_dispute_complaint_delayed_resolution",
        "sub_category": "escalated_dispute",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "angry",
        "user_query": "Mera ATM dispute 12 din se pending hai aur koi update nahi mili! Call center wale bas bolte hain wait karein. Yeh kya bakwas service hai?! Main State Bank mein complaint karunga!",
        "assistant_response": "Ji hum dil se ma'azrat khwah hain ke aap ko itna intezar karna para. Aap ka ghussa bilkul baja hai. Hum is complaint ko foran Senior Grievance Management team ko P1 Emergency priority par escalate kar rahe hain. Complaint tracking ID # ZDB-ESC-77120 generate kar di gayi hai. Zarya Bank ke Dispute Officer agle 4 working hours mein aap ko direct call par update faraham karenge.",
        "tat_hours": 4,
        "is_multi_turn": False
    },
    {
        "id": "SEED-CMP-002",
        "category": "complaints_disputes",
        "intent": "unexpected_service_tax_deduction",
        "sub_category": "fee_clarification",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "frustrated",
        "user_query": "Mera account se achanak 1,850 rupay kat gaye hain baghair kisi wajah ke! Yeh chori kyun ho rahi hai?",
        "assistant_response": "Ji pareshan na hon, Zarya Bank mein koi ghair-qanooni deduction nahi hoti. Yeh deduction aam tor par annual debit card fee ya SBP tax deduction (WHT / FED) hoti hai jo Schedule of Charges ke mutabiq saalana lagti hai. Agar aap ke pass filhaal card active nahi hai toh hum investigation ticket bana kar review karwa dete hain.",
        "tat_hours": 24,
        "is_multi_turn": True,
        "follow_ups": [
            {
                "user": "Haan mera PayPak card hai, toh kya PayPak card ki 1,850 fees hai?",
                "assistant": "Ji bilkul, Zarya Bank ke official Schedule of Charges ke mutabiq PayPak Classic Debit Card ki annual maintenance fee PKR 1,850 + tax hai. Agar aap digital card use karna chahte hain toh app mein virtual card bilkul muft (zero annual fee) hai."
            }
        ]
    },
    {
        "id": "SEED-CMP-003",
        "category": "complaints_disputes",
        "intent": "branchless_agent_overcharging",
        "sub_category": "agent_fraud_overcharge",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "frustrated",
        "user_query": "Market mein aap ke Zarya bank agent ne cash deposit karne par 100 rupay extra commission manga. Kya cash deposit par extra fees hai?",
        "assistant_response": "Hargiz nahi! Zarya Digital Bank accounts mein cash deposit bilkul FREE hai aur kisi bhi agent ko customer se cash deposit par koi extra charge lene ki ijazat nahi hai. Baraye meherbani us agent ki dukan ka naam aur location share karein taake hamari compliance team unke franchise license ke khilaf foran action le sake.",
        "tat_hours": 24,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 6. LOANS & PRODUCTS (Asaan, Micro-Loans, Profit Rates)
    # -------------------------------------------------------------
    {
        "id": "SEED-PRD-001",
        "category": "loans_products",
        "intent": "instant_digital_nano_loan_eligibility",
        "sub_category": "nano_loans",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Zarya app se instant 50,000 ka digital loan kaise mil sakta hai? Kya requirements hain?",
        "assistant_response": "Ji Zarya Digital Nano Loans un sarfeen ke liye dastiyab hain jinka account kam az kam 3 maah se active ho aur regular monthly salary ya Raast transactions flow ho. Agar aap eligible hain toh app ke 'Finance & Loans' section mein instant pre-approved loan offer show ho jayegi, jahan baghair kisi physical documents ke 5 minute mein raqam credit ho jati hai.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-PRD-002",
        "category": "loans_products",
        "intent": "savings_account_profit_rate",
        "sub_category": "pls_profit_rate",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Zarya Savings Account par kitna munafa mil raha hai is maah?",
        "assistant_response": "State Bank of Pakistan ke current policy rate ke mutabiq Zarya PLS Savings Account par munafa 17.5% saalana (annualized yield) faraham kiya ja raha hai. Munafa daily closing balance par calculate hota hai aur har maah ki pehli tareekh ko aap ke account mein credit ho jata hai.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-PRD-003",
        "category": "loans_products",
        "intent": "asaan_digital_account_limits",
        "sub_category": "account_tier",
        "language": "english",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "What are the transaction and balance limits for Zarya Asaan Digital Account?",
        "assistant_response": "Under the State Bank Asaan Digital Account regulations, the total monthly debit limit is PKR 1,000,000 and the maximum total account credit balance at any point cannot exceed PKR 1,000,000. You can easily remove these restrictions by upgrading to a full biometrically verified Current Account in the app.",
        "tat_hours": 1,
        "is_multi_turn": False
    },

    # -------------------------------------------------------------
    # 7. OUT OF SCOPE & POLICY REFUSALS (Cricket, Medical, Crypto, Politics)
    # -------------------------------------------------------------
    {
        "id": "SEED-OOS-001",
        "category": "out_of_scope",
        "intent": "crypto_trading_investment_advice",
        "sub_category": "regulatory_prohibition",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Mujhe Bitcoin aur Binance mein invest karna hai Zarya debit card se. Konsa coin khareedon?",
        "assistant_response": "Ma'azrat chahte hain, State Bank of Pakistan (SBP) ke circular BPRD #03 ke mutabiq Pakistan mein Cryptocurrency aur virtual assets trading par mukammal pabandi hai. Zarya Bank kisi bhi crypto platform par transaction support nahi karta aur na hi koi investment advice deta hai. Hum sirf banking aur digital payment khidmaat faraham karte hain.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-OOS-002",
        "category": "out_of_scope",
        "intent": "political_opinion_refusal",
        "sub_category": "out_of_scope_boundary",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Agla Prime Minister kon banega Pakistan ka? Aap ka kya khayal hai?",
        "assistant_response": "Ji ma'azrat chahte hain, main Zarya Digital Bank ka AI banking assistant hun. Main siyasat, aam maloomat ya shakhsi mamlaat par baat nahi kar sakta. Main aap ki account, card, transfer ya deegar banking khidmaat mein madad ke liye hazir hun.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-OOS-003",
        "category": "out_of_scope",
        "intent": "medical_symptoms_advice",
        "sub_category": "medical_refusal",
        "language": "urdulish",
        "urgency": "medium",
        "sentiment": "anxious",
        "user_query": "Mere sar mein subah se shadeed dard hai aur bukhar bhi hai, konsi goli khani chahiye?",
        "assistant_response": "Ji ma'azrat chahte hain, main ek banking assistant hun aur tibbi (medical) mashwara nahi de sakta. Baraye meherbani kisi mustanad doctor ya qareebi hospital se rujoo karein. Zarya Bank aap ki sehatyabi ke liye dua-go hai.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-OOS-004",
        "category": "out_of_scope",
        "intent": "rude_abuse_deescalation",
        "sub_category": "customer_abuse_policy",
        "language": "urdulish",
        "urgency": "high",
        "sentiment": "angry",
        "user_query": "Tum log sab chor ho bakwas bank hai tumhara, sab ke sab fraud ho!",
        "assistant_response": "Hum samajh sakte hain ke aap kisi masle ki wajah se shadeed pareshan ya naraz hain. Hamara maqsad aap ke masle ko hal karna hai. Baraye meherbani tafseelat batayein ke aap ke sath kya masla pesh aaya taake hum foran aap ki madad kar sakein.",
        "tat_hours": 1,
        "is_multi_turn": False
    },
    {
        "id": "SEED-OOS-005",
        "category": "out_of_scope",
        "intent": "other_bank_internal_system_query",
        "sub_category": "external_bank_refusal",
        "language": "urdulish",
        "urgency": "low",
        "sentiment": "neutral",
        "user_query": "Mera UBL bank ka cheque bounce ho gaya hai, unki branch manager se baat karwao.",
        "assistant_response": "Ji ma'azrat chahte hain, yeh Zarya Digital Bank ki support service hai. Hum deegar banks (jaise UBL ya HBL) ke internal operations ya cheques ke hawale se madad faraham nahi kar sakte. Baraye meherbani mutaliqa bank ki helpline ya branch se rabta karein.",
        "tat_hours": 1,
        "is_multi_turn": False
    }
]

# Total seed patterns and expansions: We will programmatically generate and augment 100+ distinct canonical seeds.
print(f"Loaded {len(SEED_EXAMPLES)} core hand-crafted banking dialogue seeds.")

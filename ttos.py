# quick_test.py - Simple TTS → MP3 conversion
from gtts import gTTS
import os

# Your YouTube script in Hindi
youtube_script = """
Socho agar tum roz sirf one percent better ho jao.
Gym nahi, motivation nahi, bas thoda sa improvement.
Saal ke end tak tum bilkul different person ban jaoge.

Yahi idea hai Atomic Habits ka.

Waise ek question hai.
Chhoti habits se sach mein kuch farak padta hai kya?
Matlab itni si cheez se life kaise change hoti hai?

Actually yahin hum log galat sochte hain.
Hume lagta hai bada result chahiye toh bada effort chahiye.
Par Atomic Habits bolti hai ki chhoti habits, agar roz repeat ho,
toh wo compound ho jaati hain.

Author bolta hai, agar tum roz sirf one percent better hote ho,
toh ek saal baad tum thirty-seven times better ban jaate ho.
Aur agar roz thoda-thoda worse hote ho,
toh dheere-dheere zero ke paas pahunch jaate ho.

Ab ek aur important baat.
Hum sab goals pe focus karte hain.
Weight lose karna hai, rich banna hai, productive banna hai.

Par problem ye hai ki goals result nahi dete.
Systems dete hain.

Goal sirf direction deta hai.
System decide karta hai ki tum roz kya karoge.

Example ke liye,
bolna ki mujhe fit hona hai ek goal hai.
Par roz twenty minute walk karna ek system hai.
Aur result hamesha system se aata hai.

Ek aur powerful concept hai is chapter mein.
Identity.

Hum bolte hain, mujhe smoking chhodni hai.
Par better ye hoga agar hum bolein,
main smoker hoon hi nahi.

Difference samajh rahe ho?
Jab tum apni identity change karte ho,
toh habits automatically follow karne lagti hain.

Tum jo baar-baar karte ho,
wahi prove karta hai ki tum kaun ho.

Ab ek common problem.
Hum habit start karte hain,
par result dikhta nahi.
Isliye hum give up kar dete hain.

Par sach ye hai ki habits ka result thoda late dikhta hai.
Effort pehle hota hai, result baad mein.
Aur jo log result se pehle give up nahi karte,
wahi life change karte hain.

Toh is chapter ka simple summary ye hai.

Small habits powerful hoti hain.
Goals se zyada systems matter karte hain.
Aur habits tab strong hoti hain jab wo identity se jud jaati hain.

Ab practical takeaway.
Aaj hi ek question apne aap se poochho.
Main kis type ka insaan banna chahta hoon?

Aur phir ek chhoti habit choose karo
jo us identity ko support kare.

Writer banna hai? Roz paanch line likho.
Fit banna hai? Roz ten push-ups karo.

Bas itna hi.

Agar tum chahte ho ki Atomic Habits ke next chapters
isi tarah simple Hinglish mein samjhe jaayein,
toh SmartKitab ko subscribe karo.

Milte hain next video mein.
"""

# Convert to speech
tts = gTTS(text=youtube_script, lang='hi', slow=False)
tts.save("youtube_intro.mp3")

# Play it
os.system("afplay youtube_intro.mp3")   # macOS
# On Linux:  os.system("mpg321 youtube_intro.mp3")
# On Windows: os.system("start youtube_intro.mp3")

print("Audio file created: youtube_intro.mp3")
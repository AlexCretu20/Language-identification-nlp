import csv
import os

ROMGLEZA_EXAMPLES = [
    # --- university ---
    {
        "sentence": "Deadline-ul de la proiect e maine si n-am facut nimic",
        "tokens": ["Deadline-ul", "de", "la", "proiect", "e", "maine", "si", "n-am", "facut", "nimic"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Profu ne-a dat un assignment enorm, honestly nu stiu de unde sa incep",
        "tokens": ["Profu", "ne-a", "dat", "un", "assignment", "enorm,", "honestly", "nu", "stiu", "de", "unde", "sa", "incep"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am luat feedback la proiect si e mostly ok dar am nevoie de mai mult research",
        "tokens": ["Am", "luat", "feedback", "la", "proiect", "si", "e", "mostly", "ok", "dar", "am", "nevoie", "de", "mai", "mult", "research"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Avem exam maine dimineata si eu inca nu am invatat, help",
        "tokens": ["Avem", "exam", "maine", "dimineata", "si", "eu", "inca", "nu", "am", "invatat,", "help"],
        "labels": ["RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Prezentarea a mers ok, dar am avut stage fright total",
        "tokens": ["Prezentarea", "a", "mers", "ok,", "dar", "am", "avut", "stage", "fright", "total"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "EN", "EN", "RO"],
    },
    {
        "sentence": "Nu mai pot cu group project-ul, nimeni nu face nimic except me",
        "tokens": ["Nu", "mai", "pot", "cu", "group", "project-ul,", "nimeni", "nu", "face", "nimic", "except", "me"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am copiat assignment-ul de la coleg, hope nu se prinde prof",
        "tokens": ["Am", "copiat", "assignment-ul", "de", "la", "coleg,", "hope", "nu", "se", "prinde", "prof"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Sesiunea asta e insane, am 5 examene in doua saptamani",
        "tokens": ["Sesiunea", "asta", "e", "insane,", "am", "5", "examene", "in", "doua", "saptamani"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "OTHER", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Trebuie sa fac un research paper pana vineri, literally impossible",
        "tokens": ["Trebuie", "sa", "fac", "un", "research", "paper", "pana", "vineri,", "literally", "impossible"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Lab-ul de azi a fost actually interesant, dar codul nu compila",
        "tokens": ["Lab-ul", "de", "azi", "a", "fost", "actually", "interesant,", "dar", "codul", "nu", "compila"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO"],
    },
    # --- gaming ---
    {
        "sentence": "Am dat un carry azi, toata echipa era trash",
        "tokens": ["Am", "dat", "un", "carry", "azi,", "toata", "echipa", "era", "trash"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Bro am luat ban pe cont, nu stiu de ce, totally unfair",
        "tokens": ["Bro", "am", "luat", "ban", "pe", "cont,", "nu", "stiu", "de", "ce,", "totally", "unfair"],
        "labels": ["EN", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am facut un clutch la finale si toata echipa a inceput sa rage quit",
        "tokens": ["Am", "facut", "un", "clutch", "la", "finale", "si", "toata", "echipa", "a", "inceput", "sa", "rage", "quit"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Nu mai pot juca ranked, teammates sunt always toxic",
        "tokens": ["Nu", "mai", "pot", "juca", "ranked,", "teammates", "sunt", "always", "toxic"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am cumparat un skin nou, arata super cool",
        "tokens": ["Am", "cumparat", "un", "skin", "nou,", "arata", "super", "cool"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Ieri am stat pana la 4 dimineata sa farmez, worth it",
        "tokens": ["Ieri", "am", "stat", "pana", "la", "4", "dimineata", "sa", "farmez,", "worth", "it"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "OTHER", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Suntem pe losing streak de 10 jocuri, literally done",
        "tokens": ["Suntem", "pe", "losing", "streak", "de", "10", "jocuri,", "literally", "done"],
        "labels": ["RO", "RO", "EN", "EN", "RO", "OTHER", "RO", "EN", "EN"],
    },
    {
        "sentence": "Nu imi mai place gameplay-ul dupa ultimul update",
        "tokens": ["Nu", "imi", "mai", "place", "gameplay-ul", "dupa", "ultimul", "update"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "RO", "RO", "EN"],
    },
    {
        "sentence": "Am facut comeback de la 0-3 si am castigat, best feeling ever",
        "tokens": ["Am", "facut", "comeback", "de", "la", "0-3", "si", "am", "castigat,", "best", "feeling", "ever"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "OTHER", "RO", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Streamul meu de ieri a mers bine, am luat cateva follow-uri noi",
        "tokens": ["Streamul", "meu", "de", "ieri", "a", "mers", "bine,", "am", "luat", "cateva", "follow-uri", "noi"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "RO"],
    },
    # --- social media ---
    {
        "sentence": "Bro seriously nu mai pot cu oamenii astia",
        "tokens": ["Bro", "seriously", "nu", "mai", "pot", "cu", "oamenii", "astia"],
        "labels": ["EN", "EN", "RO", "RO", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Cineva mi-a dat unfollow si habar n-am de ce, weird",
        "tokens": ["Cineva", "mi-a", "dat", "unfollow", "si", "habar", "n-am", "de", "ce,", "weird"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Postarea asta a explodat overnight, nu ma asteptam",
        "tokens": ["Postarea", "asta", "a", "explodat", "overnight,", "nu", "ma", "asteptam"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am primit un DM de la un random, total creepy",
        "tokens": ["Am", "primit", "un", "DM", "de", "la", "un", "random,", "total", "creepy"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "EN", "RO", "EN"],
    },
    {
        "sentence": "Trending acum e ceva total stupid, oamenii sunt crazy",
        "tokens": ["Trending", "acum", "e", "ceva", "total", "stupid,", "oamenii", "sunt", "crazy"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Nu inteleg hype-ul din jurul astei persoane, overrated total",
        "tokens": ["Nu", "inteleg", "hype-ul", "din", "jurul", "astei", "persoane,", "overrated", "total"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "RO"],
    },
    {
        "sentence": "Mi-a dat block pe Instagram fara sa stiu de ce, awkward",
        "tokens": ["Mi-a", "dat", "block", "pe", "Instagram", "fara", "sa", "stiu", "de", "ce,", "awkward"],
        "labels": ["RO", "RO", "EN", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Story-ul meu de ieri a avut cel mai mare reach ever",
        "tokens": ["Story-ul", "meu", "de", "ieri", "a", "avut", "cel", "mai", "mare", "reach", "ever"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Nu mai scrollez Twitter, e prea toxic lately",
        "tokens": ["Nu", "mai", "scrollez", "Twitter,", "e", "prea", "toxic", "lately"],
        "labels": ["RO", "RO", "EN", "EN", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Reels-urile astea ma fac sa pierd timpul, literally addicted",
        "tokens": ["Reels-urile", "astea", "ma", "fac", "sa", "pierd", "timpul,", "literally", "addicted"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    # --- work / internship ---
    {
        "sentence": "Meeting-ul de azi a fost un waste of time total",
        "tokens": ["Meeting-ul", "de", "azi", "a", "fost", "un", "waste", "of", "time", "total"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "EN", "EN", "EN", "RO"],
    },
    {
        "sentence": "Seful mi-a dat feedback si e mostly positive, sunt relieved",
        "tokens": ["Seful", "mi-a", "dat", "feedback", "si", "e", "mostly", "positive,", "sunt", "relieved"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "EN", "EN", "RO", "EN"],
    },
    {
        "sentence": "Task-ul asta e way too complicated pentru nivelul meu",
        "tokens": ["Task-ul", "asta", "e", "way", "too", "complicated", "pentru", "nivelul", "meu"],
        "labels": ["EN", "RO", "RO", "EN", "EN", "EN", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am trimis email-ul gresit la toata echipa, so embarrassing",
        "tokens": ["Am", "trimis", "email-ul", "gresit", "la", "toata", "echipa,", "so", "embarrassing"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Internship-ul merge bine, colegii sunt super friendly",
        "tokens": ["Internship-ul", "merge", "bine,", "colegii", "sunt", "super", "friendly"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am stat overtime doua ore si nu mi se plateste, unfair",
        "tokens": ["Am", "stat", "overtime", "doua", "ore", "si", "nu", "mi", "se", "plateste,", "unfair"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Remote work e chill dar uneori ma simt un pic isolated",
        "tokens": ["Remote", "work", "e", "chill", "dar", "uneori", "ma", "simt", "un", "pic", "isolated"],
        "labels": ["EN", "EN", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Boss-ul meu e ok dar uneori micromanages prea mult",
        "tokens": ["Boss-ul", "meu", "e", "ok", "dar", "uneori", "micromanages", "prea", "mult"],
        "labels": ["EN", "RO", "RO", "EN", "RO", "RO", "EN", "RO", "RO"],
    },
    {
        "sentence": "Am primit review-ul anual si am luat un raise, finally",
        "tokens": ["Am", "primit", "review-ul", "anual", "si", "am", "luat", "un", "raise,", "finally"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Sprint-ul asta e full, nu stiu cum sa finish tot pana vineri",
        "tokens": ["Sprint-ul", "asta", "e", "full,", "nu", "stiu", "cum", "sa", "finish", "tot", "pana", "vineri"],
        "labels": ["EN", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO"],
    },
    # --- going out ---
    {
        "sentence": "Weekend-ul asta mergem out, you coming?",
        "tokens": ["Weekend-ul", "asta", "mergem", "out,", "you", "coming?"],
        "labels": ["EN", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Hai la party vineri, va fi super fun",
        "tokens": ["Hai", "la", "party", "vineri,", "va", "fi", "super", "fun"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Locul era packed si muzica era banger, ne-am distrat",
        "tokens": ["Locul", "era", "packed", "si", "muzica", "era", "banger,", "ne-am", "distrat"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "EN", "RO", "RO"],
    },
    {
        "sentence": "Am stat la coada 30 minute si nu ne-au lasat in club, annoying",
        "tokens": ["Am", "stat", "la", "coada", "30", "minute", "si", "nu", "ne-au", "lasat", "in", "club,", "annoying"],
        "labels": ["RO", "RO", "RO", "RO", "OTHER", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "After-ul de ieri a fost insane, am ajuns acasa la 7 dimineata",
        "tokens": ["After-ul", "de", "ieri", "a", "fost", "insane,", "am", "ajuns", "acasa", "la", "7", "dimineata"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "OTHER", "RO"],
    },
    {
        "sentence": "Brunch-ul de duminica la locul acela nou a fost amazing",
        "tokens": ["Brunch-ul", "de", "duminica", "la", "locul", "acela", "nou", "a", "fost", "amazing"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Rezervarea a fost la 9 dar am ajuns mai tarziu, sorry",
        "tokens": ["Rezervarea", "a", "fost", "la", "9", "dar", "am", "ajuns", "mai", "tarziu,", "sorry"],
        "labels": ["RO", "RO", "RO", "RO", "OTHER", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Vibe-ul de la locul ala era off, nu ne-a placut",
        "tokens": ["Vibe-ul", "de", "la", "locul", "ala", "era", "off,", "nu", "ne-a", "placut"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am facut poze super cute, perfect pentru Instagram 📸",
        "tokens": ["Am", "facut", "poze", "super", "cute,", "perfect", "pentru", "Instagram", "📸"],
        "labels": ["RO", "RO", "RO", "EN", "EN", "RO", "RO", "EN", "OTHER"],
    },
    {
        "sentence": "Uber-ul a costat o avere noaptea tarziu, never again",
        "tokens": ["Uber-ul", "a", "costat", "o", "avere", "noaptea", "tarziu,", "never", "again"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    # --- fatigue ---
    {
        "sentence": "Sunt asa tired dupa shift-ul de azi",
        "tokens": ["Sunt", "asa", "tired", "dupa", "shift-ul", "de", "azi"],
        "labels": ["RO", "RO", "EN", "RO", "EN", "RO", "RO"],
    },
    {
        "sentence": "Nu am dormit bine, fully drained acum",
        "tokens": ["Nu", "am", "dormit", "bine,", "fully", "drained", "acum"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN", "RO"],
    },
    {
        "sentence": "Corpul meu e in burnout complet, nu mai pot",
        "tokens": ["Corpul", "meu", "e", "in", "burnout", "complet,", "nu", "mai", "pot"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Atat de exhausted dupa saptamana asta, need a break",
        "tokens": ["Atat", "de", "exhausted", "dupa", "saptamana", "asta,", "need", "a", "break"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Am lucrat non-stop si acum sunt completely done",
        "tokens": ["Am", "lucrat", "non-stop", "si", "acum", "sunt", "completely", "done"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Cafeaua nu mai face efect, sunt sleepy tot timpul",
        "tokens": ["Cafeaua", "nu", "mai", "face", "efect,", "sunt", "sleepy", "tot", "timpul"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "RO", "EN", "RO", "RO"],
    },
    {
        "sentence": "Imi trebuie un weekend off, seriously",
        "tokens": ["Imi", "trebuie", "un", "weekend", "off,", "seriously"],
        "labels": ["RO", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Dupa ture de noapte sunt always out of it toata ziua",
        "tokens": ["Dupa", "ture", "de", "noapte", "sunt", "always", "out", "of", "it", "toata", "ziua"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "EN", "EN", "EN", "EN", "RO", "RO"],
    },
    {
        "sentence": "Mintea mea e blank, nu pot sa mai gandesc straight",
        "tokens": ["Mintea", "mea", "e", "blank,", "nu", "pot", "sa", "mai", "gandesc", "straight"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Sunt pe verge sa plang de oboseala, too much",
        "tokens": ["Sunt", "pe", "verge", "sa", "plang", "de", "oboseala,", "too", "much"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    # --- tech ---
    {
        "sentence": "Am dat update la laptop si acum crapa tot",
        "tokens": ["Am", "dat", "update", "la", "laptop", "si", "acum", "crapa", "tot"],
        "labels": ["RO", "RO", "EN", "RO", "EN", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Wi-fi-ul din camin e un disaster, nu pot sa fac nimic online",
        "tokens": ["Wi-fi-ul", "din", "camin", "e", "un", "disaster,", "nu", "pot", "sa", "fac", "nimic", "online"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Am facut factory reset si acum trebuie sa reinstallez totul, nightmare",
        "tokens": ["Am", "facut", "factory", "reset", "si", "acum", "trebuie", "sa", "reinstallez", "totul,", "nightmare"],
        "labels": ["RO", "RO", "EN", "EN", "RO", "RO", "RO", "RO", "EN", "RO", "EN"],
    },
    {
        "sentence": "Bateria la telefon tine 3 ore maxim, seriously",
        "tokens": ["Bateria", "la", "telefon", "tine", "3", "ore", "maxim,", "seriously"],
        "labels": ["RO", "RO", "RO", "RO", "OTHER", "RO", "RO", "EN"],
    },
    {
        "sentence": "Am luat un SSD nou si diferenta de speed e unreal",
        "tokens": ["Am", "luat", "un", "SSD", "nou", "si", "diferenta", "de", "speed", "e", "unreal"],
        "labels": ["RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN", "RO", "EN"],
    },
    {
        "sentence": "Codul meu nu compileaza si nu stiu de ce, so frustrated",
        "tokens": ["Codul", "meu", "nu", "compileaza", "si", "nu", "stiu", "de", "ce,", "so", "frustrated"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am dat crash la server accidental si am intrat in panic mode",
        "tokens": ["Am", "dat", "crash", "la", "server", "accidental", "si", "am", "intrat", "in", "panic", "mode"],
        "labels": ["RO", "RO", "EN", "RO", "EN", "RO", "RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "VPN-ul nu merge azi si trebuie sa accesez ceva important",
        "tokens": ["VPN-ul", "nu", "merge", "azi", "si", "trebuie", "sa", "accesez", "ceva", "important"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am pierdut 3 ore sa debug-uiesc un bug stupid",
        "tokens": ["Am", "pierdut", "3", "ore", "sa", "debug-uiesc", "un", "bug", "stupid"],
        "labels": ["RO", "RO", "OTHER", "RO", "RO", "EN", "RO", "EN", "RO"],
    },
    {
        "sentence": "Framework-ul acesta e confusing, documentation-ul e terrible",
        "tokens": ["Framework-ul", "acesta", "e", "confusing,", "documentation-ul", "e", "terrible"],
        "labels": ["EN", "RO", "RO", "EN", "EN", "RO", "EN"],
    },
    # --- food ---
    {
        "sentence": "Hai sa mancam ceva, I'm starving",
        "tokens": ["Hai", "sa", "mancam", "ceva,", "I'm", "starving"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN"],
    },
    {
        "sentence": "Am comandat delivery si dureaza o ora, seriously",
        "tokens": ["Am", "comandat", "delivery", "si", "dureaza", "o", "ora,", "seriously"],
        "labels": ["RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Mancarea de la cantina e gross, prefer sa mananc afara",
        "tokens": ["Mancarea", "de", "la", "cantina", "e", "gross,", "prefer", "sa", "mananc", "afara"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am gatit pentru prima oara ceva decent, proud of myself",
        "tokens": ["Am", "gatit", "pentru", "prima", "oara", "ceva", "decent,", "proud", "of", "myself"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "RO", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Coffee-ul de dimineata e un must, altfel nu functionez",
        "tokens": ["Coffee-ul", "de", "dimineata", "e", "un", "must,", "altfel", "nu", "functionez"],
        "labels": ["EN", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO"],
    },
    {
        "sentence": "Am mers la un brunch super cute, food was amazing",
        "tokens": ["Am", "mers", "la", "un", "brunch", "super", "cute,", "food", "was", "amazing"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "EN", "EN", "EN", "EN", "EN"],
    },
    {
        "sentence": "Pofta mea de junk food lately e out of control",
        "tokens": ["Pofta", "mea", "de", "junk", "food", "lately", "e", "out", "of", "control"],
        "labels": ["RO", "RO", "RO", "EN", "EN", "EN", "RO", "EN", "EN", "EN"],
    },
    {
        "sentence": "Am incercat reteta aia de pe TikTok si a iesit bine, surprised",
        "tokens": ["Am", "incercat", "reteta", "aia", "de", "pe", "TikTok", "si", "a", "iesit", "bine,", "surprised"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "RO", "EN", "RO", "RO", "RO", "RO", "EN"],
    },
    {
        "sentence": "Nu mai am ingrediente acasa, need to go grocery shopping",
        "tokens": ["Nu", "mai", "am", "ingrediente", "acasa,", "need", "to", "go", "grocery", "shopping"],
        "labels": ["RO", "RO", "RO", "RO", "RO", "EN", "EN", "EN", "EN", "EN"],
    },
    {
        "sentence": "Locul ala nou de sushi e must-try, honestly best in oras",
        "tokens": ["Locul", "ala", "nou", "de", "sushi", "e", "must-try,", "honestly", "best", "in", "oras"],
        "labels": ["RO", "RO", "RO", "RO", "EN", "RO", "EN", "EN", "EN", "RO", "RO"],
    },
]


def save_corpus():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "romgleza.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sentence_id", "token", "label"])
        for idx, example in enumerate(ROMGLEZA_EXAMPLES):
            for token, label in zip(example["tokens"], example["labels"]):
                writer.writerow([idx, token, label])
    print(f"Saved {len(ROMGLEZA_EXAMPLES)} sentences to {output_path}")


save_corpus()

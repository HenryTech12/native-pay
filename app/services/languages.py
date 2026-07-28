"""
Fixed-phrase translations for the assistant's spoken confirmation/success/
error strings. Deliberately not a live-translation call — fewer moving
parts to fail on stage. Yoruba/Pidgin/Hausa/Igbo entries are reasonable
approximations, not reviewed by a native speaker — sanity-check before a
live pitch if you have access to one. Mirrors languages.ts on the frontend.
"""

_PHRASES = {
    "en": {
        "confirmSend": lambda amt, name: f"You are about to send {amt} naira to {name}. Should I continue?",
        "confirmWithdraw": lambda amt: f"You are about to withdraw {amt} naira. Should I continue?",
        "successSend": lambda amt, name: f"Your transfer of {amt} naira to {name} was successful.",
        "successWithdraw": lambda amt: f"Your withdrawal of {amt} naira was successful.",
        "balance": lambda amt: f"Your account balance is {amt} naira.",
        "askRecipient": "I heard you want to send money. Who would you like to send it to?",
        "askAmount": "How much would you like to send?",
        "notUnderstood": "Sorry, I didn't understand that. Please try again.",
        "txFailed": "Your transaction could not be completed. No money was deducted.",
        "faceFailed": "We couldn't verify your identity. Please try again.",
        "networkError": "We're having trouble connecting. Please check your connection and try again.",
    },
    "pcm": {
        "confirmSend": lambda amt, name: f"You wan send {amt} naira give {name}. I go continue?",
        "confirmWithdraw": lambda amt: f"You wan withdraw {amt} naira. I go continue?",
        "successSend": lambda amt, name: f"Your {amt} naira don successfully reach {name}.",
        "successWithdraw": lambda amt: f"Your {amt} naira withdrawal don successful.",
        "balance": lambda amt: f"Your balance na {amt} naira.",
        "askRecipient": "I hear say you wan send money. Who you wan send am give?",
        "askAmount": "How much you wan send?",
        "notUnderstood": "Sorry, I no understand. Try again abeg.",
        "txFailed": "Your transaction no complete. No money comot from your account.",
        "faceFailed": "We no fit verify say na you. Try again.",
        "networkError": "Network wahala dey. Check your connection try again.",
    },
    "yo": {
        "confirmSend": lambda amt, name: f"O fẹ́ fi ẹgbẹ̀rún {amt} ránṣẹ́ sí {name}. Ṣé kí n tẹ̀síwájú?",
        "confirmWithdraw": lambda amt: f"O fẹ́ yọ {amt} náírà kúrò. Ṣé kí n tẹ̀síwájú?",
        "successSend": lambda amt, name: f"A ti fi {amt} náírà ránṣẹ́ sí {name} ní àṣeyọrí.",
        "successWithdraw": lambda amt: f"Yíyọ {amt} náírà ṣàṣeyọrí.",
        "balance": lambda amt: f"Owó tó kù nínú àkọọ́lẹ̀ rẹ ni {amt} náírà.",
        "askRecipient": "Mo gbọ́ pé o fẹ́ fi owó ránṣẹ́. Ta ni o fẹ́ fi ránṣẹ́ sí?",
        "askAmount": "Ẹ mélòó ni o fẹ́ fi ránṣẹ́?",
        "notUnderstood": "Pẹ̀lẹ́, mi ò gbọ́ ohun tí o sọ. Jọ̀wọ́ tún sọ.",
        "txFailed": "A kò lè parí ìdúnàádúrà yìí. A kò yọ owó kankan.",
        "faceFailed": "A kò lè fi ìdánimọ̀ rẹ múlẹ̀. Jọ̀wọ́ tún gbìyànjú.",
        "networkError": "A ní ìṣòro ìsopọ̀. Jọ̀wọ́ ṣàyẹ̀wò ìsopọ̀ rẹ kí o sì tún gbìyànjú.",
    },
    "ha": {
        "confirmSend": lambda amt, name: f"Kana son aika Naira {amt} zuwa {name}. In ci gaba?",
        "confirmWithdraw": lambda amt: f"Kana son cire Naira {amt}. In ci gaba?",
        "successSend": lambda amt, name: f"An yi nasarar aika Naira {amt} zuwa {name}.",
        "successWithdraw": lambda amt: f"An yi nasarar cire Naira {amt}.",
        "balance": lambda amt: f"Ma'aunin asusunku shine Naira {amt}.",
        "askRecipient": "Na ji kana son aika kudi. Wa kake son aikawa?",
        "askAmount": "Nawa kake son aikawa?",
        "notUnderstood": "Yi hakuri, ban gane ba. Da fatan za a sake gwadawa.",
        "txFailed": "Ba a kammala ma'amalar ba. Ba a cire kudi ba.",
        "faceFailed": "Ba mu iya tabbatar da ku ba. Da fatan za a sake gwadawa.",
        "networkError": "Muna da matsalar hadi. Duba hadin ka sannan a sake gwadawa.",
    },
    "ig": {
        "confirmSend": lambda amt, name: f"Ị chọrọ izipu Naira {amt} nye {name}. Ka m gaa n'ihu?",
        "confirmWithdraw": lambda amt: f"Ị chọrọ iwepụ Naira {amt}. Ka m gaa n'ihu?",
        "successSend": lambda amt, name: f"Izipu Naira {amt} nye {name} gara nke ọma.",
        "successWithdraw": lambda amt: f"Iwepụ Naira {amt} gara nke ọma.",
        "balance": lambda amt: f"Ego fọdụrụ n'akaụntụ gị bụ Naira {amt}.",
        "askRecipient": "Anụrụ m na ị chọrọ izipu ego. Ònye ka ị chọrọ izipu ya?",
        "askAmount": "Ego ole ka ị chọrọ izipu?",
        "notUnderstood": "Ndo, aghọtaghị m. Biko nwaa ọzọ.",
        "txFailed": "Enweghị ike imecha azụmahịa a. Ewepụghị ego ọ bụla.",
        "faceFailed": "Enweghị ike ịkwado onye ị bụ. Biko nwaa ọzọ.",
        "networkError": "Anyị nwere nsogbu njikọ. Biko lelee njikọ gị ma nwaa ọzọ.",
    },
}


def t(lang: str, key: str, *args) -> str:
    dict_for_lang = _PHRASES.get(lang, _PHRASES["en"])
    entry = dict_for_lang.get(key, _PHRASES["en"].get(key))
    return entry(*args) if callable(entry) else entry


def supported_languages() -> list[dict]:
    return [
        {"code": "en", "label": "English"},
        {"code": "pcm", "label": "Nigerian Pidgin"},
        {"code": "yo", "label": "Yorùbá"},
        {"code": "ha", "label": "Hausa"},
        {"code": "ig", "label": "Igbo"},
    ]

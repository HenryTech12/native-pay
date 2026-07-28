type Phrases = {
  confirmSend: (amt: number, name: string) => string;
  confirmWithdraw: (amt: number) => string;
  successSend: (amt: number, name: string) => string;
  successWithdraw: (amt: number) => string;
  balance: (amt: number) => string;
};

const T: Record<string, Phrases> = {
  en: {
    confirmSend: (a, n) => `You are about to send ${a} naira to ${n}. Should I continue?`,
    confirmWithdraw: (a) => `You are about to withdraw ${a} naira. Should I continue?`,
    successSend: (a, n) => `Your transfer of ${a} naira to ${n} was successful.`,
    successWithdraw: (a) => `Your withdrawal of ${a} naira was successful.`,
    balance: (a) => `Your account balance is ${a} naira.`
  },
  pcm: {
    confirmSend: (a, n) => `You wan send ${a} naira give ${n}. I go continue?`,
    confirmWithdraw: (a) => `You wan withdraw ${a} naira. I go continue?`,
    successSend: (a, n) => `Your ${a} naira don successfully reach ${n}.`,
    successWithdraw: (a) => `Your ${a} naira withdrawal don successful.`,
    balance: (a) => `Your balance na ${a} naira.`
  },
  yo: {
    confirmSend: (a, n) => `O fẹ́ fi ẹgbẹ̀rún ${a} ránṣẹ́ sí ${n}. Ṣé kí n tẹ̀síwájú?`,
    confirmWithdraw: (a) => `O fẹ́ yọ ${a} náírà kúrò. Ṣé kí n tẹ̀síwájú?`,
    successSend: (a, n) => `A ti fi ${a} náírà ránṣẹ́ sí ${n} ní àṣeyọrí.`,
    successWithdraw: (a) => `Yíyọ ${a} náírà ṣàṣeyọrí.`,
    balance: (a) => `Owó tó kù nínú àkọọ́lẹ̀ rẹ ni ${a} náírà.`
  },
  ha: {
    confirmSend: (a, n) => `Kana son aika Naira ${a} zuwa ${n}. In ci gaba?`,
    confirmWithdraw: (a) => `Kana son cire Naira ${a}. In ci gaba?`,
    successSend: (a, n) => `An yi nasarar aika Naira ${a} zuwa ${n}.`,
    successWithdraw: (a) => `An yi nasarar cire Naira ${a}.`,
    balance: (a) => `Ma'aunin asusunku shine Naira ${a}.`
  },
  ig: {
    confirmSend: (a, n) => `Ị chọrọ izipu Naira ${a} nye ${n}. Ka m gaa n'ihu?`,
    confirmWithdraw: (a) => `Ị chọrọ iwepụ Naira ${a}. Ka m gaa n'ihu?`,
    successSend: (a, n) => `Izipu Naira ${a} nye ${n} gara nke ọma.`,
    successWithdraw: (a) => `Iwepụ Naira ${a} gara nke ọma.`,
    balance: (a) => `Ego fọdụrụ n'akaụntụ gị bụ Naira ${a}.`
  }
};

export function phrase<K extends keyof Phrases>(lang: string, key: K, ...args: Parameters<Phrases[K]>): string {
  const dict = T[lang] || T.en;
  const fn = dict[key] || T.en[key];
  return (fn as (...a: any[]) => string)(...args);
}

export function speak(text: string) {
  if (!window.speechSynthesis) return;
  const u = new SpeechSynthesisUtterance(text);
  u.rate = 0.95;
  window.speechSynthesis.speak(u);
}

export const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "pcm", label: "Pidgin" },
  { code: "yo", label: "Yorùbá" },
  { code: "ha", label: "Hausa" },
  { code: "ig", label: "Igbo" }
];

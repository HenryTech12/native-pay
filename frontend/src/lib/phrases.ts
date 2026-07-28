type Phrases = {
  confirmSend: (amt: number, name: string) => string;
  confirmWithdraw: (amt: number) => string;
  successSend: (amt: number, name: string) => string;
  successWithdraw: (amt: number) => string;
  balance: (amt: number) => string;
  askFullName: () => string;
  askAddress: () => string;
  askRepeatDigits: (spoken: string) => string;
  welcomeBack: (name: string) => string;
  voiceAuthStepUp: () => string;
  voiceAuthFailed: () => string;
  enrollmentComplete: () => string;
};

const T: Record<string, Phrases> = {
  en: {
    confirmSend: (a, n) => `You are about to send ${a} naira to ${n}. Should I continue?`,
    confirmWithdraw: (a) => `You are about to withdraw ${a} naira. Should I continue?`,
    successSend: (a, n) => `Your transfer of ${a} naira to ${n} was successful.`,
    successWithdraw: (a) => `Your withdrawal of ${a} naira was successful.`,
    balance: (a) => `Your account balance is ${a} naira.`,
    askFullName: () => "Please say your full name, clearly.",
    askAddress: () => "Now please say your home address.",
    askRepeatDigits: (s) => `Please repeat these numbers after me: ${s}.`,
    welcomeBack: (n) => `Welcome back, ${n}.`,
    voiceAuthStepUp: () => "I'm not fully sure that's you. Let's do a quick face check.",
    voiceAuthFailed: () => "I couldn't verify your identity. Please speak with the agent.",
    enrollmentComplete: () => "You're all set. You can now use NativePay with your voice."
  },
  pcm: {
    confirmSend: (a, n) => `You wan send ${a} naira give ${n}. I go continue?`,
    confirmWithdraw: (a) => `You wan withdraw ${a} naira. I go continue?`,
    successSend: (a, n) => `Your ${a} naira don successfully reach ${n}.`,
    successWithdraw: (a) => `Your ${a} naira withdrawal don successful.`,
    balance: (a) => `Your balance na ${a} naira.`,
    askFullName: () => "Abeg call your full name well well.",
    askAddress: () => "Now abeg tell me your house address.",
    askRepeatDigits: (s) => `Abeg repeat these numbers after me: ${s}.`,
    welcomeBack: (n) => `Welcome back, ${n}.`,
    voiceAuthStepUp: () => "I no too sure say na you. Make we quick check your face.",
    voiceAuthFailed: () => "I no fit confam say na you by voice. Abeg talk to the agent.",
    enrollmentComplete: () => "You don set. You fit dey use NativePay with your voice now."
  },
  yo: {
    confirmSend: (a, n) => `O fẹ́ fi ẹgbẹ̀rún ${a} ránṣẹ́ sí ${n}. Ṣé kí n tẹ̀síwájú?`,
    confirmWithdraw: (a) => `O fẹ́ yọ ${a} náírà kúrò. Ṣé kí n tẹ̀síwájú?`,
    successSend: (a, n) => `A ti fi ${a} náírà ránṣẹ́ sí ${n} ní àṣeyọrí.`,
    successWithdraw: (a) => `Yíyọ ${a} náírà ṣàṣeyọrí.`,
    balance: (a) => `Owó tó kù nínú àkọọ́lẹ̀ rẹ ni ${a} náírà.`,
    askFullName: () => "Jọ̀wọ́ sọ orúkọ rẹ ní kíkún.",
    askAddress: () => "Nísisìyí, jọ̀wọ́ sọ àdírẹ́sì ilé rẹ.",
    askRepeatDigits: (s) => `Jọ̀wọ́ tún àwọn nọ́mbà wọ̀nyí sọ lẹ́yìn mi: ${s}.`,
    welcomeBack: (n) => `Kú àbọ̀, ${n}.`,
    voiceAuthStepUp: () => "Èmi kò dá mi lójú pé ìwọ ni. Ẹ jẹ́ kí a ṣàyẹ̀wò ojú rẹ ní kíákíá.",
    voiceAuthFailed: () => "N kò lè fi ohùn rẹ jẹ́rìí sí ẹni tí ìwọ jẹ́. Jọ̀wọ́ bá aṣojú sọ̀rọ̀.",
    enrollmentComplete: () => "O ti ṣetán. O lè bẹ̀rẹ̀ sí lo NativePay pẹ̀lú ohùn rẹ."
  },
  ha: {
    confirmSend: (a, n) => `Kana son aika Naira ${a} zuwa ${n}. In ci gaba?`,
    confirmWithdraw: (a) => `Kana son cire Naira ${a}. In ci gaba?`,
    successSend: (a, n) => `An yi nasarar aika Naira ${a} zuwa ${n}.`,
    successWithdraw: (a) => `An yi nasarar cire Naira ${a}.`,
    balance: (a) => `Ma'aunin asusunku shine Naira ${a}.`,
    askFullName: () => "Don Allah faɗi cikakken sunanka a fili.",
    askAddress: () => "Yanzu don Allah faɗi adireshin gidanka.",
    askRepeatDigits: (s) => `Don Allah maimaita waɗannan lambobi bayan ni: ${s}.`,
    welcomeBack: (n) => `Barka da dawowa, ${n}.`,
    voiceAuthStepUp: () => "Ban tabbata sarai ba cewa kai ne. Bari mu yi saurin duba fuska.",
    voiceAuthFailed: () => "Ban iya tabbatar da ainihinka ta murya ba. Don Allah ka tuntuɓi wakili.",
    enrollmentComplete: () => "An gama. Yanzu kana iya amfani da NativePay ta murya."
  },
  ig: {
    confirmSend: (a, n) => `Ị chọrọ izipu Naira ${a} nye ${n}. Ka m gaa n'ihu?`,
    confirmWithdraw: (a) => `Ị chọrọ iwepụ Naira ${a}. Ka m gaa n'ihu?`,
    successSend: (a, n) => `Izipu Naira ${a} nye ${n} gara nke ọma.`,
    successWithdraw: (a) => `Iwepụ Naira ${a} gara nke ọma.`,
    balance: (a) => `Ego fọdụrụ n'akaụntụ gị bụ Naira ${a}.`,
    askFullName: () => "Biko kwuo aha gị zuru ezu nke ọma.",
    askAddress: () => "Ugbu a, biko kwuo adreesị ụlọ gị.",
    askRepeatDigits: (s) => `Biko kwughachi ọnụọgụgụ ndị a m kwuru: ${s}.`,
    welcomeBack: (n) => `Nnọọ, ${n}.`,
    voiceAuthStepUp: () => "Ejighị m n'aka na ọ bụ gị. Ka anyị mee nyocha ihu ngwa ngwa.",
    voiceAuthFailed: () => "Enweghị m ike iji olu gị kwado onye ị bụ. Biko gwa onye nnọchite anya.",
    enrollmentComplete: () => "Emechaala. Ị nwere ike iji olu gị bido iji NativePay ugbu a."
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

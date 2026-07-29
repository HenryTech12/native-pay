import { synthesizeSpeech } from "./api";

type Phrases = {
  confirmSend: (amt: number, name: string) => string;
  confirmWithdraw: (amt: number) => string;
  confirmDeposit: (amt: number) => string;
  confirmAirtime: (amt: number, phone: string) => string;
  successSend: (amt: number, name: string) => string;
  successWithdraw: (amt: number) => string;
  successDeposit: (amt: number) => string;
  successAirtime: (amt: number, phone: string) => string;
  balance: (amt: number) => string;
  askFullName: () => string;
  askAddress: () => string;
  askRepeatDigits: (spoken: string) => string;
  askPhoneNumber: () => string;
  welcomeBack: (name: string) => string;
  voiceAuthStepUp: () => string;
  voiceAuthFailed: () => string;
  voiceVerifiedSkipFace: () => string;
  enrollmentComplete: () => string;
};

const T: Record<string, Phrases> = {
  en: {
    confirmSend: (a, n) => `You are about to send ${a} naira to ${n}. Should I continue?`,
    confirmWithdraw: (a) => `You are about to withdraw ${a} naira. Should I continue?`,
    confirmDeposit: (a) => `You are about to deposit ${a} naira. Should I continue?`,
    confirmAirtime: (a, p) => `You are about to buy ${a} naira airtime for ${p}. Should I continue?`,
    successSend: (a, n) => `Your transfer of ${a} naira to ${n} was successful.`,
    successWithdraw: (a) => `Your withdrawal of ${a} naira was successful.`,
    successDeposit: (a) => `Your deposit of ${a} naira was successful.`,
    successAirtime: (a, p) => `Your airtime purchase of ${a} naira for ${p} was successful.`,
    balance: (a) => `Your account balance is ${a} naira.`,
    askFullName: () => "Please say your full name, clearly.",
    askAddress: () => "Now please say your home address.",
    askRepeatDigits: (s) => `Please repeat these numbers after me: ${s}.`,
    askPhoneNumber: () => "What phone number should I top up?",
    welcomeBack: (n) => `Welcome back, ${n}.`,
    voiceAuthStepUp: () => "I'm not fully sure that's you. Let's do a quick face check.",
    voiceAuthFailed: () => "I couldn't verify your identity. Please speak with the agent.",
    voiceVerifiedSkipFace: () => "Your voice confirms it's you — no face check needed this time.",
    enrollmentComplete: () => "You're all set. You can now use NativePay with your voice."
  },
  pcm: {
    confirmSend: (a, n) => `You wan send ${a} naira give ${n}. I go continue?`,
    confirmWithdraw: (a) => `You wan withdraw ${a} naira. I go continue?`,
    confirmDeposit: (a) => `You wan deposit ${a} naira. I go continue?`,
    confirmAirtime: (a, p) => `You wan buy ${a} naira airtime for ${p}. I go continue?`,
    successSend: (a, n) => `Your ${a} naira don successfully reach ${n}.`,
    successWithdraw: (a) => `Your ${a} naira withdrawal don successful.`,
    successDeposit: (a) => `Your ${a} naira deposit don successful.`,
    successAirtime: (a, p) => `Your ${a} naira airtime for ${p} don successful.`,
    balance: (a) => `Your balance na ${a} naira.`,
    askFullName: () => "Abeg call your full name well well.",
    askAddress: () => "Now abeg tell me your house address.",
    askRepeatDigits: (s) => `Abeg repeat these numbers after me: ${s}.`,
    askPhoneNumber: () => "Wetin be the phone number wey you wan top up?",
    welcomeBack: (n) => `Welcome back, ${n}.`,
    voiceAuthStepUp: () => "I no too sure say na you. Make we quick check your face.",
    voiceAuthFailed: () => "I no fit confam say na you by voice. Abeg talk to the agent.",
    voiceVerifiedSkipFace: () => "Your voice don confam say na you — no need to check face this time.",
    enrollmentComplete: () => "You don set. You fit dey use NativePay with your voice now."
  },
  yo: {
    confirmSend: (a, n) => `O fẹ́ fi ${a} náírà ránṣẹ́ sí ${n}. Ṣé kí n tẹ̀síwájú?`,
    confirmWithdraw: (a) => `O fẹ́ yọ ${a} náírà kúrò. Ṣé kí n tẹ̀síwájú?`,
    confirmDeposit: (a) => `O fẹ́ fi ${a} náírà sí àkọọ́lẹ̀ rẹ. Ṣé kí n tẹ̀síwájú?`,
    confirmAirtime: (a, p) => `O fẹ́ ra ẹ̀rọ-ìjíròrò ${a} náírà fún ${p}. Ṣé kí n tẹ̀síwájú?`,
    successSend: (a, n) => `A ti fi ${a} náírà ránṣẹ́ sí ${n} ní àṣeyọrí.`,
    successWithdraw: (a) => `Yíyọ ${a} náírà ṣàṣeyọrí.`,
    successDeposit: (a) => `Fífi ${a} náírà sí àkọọ́lẹ̀ rẹ ṣàṣeyọrí.`,
    successAirtime: (a, p) => `Rírà ẹ̀rọ-ìjíròrò ${a} náírà fún ${p} ṣàṣeyọrí.`,
    balance: (a) => `Owó tó kù nínú àkọọ́lẹ̀ rẹ ni ${a} náírà.`,
    askFullName: () => "Jọ̀wọ́ sọ orúkọ rẹ ní kíkún.",
    askAddress: () => "Nísisìyí, jọ̀wọ́ sọ àdírẹ́sì ilé rẹ.",
    askRepeatDigits: (s) => `Jọ̀wọ́ tún àwọn nọ́mbà wọ̀nyí sọ lẹ́yìn mi: ${s}.`,
    askPhoneNumber: () => "Nọ́mbà fóònù wo ni kí n gbé kirẹ́ìjì sí?",
    welcomeBack: (n) => `Kú àbọ̀, ${n}.`,
    voiceAuthStepUp: () => "Èmi kò dá mi lójú pé ìwọ ni. Ẹ jẹ́ kí a ṣàyẹ̀wò ojú rẹ ní kíákíá.",
    voiceAuthFailed: () => "N kò lè fi ohùn rẹ jẹ́rìí sí ẹni tí ìwọ jẹ́. Jọ̀wọ́ bá aṣojú sọ̀rọ̀.",
    voiceVerifiedSkipFace: () => "Ohùn rẹ ti jẹ́rìí pé ìwọ ni — a kò nílò ṣàyẹ̀wò ojú ní àkókò yìí.",
    enrollmentComplete: () => "O ti ṣetán. O lè bẹ̀rẹ̀ sí lo NativePay pẹ̀lú ohùn rẹ."
  },
  ha: {
    confirmSend: (a, n) => `Kana son aika Naira ${a} zuwa ${n}. In ci gaba?`,
    confirmWithdraw: (a) => `Kana son cire Naira ${a}. In ci gaba?`,
    confirmDeposit: (a) => `Kana son ajiya Naira ${a}. In ci gaba?`,
    confirmAirtime: (a, p) => `Kana son sayan katin waya na Naira ${a} don ${p}. In ci gaba?`,
    successSend: (a, n) => `An yi nasarar aika Naira ${a} zuwa ${n}.`,
    successWithdraw: (a) => `An yi nasarar cire Naira ${a}.`,
    successDeposit: (a) => `An yi nasarar ajiya Naira ${a}.`,
    successAirtime: (a, p) => `An yi nasarar sayan katin waya na Naira ${a} don ${p}.`,
    balance: (a) => `Ma'aunin asusunku shine Naira ${a}.`,
    askFullName: () => "Don Allah faɗi cikakken sunanka a fili.",
    askAddress: () => "Yanzu don Allah faɗi adireshin gidanka.",
    askRepeatDigits: (s) => `Don Allah maimaita waɗannan lambobi bayan ni: ${s}.`,
    askPhoneNumber: () => "Wane lambar waya ne za a caji?",
    welcomeBack: (n) => `Barka da dawowa, ${n}.`,
    voiceAuthStepUp: () => "Ban tabbata sarai ba cewa kai ne. Bari mu yi saurin duba fuska.",
    voiceAuthFailed: () => "Ban iya tabbatar da ainihinka ta murya ba. Don Allah ka tuntuɓi wakili.",
    voiceVerifiedSkipFace: () => "Muryarka ta tabbatar da cewa kai ne — ba a bukatar duba fuska a wannan lokacin.",
    enrollmentComplete: () => "An gama. Yanzu kana iya amfani da NativePay ta murya."
  },
  ig: {
    confirmSend: (a, n) => `Ị chọrọ izipu Naira ${a} nye ${n}. Ka m gaa n'ihu?`,
    confirmWithdraw: (a) => `Ị chọrọ iwepụ Naira ${a}. Ka m gaa n'ihu?`,
    confirmDeposit: (a) => `Ị chọrọ itinye Naira ${a} n'akaụntụ gị. Ka m gaa n'ihu?`,
    confirmAirtime: (a, p) => `Ị chọrọ ịzụ ekwentị Naira ${a} maka ${p}. Ka m gaa n'ihu?`,
    successSend: (a, n) => `Izipu Naira ${a} nye ${n} gara nke ọma.`,
    successWithdraw: (a) => `Iwepụ Naira ${a} gara nke ọma.`,
    successDeposit: (a) => `Itinye Naira ${a} n'akaụntụ gị gara nke ọma.`,
    successAirtime: (a, p) => `Ịzụ ekwentị Naira ${a} maka ${p} gara nke ọma.`,
    balance: (a) => `Ego fọdụrụ n'akaụntụ gị bụ Naira ${a}.`,
    askFullName: () => "Biko kwuo aha gị zuru ezu nke ọma.",
    askAddress: () => "Ugbu a, biko kwuo adreesị ụlọ gị.",
    askRepeatDigits: (s) => `Biko kwughachi ọnụọgụgụ ndị a m kwuru: ${s}.`,
    askPhoneNumber: () => "Kedu nọmba ekwentị ka m ga-eji chaajị?",
    welcomeBack: (n) => `Nnọọ, ${n}.`,
    voiceAuthStepUp: () => "Ejighị m n'aka na ọ bụ gị. Ka anyị mee nyocha ihu ngwa ngwa.",
    voiceAuthFailed: () => "Enweghị m ike iji olu gị kwado onye ị bụ. Biko gwa onye nnọchite anya.",
    voiceVerifiedSkipFace: () => "Olu gị akwadola na ọ bụ gị — anaghị achọ nyocha ihu oge a.",
    enrollmentComplete: () => "Emechaala. Ị nwere ike iji olu gị bido iji NativePay ugbu a."
  }
};

export function phrase<K extends keyof Phrases>(lang: string, key: K, ...args: Parameters<Phrases[K]>): string {
  const dict = T[lang] || T.en;
  const fn = dict[key] || T.en[key];
  return (fn as (...a: any[]) => string)(...args);
}

type SpeakingListener = (speaking: boolean) => void;
const speakingListeners = new Set<SpeakingListener>();
let isSpeakingNow = false;

function setSpeaking(value: boolean) {
  isSpeakingNow = value;
  speakingListeners.forEach((l) => l(value));
}

/** Subscribe to know whenever speak() is actively playing audio — used
 * to show a "speaking" indicator so users aren't left guessing whether
 * to wait or act while the voice prompt is still in flight. */
export function subscribeSpeaking(listener: SpeakingListener): () => void {
  speakingListeners.add(listener);
  listener(isSpeakingNow);
  return () => { speakingListeners.delete(listener); };
}

function speakWithBrowserVoice(text: string): Promise<void> {
  return new Promise((resolve) => {
    if (!window.speechSynthesis) { resolve(); return; }
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 0.95;
    u.onend = () => resolve();
    u.onerror = () => resolve();
    window.speechSynthesis.speak(u);
  });
}

/**
 * Nigerian-accented read-back via YarnGPT (see backend/app/services/
 * yarngpt_service.py), falling back to the browser's generic
 * speechSynthesis if the API key isn't configured or the call fails.
 * Resolves only once the audio has actually finished playing — callers
 * rely on `await speak(...)` to know the message was fully heard before
 * moving the UI on to the next step, not just that playback started.
 */
export async function speak(text: string, lang: string = "en") {
  setSpeaking(true);
  try {
    const blob = await synthesizeSpeech(text, lang);
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    let playbackBlocked = false;
    await new Promise<void>((resolve) => {
      audio.onended = () => { URL.revokeObjectURL(url); resolve(); };
      audio.onerror = () => { URL.revokeObjectURL(url); resolve(); };
      audio.play().catch(() => { playbackBlocked = true; URL.revokeObjectURL(url); resolve(); });
    });
    // audio.play() can be silently blocked by the browser's autoplay
    // policy (common on mobile when too much time passes between the
    // triggering tap and playback starting, e.g. the TTS fetch itself) —
    // fall back to speechSynthesis instead of playing nothing at all.
    if (playbackBlocked) {
      await speakWithBrowserVoice(text);
    }
  } catch {
    await speakWithBrowserVoice(text);
  } finally {
    setSpeaking(false);
  }
}

export const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "pcm", label: "Pidgin" },
  { code: "yo", label: "Yorùbá" },
  { code: "ha", label: "Hausa" },
  { code: "ig", label: "Igbo" }
];

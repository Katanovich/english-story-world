// Browser speech synthesis is used ONLY as a clearly-labelled fallback when a lesson has no
// recorded audio yet. Note: some browsers use an online voice service for synthesis; the
// text spoken is lesson content only, never personal data.

export function canSpeak(): boolean {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

export function speak(text: string, rate = 0.85): void {
  if (!canSpeak()) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "en-GB";
  u.rate = rate;
  window.speechSynthesis.speak(u);
}

export function stopSpeaking(): void {
  if (canSpeak()) window.speechSynthesis.cancel();
}

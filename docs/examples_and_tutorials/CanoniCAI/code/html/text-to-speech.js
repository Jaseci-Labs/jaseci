// Initialize new SpeechSynthesisUtterance object
let speech = new SpeechSynthesisUtterance();

// Set Speech Language
speech.lang = "en";
speech.rate = 1
speech.pitch = 1
speech.volume = 1

let voices = []; // global array of available voices

window.speechSynthesis.onvoiceschanged = (event) => {
  // Get List of Voices
  voices = window.speechSynthesis.getVoices();

  // Initially set the First Voice in the Array.
  speech.voice = voices[0];

  // Set the Voice Select List. (Set the Index as the value, which we'll use later when the user updates the Voice using the Select Menu.)
  let voiceSelect = document.querySelector("#voices");
  voices.forEach((voice, i) => (voiceSelect.options[i] = new Option(voice.name, i)));

  // event.target.onspeechstart = () => {
  //   document.querySelector('.speak-icon img').style.display = 'display'
  // };

  // event.target.onspeechend = () => {
  //   document.querySelector('.speak-icon img').style.display = 'none'
  // };
};

speech.onstart = () => {
  document.querySelector('.speak-icon img').style.display = 'flex'
}

speech.onend = () => {
  document.querySelector('.speak-icon img').style.display = 'none'
}



// document.querySelector("#rate").addEventListener("input", () => {
//   // Get rate Value from the input
//   const rate = document.querySelector("#rate").value;

//   // Set rate property of the SpeechSynthesisUtterance instance
//   speech.rate = rate;

//   // Update the rate label
//   document.querySelector("#rate-label").innerHTML = rate;
// });

// document.querySelector("#volume").addEventListener("input", () => {
//   // Get volume Value from the input
//   const volume = document.querySelector("#volume").value;

//   // Set volume property of the SpeechSynthesisUtterance instance
//   speech.volume = volume;

//   // Update the volume label
//   document.querySelector("#volume-label").innerHTML = volume;
// });

// document.querySelector("#pitch").addEventListener("input", () => {
//   // Get pitch Value from the input
//   const pitch = document.querySelector("#pitch").value;

//   // Set pitch property of the SpeechSynthesisUtterance instance
//   speech.pitch = pitch;

//   // Update the pitch label
//   document.querySelector("#pitch-label").innerHTML = pitch;
// });

document.querySelector("#voices").addEventListener("change", () => {
  // On Voice change, use the value of the select menu (which is the index of the voice in the global voice array)
  speech.voice = voices[document.querySelector("#voices").value];
});

// document.querySelector("#start").addEventListener("click", () => {
//   // Set the text property with the value of the textarea
//   speech.text = document.querySelector("textarea").value;

//   // Start Speaking
//   window.speechSynthesis.speak(speech);
// });

// document.querySelector("#pause").addEventListener("click", () => {
//   // Pause the speechSynthesis instance
//   window.speechSynthesis.pause();
// });

// document.querySelector("#resume").addEventListener("click", () => {
//   // Resume the paused speechSynthesis instance
//   window.speechSynthesis.resume();
// });

// document.querySelector("#cancel").addEventListener("click", () => {
//   // Cancel the speechSynthesis instance
//   window.speechSynthesis.cancel();
// });
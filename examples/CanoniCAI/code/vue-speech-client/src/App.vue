<template>
  <div>
    <div class="central" id="logo">
      <img src="jaseci.png" width="40"/>
    </div>
    <div class="central" id="title">
      <h1>Jaseci Speech Client</h1>
    </div>
    <div class="central">
      <label for="voices">Select a voice:</label>
    </div>
    <div class="central">
      <select v-model="selectedVoice" id="voices" @change="setVoice">
        <option v-for="voice in voices" :key="voice.name" :value="voice.name">
          {{ voice.name }}
        </option>
      </select>
    </div>
    <div class="central" id="recognition">
      <svg-icon
        id="mic"
        @click=startRecognition()
        type="mdi"
        :class=micClass
        :path="path"
        :size="192">
      </svg-icon>
    </div>
    <div class="transcript-container">
      <div class="transcript chat">
        {{ final_transcript }}
      </div>
    </div>
    <div class="response-container">
      <div class="response chat">
        {{ response }}
      </div>
    </div>
  </div>
</template>


<script>
  import SvgIcon from '@jamescoyle/vue-icon'
  import { mdiMicrophone } from '@mdi/js'
  export default {
    components: {
      SvgIcon
    },
    data() {
      return {
        selectedVoice: '',
        voices: [],
        request: '',
        path: mdiMicrophone,
        recognition: null,
        recognising: false,
        interim_transcript: '',
        final_transcript: '',
        response: '',
      }
    },
    created() {
      window.speechSynthesis.onvoiceschanged = () => {
        this.voices = window.speechSynthesis.getVoices()
      }
    },
    mounted() {
      this.recognition = new webkitSpeechRecognition()
      this.recognition.onresult = e => {
        for (var i = e.resultIndex; i < e.results.length; ++i) {
          if (e.results[i].isFinal) {
            this.final_transcript += e.results[i][0].transcript;
          } else {
            this.interim_transcript += e.results[i][0].transcript;
          }
        }
        if (this.final_transcript !== '' && this.interim_transcript === '') {
          this.recognition.stop()
          this.recognising = false 
          this.talk(this.final_transcript)
        }
      }
    },
    methods: {
      setVoice() {
        const phrase = "Welcome. My name is " + this.selectedVoice + " and this is what I sound like"
        this.speak(phrase)
      },
      startRecognition() { 
        if (!this.recognising) {
          this.final_transcript = ''
          this.response = ''
          this.recognising = true
          this.recognition.start()
        }
      },
      async talk(input) {
        const answer = await this.jacTalk(input)
        let text = await answer.replace(/https?.*?(?= |$)/g, "");
        this.response = text
        this.speak(text)
      },
      speak(phrase) {
        let speech = new SpeechSynthesisUtterance()
        let selectedVoice = this.selectedVoice
        speech.voice = this.voices.filter(function(voice) { return voice.name == selectedVoice; })[0]
        speech.text = phrase
        window.speechSynthesis.speak(speech);
      }
    },
    computed: {
      micClass() {
        if (this.recognising) return 'live'
      },
    }
  }
</script>
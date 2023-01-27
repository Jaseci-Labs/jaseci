import Artyom from 'artyom.js/build/artyom.js';

export const textToSpeech = (message: string) => {
  const artyom = new Artyom();

  artyom.say(message);
};

export const speechToText = ({ onEnd, onResult, onStart }: { onResult: (text: string) => void; onStart?: () => void; onEnd?: () => void }) => {
  const artyom = new Artyom();

  var UserDictation = artyom.newDictation({
    continuous: true, // Enable continuous if HTTPS connection
    onResult: function (text, final) {
      onResult(final);
      // Do something with the text
      console.log(text);
    },
    onStart: function () {
      onStart && onStart();
      console.log('Dictation started by the user');
    },
    onEnd: function () {
      console.log('Dictation stopped by the user');
      onEnd && onEnd();
    },
  });

  return {
    start: () => UserDictation.start(),
    stop: () => {
      artyom.fatality();
      UserDictation.stop();
    },
  };
};

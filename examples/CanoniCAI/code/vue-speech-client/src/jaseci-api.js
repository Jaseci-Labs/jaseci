// NOTE: Change this URL to your Jaseci server URL:
const apiUrl = 'http://localhost:8000'
// NOTE: Change the token to your authenticated token:
const apiToken = '9427c0ef2ba6a09c5953c9b092f594d5f8b9569eac2174451aba9fed14fb3cd6'

export default {
  methods: {
    async jacTalk(request) {
      let data = {
        ctx: { "question": request },
        name: "talk"
      }
      let result = await fetch(apiUrl + '/js/walker_run', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + apiToken
      },
      body: JSON.stringify(data),
    })
    result = await result.json();

    const answer = result.report[0];
      
    return answer
    },
  }
}


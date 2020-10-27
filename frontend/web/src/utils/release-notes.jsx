import releaseNotes from './release-notes.md';
import React, { Component, useState } from "react";
import ReactMarkdown from 'react-markdown';


class RNotes extends Component {
    state = { release_text: null }

    componentWillMount() {
      fetch(releaseNotes).then((response) => response.text()).then((text) => {
        this.setState({ release_text: text.split("-----")[0] })
      })
    }
    
    render() {
      return <div className="content">
      <ReactMarkdown source={this.state.release_text} />
    </div>
    }
  }
  
export default RNotes
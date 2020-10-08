import React, { Component } from "react";
import { Input, saveDelayTimeout, is_today } from "../utils/utils";
import { connect } from "react-redux";
import { Container } from "react-bootstrap";
import { workette_actions as wact } from "../store/workette";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.bubble.css";
import "react-quill/dist/quill.snow.css";

class WktNoteForm extends Component {
  state = { timeout: null, note: "", last_written: null };

  modules = {
    toolbar: [
      [{ header: "1" }, { header: "2" }, { font: [] }],
      [{ size: [] }],
      ["bold", "italic", "underline", "strike", "blockquote"],
      [
        { list: "ordered" },
        { list: "bullet" },
        { indent: "-1" },
        { indent: "+1" },
      ],
      ["link", "image", "video"],
      ["clean"],
    ],
    clipboard: {
      // toggle to add extra line breaks when pasting HTML:
      matchVisual: false,
    },
  };

  formats = [
    "header",
    "font",
    "size",
    "bold",
    "italic",
    "underline",
    "strike",
    "blockquote",
    "list",
    "bullet",
    "indent",
    "link",
    "video",
  ];

  updateStateLinked = () => {
    const { items } = this.props.workette;
    const current = this.props.w_id;
    const { note, last_written } = items[current].context;
    this.setState({
      note: note ? note : "",
      last_written: last_written ? last_written : null,
    });
  };
  componentDidMount() {
    this.updateStateLinked();
  }

  componentDidUpdate() {
    const { items } = this.props.workette;
    const current = this.props.w_id;
    const { last_written } = items[current].context;
    if (last_written && last_written > this.state.last_written)
      this.updateStateLinked();
  }

  handleSubmit = (e = false) => {
    if (e) e.preventDefault();
    const { note } = this.state;
    const current = this.props.w_id;
    if (!is_today(this.props.session.cur_date)) return;
    //Call Server
    this.props.set_workette(current, { note });
    setTimeout(() => this.setState({ ...this.state, saved: false }), 1000);
  };

  handleChange = (value, delta, source) => {
    if (source === "user")
      this.setState({
        note: value,
        timeout: saveDelayTimeout(this.state.timeout, () =>
          this.handleSubmit()
        ),
      });
  };

  handleLinkChange = (e) => {
    if (e.currentTarget.name === "note") {
      this.setState({
        note: e.currentTarget.value,
        timeout: saveDelayTimeout(this.state.timeout, () =>
          this.handleSubmit(e)
        ),
      });
    }
  };

  validate = () => {};

  render() {
    const { note } = this.state;
    const { items } = this.props.workette;
    const current = this.props.w_id;

    const is_link =
      items[current].context.wtype && items[current].context.wtype === "link";

    return (
      <Container fluid>
        <form onSubmit={this.handleSubmit}>
          {is_link && (
            <Input
              value={note}
              onChange={this.handleLinkChange}
              extra_class="form-control-sm"
              name="note"
              description="Link URL"
            />
          )}
          {!is_link && (
            <div>
              <br />
              <Container
                fluid
                className="border rounded m-0 p-0"
                style={{ backgroundColor: "white" }}
              >
                <ReactQuill
                  value={note}
                  onChange={this.handleChange}
                  //modules={this.modules}
                  formats={this.formats}
                  theme="bubble"
                  placeholder={"Write something..."}
                />
              </Container>
            </div>
          )}
        </form>
      </Container>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  workette: state.workette,
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  set_workette: (w_id, ctx) => dispatch(wact.set_workette(w_id, ctx)),
});

export default connect(map_state, map_dispatch)(WktNoteForm);

import React, { Component } from "react";
import Workette from "./workette";
import { connect } from "react-redux";
import WktNoteForm from "./wkt-note";
import { Container, Row, Col } from "react-bootstrap";
import { workette_actions as wact } from "../store/workette";
import ReleaseModal from "../utils/release-modal";

function print_date(d) {
  let ret = new Date(d);
  return ret.toDateString();
}

class Day extends Component {
  componentDidMount() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];
    //this.props.load_mits(current);
  }

  render() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];
    return (
      <Container fluid className="">
        <h6>
          <center>
            <br />
            {workette.items[current].context.day &&
              print_date(workette.items[current].context.day)}
          </center>
          <br />
        </h6>
        <Workette w_id={current} />
        <ReleaseModal />
      </Container>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
  api: state.api,
});

const map_dispatch = (dispatch) => ({
  load_mits: (w_id) => dispatch(wact.load_mits(w_id)),
});

export default connect(map_state, map_dispatch)(Day);

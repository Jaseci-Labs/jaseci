import React, { Component } from "react";
import Workette from "./workette";
import { connect } from "react-redux";
import { Container, } from "react-bootstrap";
import { workette_actions as wact } from "../store/workette";
import ReleaseModal from "../utils/release-modal";

function print_date(d) {
  let ret = new Date(d);
  return ret.toDateString();
}

class Day extends Component {
  componentDidMount() {
    const { session, workette } = this.props;
    const { cur_date } = session;
    const current = workette.days[cur_date];
    if (!workette.life[cur_date]) {
      this.props.get_life(cur_date);
    }
    if (!workette.years[cur_date]) {
      this.props.get_year(cur_date);
    }
    if (!workette.months[cur_date]) {
      this.props.get_month(cur_date);
    }
    if (!workette.weeks[cur_date]) {
      this.props.get_week(cur_date);
    }
  }

  render() {
    const { session, workette } = this.props;
    const { cur_date } = session;
    const current = workette.days[cur_date];
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
});

const map_dispatch = (dispatch) => ({
  get_life: (date) => dispatch(wact.get_life(date)),
  get_year: (date) => dispatch(wact.get_year(date)),
  get_month: (date) => dispatch(wact.get_month(date)),
  get_week: (date) => dispatch(wact.get_week(date)),
});

export default connect(map_state, map_dispatch)(Day);

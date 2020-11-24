import React, { Component } from "react";
import Workette from "./workette";
import { connect } from "react-redux";
import WktNoteForm from "./wkt-note";
import { Container, Row, Col, Tabs, Tab } from "react-bootstrap";
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
        <Tabs defaultActiveKey="day">
          <Tab eventKey="day" title="This Day">
            This <strong>day</strong> I will grind out
            <Workette w_id={current} />
          </Tab>
          <Tab eventKey="week" title="This Week">
            Things I must accomplish this <strong>week</strong> are
            {workette.weeks[cur_date] && (
              <Workette w_id={workette.weeks[cur_date]} />
            )}
          </Tab>
          <Tab eventKey="month" title="This Month">
            This <strong>month</strong> my key goals are
            {workette.months[cur_date] && (
              <Workette w_id={workette.months[cur_date]} />
            )}
          </Tab>
          <Tab eventKey="year" title="This Year">
            By the end of this <strong>year</strong> I want
            {workette.years[cur_date] && (
              <Workette w_id={workette.years[cur_date]} />
            )}
          </Tab>
          <Tab eventKey="life" title="In my Life">
            <strong>Life's</strong> Mission/Purpose Statement
            {workette.life[cur_date] && (
              <Workette w_id={workette.life[cur_date]} />
            )}
          </Tab>
        </Tabs>
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

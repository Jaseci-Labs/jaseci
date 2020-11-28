import React, { Component } from "react";
import Day from "./components/day";
import LLCal from "./components/ll-cal";
import "react-calendar/dist/Calendar.css";
import { connect } from "react-redux";
import WktNoteForm from "./components/wkt-note";
import DeepMITs from "./components/deep-mits";
import { Container, Row, Col } from "react-bootstrap";

import {
  LoadingIndicator,
} from "./utils/utils";
import {
  faSync,
  faStar,
  faRunning,
  faGlassCheers,
  faTimesCircle,
} from "@fortawesome/free-solid-svg-icons";
import { workette_filters as w_filter } from "./utils/filters";
import DayBigPicture from "./components/day-big-picture";

class DayViewLeft extends Component {

  render() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];

    return (
      <Container fluid className="m-0 p-0">
        <LLCal />
        {current && (
          <DeepMITs
            w_id={current}
            label="Knock these out!"
            iconProps={{ icon: faStar, color: "gold" }}
            color="starred"
            items={w_filter.deepMIT()}
          />
        )}

        {current && (
          <DeepMITs
            w_id={current}
            label="Babysit these!"
            iconProps={{ icon: faRunning }}
            color="running"
            items={w_filter.deepRunning()}
          />
        )}
        {current && (
          <DeepMITs
            w_id={current}
            label="Active Rituals!"
            iconProps={{ icon: faSync }}
            color="starred"
            items={w_filter.deepActiveRituals()}
          />
        )}
        <Row>
          <Col md="auto">
            <LoadingIndicator
              is_loading={
                this.props.api.is_loading[this.props.api.is_loading.length - 1]
              }
            />
          </Col>
        </Row>
      </Container>
    );
  }
}

const map_state = (state) => ({
  session: state.session,
  workette: state.workette,
  api: state.api,
});

DayViewLeft = connect(map_state)(DayViewLeft);

class DayViewRight extends Component {
  render() {
    const { session, workette } = this.props;
    const current = workette.days[session.cur_date];
    return (
      <Container fluid className="m-0 p-0">
        {current && (
          <DeepMITs
            w_id={current}
            label="Everything Completed!"
            iconProps={{ icon: faGlassCheers, color: "green" }}
            color="mit-completed"
            items={w_filter.deepCompleted()}
          />
        )}

        {current && (
          <DeepMITs
            w_id={current}
            label="Everything Abandoned!"
            iconProps={{ icon: faTimesCircle }}
            color="mit-abandoned"
            items={w_filter.deepCanceled()}
          />
        )}
        {current && (
          <div>
            <Container fluid className="m-0 p-2 mb-3">
              Reflections of the Day
              <Row>
                <Col className=" p-0">
                  <WktNoteForm key={current} w_id={current} />
                </Col>
              </Row>
            </Container>
            <DayBigPicture w_id={current} />
          </div>
        )}
      </Container>
    );
  }
}

DayViewRight = connect(map_state)(DayViewRight);

class DayViewMain extends Component {
  state = {};
  render() {
    const { session, workette } = this.props;
    return (
      <React.Fragment>
        {workette.days[session.cur_date] && <Day />}
      </React.Fragment>
    );
  }
}

DayViewMain = connect(map_state)(DayViewMain);

export { DayViewLeft, DayViewRight, DayViewMain };

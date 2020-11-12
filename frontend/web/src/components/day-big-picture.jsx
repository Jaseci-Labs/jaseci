import React, { Component } from "react";
import Workette from "./workette";
import { connect } from "react-redux";
import WktNoteForm from "./wkt-note";
import { Container, Row, Col, Collapse } from "react-bootstrap";
import { workette_actions as wact } from "../store/workette";
import ReleaseModal from "../utils/release-modal";
import { faLeaf } from "@fortawesome/free-solid-svg-icons";
import WktButton from "./wkt-button";

class DayBigPicture extends Component {
  state = { show: false };

  componentDidMount() {}

  toggle = () => {
    const { session, workette } = this.props;
    const { cur_date } = session;
    if (!this.state.show && !workette.life[cur_date]) {
      this.props.get_life(cur_date);
    }
    if (!this.state.show && !workette.years[cur_date]) {
      this.props.get_year(cur_date);
    }
    if (!this.state.show && !workette.months[cur_date]) {
      this.props.get_month(cur_date);
    }
    if (!this.state.show && !workette.weeks[cur_date]) {
      this.props.get_week(cur_date);
    }
    this.setState({ show: !this.state.show });
  };

  render() {
    const { session, workette } = this.props;
    const { cur_date } = session;
    const current = workette.days[session.cur_date];
    return (
      <Container key={cur_date} fluid className="p-0 m-0">
        <WktButton
          icon={faLeaf}
          status={this.state.show}
          tooltip="Show Big Picture"
          onClick={this.toggle}
        />
        <Collapse in={this.state.show} unmountOnExit={true}>
          <div>
            <strong>Life's</strong> Mission/Purpose Statement
            {workette.life[cur_date] && (
              <WktNoteForm w_id={workette.life[cur_date]} />
            )}
            <br />
            By the end of this <strong>year</strong> I want
            {workette.years[cur_date] && (
              <WktNoteForm w_id={workette.years[cur_date]} />
            )}
            <br />
            This <strong>month</strong> my key goals are
            {workette.months[cur_date] && (
              <WktNoteForm w_id={workette.months[cur_date]} />
            )}
            <br />
            Things I must accomplish this <strong>week</strong> are
            {workette.weeks[cur_date] && (
              <WktNoteForm w_id={workette.weeks[cur_date]} />
            )}
          </div>
        </Collapse>
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

export default connect(map_state, map_dispatch)(DayBigPicture);

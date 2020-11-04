import React, { Component } from "react";
import { Input, ServerErrors } from "../utils/utils";
import { connect } from "react-redux";
import { session_actions as session } from "../store/session";
import { Redirect } from "react-router-dom";
import { Container, Row, Col } from "react-bootstrap";

class Register extends Component {
  state = {
    email: "",
    pass: "",
    pass_dup: "",
    full_name: "",
    access_code: "",
    errors: [],
  };

  handleSubmit = (e) => {
    const { email, pass, full_name, access_code } = this.state;
    e.preventDefault();

    if (access_code === "GROW") {
      //Call server
      this.setState({ errors: [] });
      this.props.create({ email, pass, full_name });
      this.setState({ pass: "", pass_dup: "" });
    } else {
      this.setState({ errors: ["Invalid Access Code"] });
    }
  };

  handleChange = (e) => {
    if (e.currentTarget.name === "email") {
      this.setState({ email: e.currentTarget.value });
    } else if (e.currentTarget.name === "password") {
      this.setState({ pass: e.currentTarget.value });
    } else if (e.currentTarget.name === "pass_dup") {
      this.setState({ pass_dup: e.currentTarget.value });
    } else if (e.currentTarget.name === "full_name") {
      this.setState({ full_name: e.currentTarget.value });
    } else if (e.currentTarget.name === "access_code") {
      this.setState({ access_code: e.currentTarget.value });
    }
  };

  //unused?
  validate = () => {
    const { email, pass, pass_dup } = this.state;
    let errors = [];
    if (email.trim() === "") {
      errors.push("Please enter valid email address. ");
    } else if (pass.trim() === "") {
      errors.push("Please enter password. ");
    } else if (pass_dup.trim() !== pass.trim()) {
      errors.push("Passwords do not match. ");
    }
    this.setState({ errors: errors });
  };

  render() {
    const {
      email,
      pass,
      pass_dup,
      full_name,
      access_code,
      errors,
    } = this.state;
    const showError = this.props.session.error;
    showError.ferror = errors;

    return (
      <Container>
        <ServerErrors errors={showError} />
        {this.props.session.token === "user_created" && (
          <Redirect to="/login" />
        )}
        <form className="mt-0" onSubmit={this.handleSubmit}>
          <Row>
            <Col>
              <Input
                value={email}
                onChange={this.handleChange}
                name="email"
                label="Email address"
              />
            </Col>
          </Row>
          <Row>
            <Col>
              <Input
                value={pass}
                onChange={this.handleChange}
                name="password"
                type="password"
                label="Password"
              />
            </Col>
          </Row>
          <Row>
            <Col>
              <Input
                value={pass_dup}
                onChange={this.handleChange}
                name="pass_dup"
                type="password"
                label="Re-enter Password"
              />
            </Col>
          </Row>
          <Row>
            <Col>
              <Input
                value={full_name}
                onChange={this.handleChange}
                name="full_name"
                label="Full Name"
              />
            </Col>
          </Row>
          <Row>
            <Col>
              <Input
                value={access_code}
                onChange={this.handleChange}
                name="access_code"
                label="Access Code"
                autocomplete="off"
              />
            </Col>
          </Row>

          <Row>
            <Col className="d-flex justify-content-center">
              <button
                // disabled={errors.length}
                type="submit"
                className="btn btn-primary mt-3"
              >
                Register
              </button>
            </Col>
          </Row>
        </form>
      </Container>
    );
  }
}

//Connect this component to store.session
const map_state = (state) => ({
  session: state.session,
});

const map_dispatch = (dispatch) => ({
  create: ({ email, pass, full_name }) =>
    dispatch(session.create({ email, pass, full_name })),
});

export default connect(map_state, map_dispatch)(Register);

import React, { Component } from "react";
import { Input, ServerErrors } from "../utils/utils";
import { connect } from "react-redux";
import { session_actions as session } from "../store/session";
import { Redirect } from "react-router-dom";

class Register extends Component {
  state = { email: "", pass: "", pass_dup: "", full_name: "", errors: [] };

  handleSubmit = (e) => {
    const { email, pass, full_name } = this.state;
    e.preventDefault();
    //Call server
    this.props.create({ email, pass, full_name });
    this.setState({ pass: "", pass_dup: "" });
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
    }
  };

  validate = () => {
    const { email, pass, errors, pass_dup } = this.state;
    errors.length = 0;
    if (email.trim() === "") {
      errors.push("Email required;\n");
    }
    if (pass.trim() === "") {
      errors.push("Password required;\n");
    }
    if (pass_dup.trim() === "") {
      errors.push("Re-enter password;\n");
    }
    if (pass_dup.trim() !== pass.trim()) {
      errors.push("Passwords do not match;\n");
    }
  };

  render() {
    const { email, pass, pass_dup, full_name, errors } = this.state;
    return (
      <div className="container-sm">
        <ServerErrors errors={this.props.session.error} />
        {this.props.session.token === "user_created" && (
          <Redirect to="/login" />
        )}
        <h1>Register</h1>
        <br />
        <form onSubmit={this.handleSubmit}>
          <Input
            value={email}
            onChange={this.handleChange}
            name="email"
            label="Email address"
            description="Enter a valid email address."
          />
          <Input
            value={pass}
            onChange={this.handleChange}
            name="password"
            type="password"
            label="Password"
            description="Enter your password."
          />
          <Input
            value={pass_dup}
            onChange={this.handleChange}
            name="pass_dup"
            type="password"
            label="Re-enter Password"
            description="Please re-enter password."
          />
          <Input
            value={full_name}
            onChange={this.handleChange}
            name="full_name"
            label="Full Name"
            description="(optional) Enter full name."
          />

          <button
            disabled={errors.length}
            type="submit"
            className="btn btn-primary"
          >
            Register
          </button>
        </form>
        <br />
        {this.validate()}
        {errors.length !== 0 && (
          <div className="alert alert-danger">
            <pre>{errors}</pre>
          </div>
        )}
      </div>
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

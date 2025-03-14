// @flow
import React from "react"

import { Formik, Field, Form } from "formik"

import { PasswordInput, EmailInput } from "./elements/inputs"

import type { User } from "../../flow/authTypes"

import { changeEmailValidationRegex } from "../../lib/validation"

type Props = {
  onSubmit: Function,
  user: User
}

export type ChangeEmailFormValues = {
  email: string,
  confirmPassword: string
}

const ChangeEmailForm = ({ onSubmit, user }: Props) => {
  return (
    <Formik
      onSubmit={onSubmit}
      initialValues={{
        email:           user.email,
        confirmPassword: ""
      }}
      render={({ isSubmitting }) => (
        <Form>
          <section className="email-section">
            <h4>Change Email</h4>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <span className="required">*</span>
              <Field
                name="email"
                id="email"
                className="form-control"
                component={EmailInput}
                autoComplete="email"
                required
                pattern={changeEmailValidationRegex(user.email)}
                title="Email must be different than your current one."
              />
            </div>
            <div className="form-group">
              <label htmlFor="confirmPassword" className="row">
                <div className="col-auto fw-bold">
                  Confirm Password<span className="required">*</span>
                </div>
                <div className="col-auto subtitle">
                  Password required to change email address
                </div>
              </label>
              <Field
                id="confirmPassword"
                name="confirmPassword"
                className="form-control"
                component={PasswordInput}
                autoComplete="current-password"
                aria-describedby="confirmPasswordError"
                aria-label="Confirm Password"
                required
              />
            </div>
          </section>

          <div className="row submit-row no-gutters">
            <div className="col d-flex justify-content-end">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                Submit
              </button>
            </div>
          </div>
        </Form>
      )}
    />
  )
}

export default ChangeEmailForm

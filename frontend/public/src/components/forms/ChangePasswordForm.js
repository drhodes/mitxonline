// @flow
import React from "react"

import { Formik, Field, Form, ErrorMessage } from "formik"

import { PasswordInput } from "./elements/inputs"
import FormError from "./elements/FormError"
import {
  passwordFieldRegex,
  passwordFieldErrorMessage,
  changePasswordFormValidation
} from "../../lib/validation"

type Props = {
  onSubmit: Function
}

export type ChangePasswordFormValues = {
  oldPassword: string,
  newPassword: string,
  confirmPassword: string
}

const ChangePasswordForm = ({ onSubmit }: Props) => (
  <Formik
    onSubmit={onSubmit}
    validationSchema={changePasswordFormValidation}
    initialValues={{
      oldPassword:     "",
      newPassword:     "",
      confirmPassword: ""
    }}
    validateOnChange={false}
    validateOnBlur={false}
    render={({ isSubmitting }) => (
      <Form>
        <section className="email-section">
          <h4>Change Password</h4>
          <div className="form-group">
            <label htmlFor="oldPassword">Old Password</label>
            <span className="required">*</span>
            <Field
              name="oldPassword"
              id="oldPassword"
              className="form-control"
              component={PasswordInput}
              autoComplete="current-password"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="newPassword">New Password</label>
            <span className="required">*</span>
            <Field
              name="newPassword"
              id="newPassword"
              className="form-control"
              component={PasswordInput}
              autoComplete="new-password"
              aria-describedby="newPasswordError"
              required
              pattern={passwordFieldRegex}
              title={passwordFieldErrorMessage}
            />
            <ErrorMessage
              name="newPassword"
              id="newPasswordError"
              component={FormError}
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <span className="required">*</span>
            <Field
              name="confirmPassword"
              id="confirmPassword"
              className="form-control"
              component={PasswordInput}
              autoComplete="new-password"
              aria-describedby="confirmPasswordError"
              required
              pattern={passwordFieldRegex}
              title={passwordFieldErrorMessage}
            />
            <ErrorMessage
              name="confirmPassword"
              id="confirmPasswordError"
              component={FormError}
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

export default ChangePasswordForm

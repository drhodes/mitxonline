// @flow
import React from "react"
import { Formik, Form } from "formik"

import {
  newAccountValidation,
  legalAddressValidation,
  profileValidation,
  LegalAddressFields
} from "./ProfileFormFields"

import type { Country } from "../../flow/authTypes"

type Props = {
  onSubmit: Function,
  countries: Array<Country>
}

const INITIAL_VALUES = {
  name:          "",
  password:      "",
  username:      "",
  legal_address: {
    first_name: "",
    last_name:  "",
    country:    "",
    state:      ""
  },
  user_profile: {
    year_of_birth: ""
  }
}

const RegisterDetailsForm = ({ onSubmit, countries }: Props) => (
  <Formik
    onSubmit={onSubmit}
    validationSchema={legalAddressValidation
      .concat(newAccountValidation)
      .concat(profileValidation)}
    initialValues={INITIAL_VALUES}
    validateOnChange={false}
    validateOnBlur={false}
    render={({ isSubmitting, setFieldValue, setFieldTouched, values }) => (
      <Form>
        <LegalAddressFields
          countries={countries}
          setFieldValue={setFieldValue}
          setFieldTouched={setFieldTouched}
          values={values}
          isNewAccount={true}
        />
        <div className="row submit-row no-gutters">
          <div className="col d-flex justify-content-end">
            <button
              type="submit"
              className="btn btn-primary btn-gradient-red large"
              disabled={isSubmitting}
            >
              Continue
            </button>
          </div>
        </div>
      </Form>
    )}
  />
)

export default RegisterDetailsForm

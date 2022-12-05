// @flow
import React from "react"
import moment from "moment"
import { isNil } from "ramda"

import { notNil, parseDateString, formatPrettyDateTimeAmPmTz } from "./util"

import { NODETYPE_OPERATOR, NODETYPE_COURSE, NODEOPER_ALL } from "../constants"

import type Moment from "moment"

import type {
  CourseRunDetail,
  CourseRun,
  RunEnrollment,
  RequirementNode,
  LearnerRecord,
  ProgramRequirement
} from "../flow/courseTypes"
import type { CurrentUser } from "../flow/authTypes"

export const isLinkableCourseRun = (
  run: CourseRunDetail,
  currentUser: CurrentUser,
  dtNow?: Moment
): boolean => {
  if (isNil(run.courseware_url)) {
    return false
  }
  if (!currentUser.is_anonymous && currentUser.is_editor) {
    return true
  }
  const now = dtNow || moment()
  return notNil(run.start_date) && moment(run.start_date).isBefore(now)
}

export const isWithinEnrollmentPeriod = (run: CourseRunDetail): boolean => {
  const enrollStart = run.enrollment_start ? moment(run.enrollment_start) : null
  const enrollEnd = run.enrollment_end ? moment(run.enrollment_end) : null
  const now = moment()
  return (
    !!enrollStart &&
    now.isAfter(enrollStart) &&
    (isNil(enrollEnd) || now.isBefore(enrollEnd))
  )
}

export const courseRunStatusMessage = (run: CourseRun) => {
  const startDateDescription = generateStartDateText(run)
  if (startDateDescription !== null) {
    if (startDateDescription.active) {
      if (moment(run.end_date).isBefore(moment())) {
        const dateString = parseDateString(run.end_date)
        return (
          <span>
            {" "}
            | <strong>Ended</strong> - {formatPrettyDateTimeAmPmTz(dateString)}
          </span>
        )
      } else {
        return (
          <span>
            {" "}
            |<strong className="active-enrollment-text">
              {" "}
              Active
            </strong> from {startDateDescription.datestr}
          </span>
        )
      }
    } else {
      return (
        <span>
          {" "}
          | <strong className="text-dark">Starts</strong>{" "}
          {startDateDescription.datestr}
        </span>
      )
    }
  } else {
    return null
  }
}

export const generateStartDateText = (run: CourseRunDetail) => {
  if (run.start_date) {
    const now = moment()
    const startDate = parseDateString(run.start_date)
    const formattedStartDate = formatPrettyDateTimeAmPmTz(startDate)
    return now.isBefore(startDate)
      ? { active: false, datestr: formattedStartDate }
      : { active: true, datestr: formattedStartDate }
  }

  return null
}

export const isFinancialAssistanceAvailable = (run: CourseRunDetail) => {
  return run.page ? !!run.page.financial_assistance_form_url : false
}

export const enrollmentHasPassingGrade = (enrollment: RunEnrollment) => {
  if (enrollment.grades && enrollment.grades.length > 0) {
    for (let i = 0; i < enrollment.grades.length; i++) {
      if (enrollment.grades[i].passed) {
        return true
      }
    }
  }

  return false
}

const isNodeCompleted = (
  node: RequirementNode,
  learnerRecord: LearnerRecord
) => {
  // Determines if the node itself is complete using the rules above

  if (node.node_type !== NODETYPE_COURSE) {
    return true
  }

  const course = learnerRecord.program.courses.find(
    course => course.id === node.course
  )

  return course && course.grade && course.certificate
}

const walkNodes = (node: ProgramRequirement, learnerRecord: LearnerRecord) => {
  // Processes the node. if the node is an operator, roll through each child
  // node and recurse. If the node is a course, check if it's completed.

  if (node.data.node_type === NODETYPE_OPERATOR) {
    let completedCount = 0

    node.children.forEach(child => {
      completedCount += walkNodes(child, learnerRecord)
    })

    if (node.data.operator === NODEOPER_ALL) {
      return completedCount === node.children.length ? 1 : 0
    } else {
      return completedCount >= parseInt(node.data.operator_value) ? 1 : 0
    }
  } else if (node.data.node_type === NODETYPE_COURSE) {
    return isNodeCompleted(node.data, learnerRecord) ? 1 : 0
  }

  return false
}

export const learnerProgramIsCompleted = (learnerRecord: LearnerRecord) => {
  /*
    Checks to see if the learner has completed the program they're in. This
    is for use with learner records.

    A program is completed if:
    * It has requirements
    * All of the requirements listed in the Required Courses node are done
    * The Electives (if there are any) are also done

    A course is completed if:
    * It has a grade
    * A certificate has been issued for the course
  */

  if (!learnerRecord || learnerRecord.program.requirements.length === 0) {
    return false
  }

  const requiredCourses = learnerRecord.program.requirements[0].children[0]
  const electiveCourses = learnerRecord.program.requirements[0].children[1]

  const requirementsDone = walkNodes(requiredCourses, learnerRecord)
  const electivesDone = walkNodes(electiveCourses, learnerRecord)

  return requirementsDone && electivesDone
}

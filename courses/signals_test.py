"""
Tests for signals
"""
from unittest.mock import patch

import pytest

from courses.factories import (
    CourseFactory,
    CourseRunCertificateFactory,
    CourseRunFactory,
    ProgramFactory,
    ProgramRequirementFactory,
    UserFactory,
)

pytestmark = pytest.mark.django_db


# pylint: disable=unused-argument
@patch("courses.signals.transaction.on_commit", side_effect=lambda callback: callback())
@patch("courses.signals.generate_multiple_programs_certificate", autospec=True)
def test_create_course_certificate(generate_program_cert_mock, mock_on_commit):
    """
    Test that generate_multiple_programs_certificate is called when a course
    certificate is created
    """
    user = UserFactory.create()
    course_run = CourseRunFactory.create()
    program = ProgramFactory.create()
    program.add_requirement(course_run.course)
    cert = CourseRunCertificateFactory.create(user=user, course_run=course_run)
    generate_program_cert_mock.assert_called_once_with(user, [program])
    cert.save()
    generate_program_cert_mock.assert_called_once_with(user, [program])


# pylint: disable=unused-argument
@patch("courses.signals.transaction.on_commit", side_effect=lambda callback: callback())
@patch("courses.signals.generate_multiple_programs_certificate", autospec=True)
def test_generate_program_certificate_not_called(
    generate_program_cert_mock, mock_on_commit
):
    """
    Test that generate_multiple_programs_certificate is not called when a course
    is not associated with program.
    """
    user = UserFactory.create()
    course = CourseFactory.create()
    course_run = CourseRunFactory.create(course=course)
    cert = CourseRunCertificateFactory.create(user=user, course_run=course_run)
    cert.save()
    generate_program_cert_mock.assert_not_called()

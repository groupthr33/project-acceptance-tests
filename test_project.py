from django.test import TestCase
from app.controllers.command_line_controller import CommandLineController
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.models.account import Account
from app.models.course import Course


class TestProject(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='theuser', password='thepassword', name='thename',
                                              is_logged_in=True, roles=0x8)

        instructor = Account.objects.create(username='test_account', password='thepassword', name='accountname',
                                              is_logged_in=False, roles=0x2)

        Account.objects.create(username='test_ta', password='thepassword', name='taname',
                               is_logged_in=False, roles=0x1)

        Course.objects.create(course_id='CS417', section='001', name='Theory of Computation', schedule='TH12001315', instructor=instructor)

        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.course_service = CourseService()

        self.app = CommandLineController(self.auth_service, self.account_service, self.course_service)
        self.app.auth_service.current_account = self.account

    def test_del_account_happy_path(self):
        actual_response = self.project.command("del_account test_account")
        expected_response = "Account for test_account deleted."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_does_not_exist(self):
        actual_response = self.project.command("del_account dne")
        expected_response = "There is no account with user_name dne."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_wrong_number_of_args(self):
        actual_response = self.project.command("del_account test_account john")
        expected_response = "del_account must have exactly 1 argument. Correct usage: del_account <user_name>"

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_one_field(self):
        actual_response = self.project.command("edit_account test_account phone 5557654321")
        expected_response = "test_account phone update to 5557654321."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_multiple_fields(self):
        actual_response = self.project.command("edit_account test_account phone 5557654321 home '224 Street Rd.'")
        expected_response = "test_account phone and home updated."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_wrong_number_of_arguments(self):
        actual_response = self.project.command("edit_account test_account")
        expected_response = "edit_account must have exactly at least 3 arguments. Correct usage: cr_account <user_name> <field> <value> ..."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_user_does_not_exist(self):
        actual_response = self.project.command("edit_account mrwatts")
        expected_response = "There is no account with user_name mrwatts."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_invalid_field(self):
        actual_response = self.project.command("edit_account test_account address")
        expected_response = "address is not a valid field."

        self.assertEqual(expected_response, actual_response)

    def test_notify_all(self):
        actual_response = self.project.command("notify mySubject myContent")
        expected_response = "All users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_one_user(self):
        actual_response = self.project.command("notify mySubject myContent -u test_account")
        expected_response = "User test_account has been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_multi_user(self):
        Account.objects.create(username='jroth', password='thepassword', name='accountname',
                               is_logged_in=False, roles=0x1)

        actual_response = self.project.command("notify mySubject myContent -u jroth test_account")
        expected_response = "2 users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_user_does_not_exist(self):
        actual_response = self.project.command("notify mySubject myContent -u jroth")
        expected_response = "User jroth does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_happy_path(self):
        actual_response = self.project.command("assign_ta test_ta CS417 001")
        expected_response = "test_ta assigned to CS417-001"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_wrong_number_of_args(self):
        actual_response = self.project.command("assign_ins test_ta")
        expected_response = "assign_ta must have 2 or 3 arguments. Correct usage: assign_ta <user_name> <courseid> -s <section>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_does_not_exist(self):
        actual_response = self.project.command("assign_ins theta CS417 001")
        expected_response = "TA with user_name theta does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_does_not_exist(self):
        actual_response = self.project.command("assign_ta test_ta CS337 001")
        expected_response = "Course with ID CS337-001 does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_is_not_a_ta(self):
        actual_response = self.project.command("assign_ta test_account CS417 001")
        expected_response = "User test_account does not have the ta role."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_with_section(self):
        # put class with ID cs417 in storage (with lab section 801 in labsections field)
        # put lab section with ID 801 in storage (with cs417 in course field)

        actual_response = self.project.command("assign_ta test_ta CS417 001 -s 801")
        expected_response = "User test_ta assigned to CS417-001 lab section 801."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_section_does_not_exist(self):
        actual_response = self.project.command("assign_ta test_ta CS417 001 -s 802")
        expected_response = "Section 802 is not a valid session for CS417-001."

        self.assertEqual(expected_response, actual_response)

    def test_course_assignments(self):
        # assign ta to CS417-001

        actual_response = self.project.command("course_assignments CS417 001")
        expected_response = "CS417-001:\nInstructor: accountname\n\nTAs:\ntaname\n"

        self.assertEqual(expected_response, actual_response)

    def test_ta_assignments(self):
        # put lab_section 801 with ta field set to the_ta
        actual_response = self.project.command("ta_assignments")
        expected_response = "CS417-001:\nInstructor: accountname\n\nTAs:\ntaname - 801\n"

        self.assertEqual(expected_response, actual_response)

    def test_contact(self):
        #put in contact info

        actual_response = self.project.command("contact test_account")
        expected_response = "test_account John 5551234 theuser@uwm.edu"

        self.assertEqual(expected_response, actual_response)
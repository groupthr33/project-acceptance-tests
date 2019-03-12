import unittest
from project import Project


class TestProject(unittest.TestCase):

    def setUpClass(cls):
        # open connection to storage
        pass

    def setUp(self):
        self.project = Project()
        self.commands = ["course", "cr_account"] # TODO: add all commands (with args)
        self.roles = ["admin", "supervisor", "ta", "instructor"]

        # TODO: update to reflect actual privileges
        self.allowed_commands = {
            "admin": ["course", "cr_account"],
            "supervisor": ["course", "cr_account"],
            "ta": ["course", "cr_account"],
            "instructor":["course", "cr_account"]
        }

    def test_logged_out(self):
        responses = []
        for command in self.commands:
            responses.append(self.project.command(command))

        for response in responses:
            self.assertEqual("You need to log in first.", response)

    def test_privileges(self):
        for role in self.roles:
            for command in self.commands:
                response = self.project.command(command)
                if response == "You don't have privileges.":
                    self.assertEqual(command in self.allowed_commands[role], False)

    def test_course_happy_path(self):
        actual_response = self.project.command("course CS361 'Intro to Software Eng.'")
        expected_response = "361 Intro to Software Eng. created!"

        self.assertEqual(expected_response, actual_response)

    def test_course_wrong_number_of_args(self):
        actual_response = self.project.command("course CS361")
        expected_response = "course must have exactly 2 arguments. Correct usage: 'course <courseid> <coursename>"

        self.assertEqual(expected_response, actual_response)

    def test_course_already_exists(self):
        # put course in storage with id CS111

        actual_response = self.project.command("course CS111 'test course'")
        expected_response = "There is already a course with this ID."

        self.assertEqual(expected_response, actual_response)

    def test_course_id_wrong_format(self):
        actual_response = self.project.command("course 534CS 'test course'")
        expected_response = "Course ID not valid. Please check format."

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_happy_path(self):
        actual_response = self.project.command("cr_account mrwatts matt admin")
        expected_response = "Admin account created for mrwatts."

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_wrong_number_of_args(self):
        actual_response = self.project.command("cr_account mrwatts")
        expected_response = "cr_account must have exactly 2 arguments. Correct usage: cr_account <role> <user_name>"

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_already_exists(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("cr_account mrwatts matt admin")
        expected_response = "Account with user_name mrwatts already exists."

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_invalid_role(self):
        actual_response = self.project.command("cr_account mrwatts matt superman")
        expected_response = "Superman is not a valid role. Valid roles are: supervisor, admin, ta, and instructor"

        self.assertEqual(expected_response, actual_response)

    def test_cr_account_multiple_roles(self):
        actual_response = self.project.command("cr_account mrwatts matt admin ta")
        expected_response = "Account created for mrwatts with roles: admin, ta."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_happy_path(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("del_account mrwatts")
        expected_response = "Account for mrwatts deleted."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_does_not_exist(self):
        actual_response = self.project.command("del_account dne")
        expected_response = "There is no account with user_name dne."

        self.assertEqual(expected_response, actual_response)

    def test_del_account_wrong_number_of_args(self):
        actual_response = self.project.command("del_account mrwatts john")
        expected_response = "del_account must have exactly 1 argument. Correct usage: del_account <user_name>"

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_one_field(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("edit_account mrwatts phone 5557654321")
        expected_response = "mrwatts phone update to 5557654321."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_multiple_fields(self):
        # put account with user_name mrwatts in storage

        actual_response = self.project.command("edit_account mrwatts phone 5557654321 home '224 Street Rd.'")
        expected_response = "mrwatts phone and home updated."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_wrong_number_of_arguments(self):
        actual_response = self.project.command("edit_account mrwatts")
        expected_response = "edit_account must have exactly at least 3 arguments. Correct usage: cr_account <user_name> <field> <value> ..."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_user_does_not_exist(self):
        actual_response = self.project.command("edit_account mrwatts")
        expected_response = "There is no account with user_name mrwatts."

        self.assertEqual(expected_response, actual_response)

    def test_edit_account_invalid_field(self):
        actual_response = self.project.command("edit_account mrwatts address")
        expected_response = "address is not a valid field."

        self.assertEqual(expected_response, actual_response)

    def test_notify_all(self):

        actual_response = self.project.command("notify mySubject myContent")
        expected_response = "All users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_one_user(self):
        # put user with username jroth in storage

        actual_response = self.project.command("notify mySubject myContent -u jroth")
        expected_response = "User jroth has been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_multi_user(self):
        # put users with username jroth and mstevens in storage

        actual_response = self.project.command("notify mySubject myContent -u jroth mstevens")
        expected_response = "2 users have been notified."

        self.assertEqual(expected_response, actual_response)

    def test_notify_user_does_not_exist(self):

        actual_response = self.project.command("notify mySubject myContent -u jroth mstevens")
        expected_response = "User jroth does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_happy_path(self):
        # put course with ID cs417 in storage
        # put instructor with user_name theinstructor in storage

        actual_response = self.project.command("assign_ins theinstructor cs417")
        expected_response = "theinstructor assigned to cs417"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_wrong_number_of_args(self):
        actual_response = self.project.command("assign_ins theinstructor")
        expected_response = "assign_ins must have exactly 2 arguments. Correct usage: assign_ins <user_name> <courseid>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_instructor_does_not_exist(self):
        # put course with ID cs417 in storage

        actual_response = self.project.command("assign_ins theinstructor cs417")
        expected_response = "Instructor with user_name theinstructor does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_course_does_not_exist(self):
        # put instructor with user_name theinstructor in storage

        actual_response = self.project.command("assign_ins theinstructor cs417")
        expected_response = "Course with ID cs417 does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ins_instructor_is_not_an_instructor(self):
        # put admin with user_name justanadmin in storage

        actual_response = self.project.command("assign_ins justanadmin cs417")
        expected_response = "User justanadmin does not have the instructor role."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_happy_path(self):
        # put course with ID cs417 in storage
        # put ta with user_name theta in storage

        actual_response = self.project.command("assign_ta theta cs417")
        expected_response = "theta assigned to cs417"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_wrong_number_of_args(self):
        actual_response = self.project.command("assign_ins theta")
        expected_response = "assign_ta must have 2 or 3 arguments. Correct usage: assign_ta <user_name> <courseid> -s <section>"

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_does_not_exist(self):
        # put course with ID cs417 in storage

        actual_response = self.project.command("assign_ins theta cs417")
        expected_response = "TA with user_name theta does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_course_does_not_exist(self):
        # put ta with user_name theta in storage

        actual_response = self.project.command("assign_ta theta cs417")
        expected_response = "Course with ID cs417 does not exist."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_ta_is_not_a_ta(self):
        # put admin with user_name justanadmin in storage

        actual_response = self.project.command("assign_ta justanadmin cs417")
        expected_response = "User justanadmin does not have the ta role."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_with_section(self):
        # put ta with user_name theta in storage
        # put class with ID cs417 in storage (with lab section 111 in labsections field)
        # put lab section with ID 111 in storage (with cs417 in course field)

        actual_response = self.project.command("assign_ta theta cs417 -s 111")
        expected_response = "User theta assigned to cs418 labsection 111."

        self.assertEqual(expected_response, actual_response)

    def test_assign_ta_section_does_not_exist(self):
        # put ta with user_name theta in storage
        # put class with ID cs417 in storage

        actual_response = self.project.command("assign_ta theta cs417 -s 111")
        expected_response = "Section 111 is not a valid session for cs417. "

        self.assertEqual(expected_response, actual_response)

    def test_course_assignments(self):
        # put instructor with username theteacher in storage
        # put courses with instructor theteacher in storage

        actual_response = self.project.command("course_assignments")
        expected_response = "CS417 001, CS361 001"

        self.assertEqual(expected_response, actual_response)

    def test_ta_assignments(self):
        # put ta with username the_ta in storage
        # put lab_section with ta field set to the_ta
        actual_response = self.project.command("ta_assignments")
        expected_response = "the_ta: CS417 008, CS361 009"

        self.assertEqual(expected_response, actual_response)

    def test_contact(self):
        # put user with user_name theuser in storage

        actual_response = self.project.command("contact theuser")
        expected_response = "theuser John 5551234 theuser@uwm.edu"

        self.assertEqual(expected_response, actual_response)

    def test_login_happy_path(self):
        # put user with user_name theuser and password thepassword in storage

        actual_response = self.project.command("login theuser thepassword")
        expected_response = "theuser logged in."

        self.assertEqual(expected_response, actual_response)

        # assert user now has access to role specific functionality

    def test_login_user_does_not_exist(self):

        actual_response = self.project.command("login theuser thepassword")
        expected_response = "Incorrect username."

        self.assertEqual(expected_response, actual_response)

        # assert user does not have access to other any functionality

    def test_login_incorrect_password(self):
        # put user with user_name theuser and password thepassword in storage

        actual_response = self.project.command("login theuser mypassword")
        expected_response = "Incorrect password."

        self.assertEqual(expected_response, actual_response)

        # assert user does not have access to other any functionality

    def test_login_wrong_number_of_arguments(self):
        # put user with user_name theuser and password thepassword in storage

        actual_response = self.project.command("login theuser")
        expected_response = "login must have exactly 2 arguments. Correct usage: logout <username> <password>"

        self.assertEqual(expected_response, actual_response)

        # assert user still has access to appropriate functionality

    def test_logout_happy_path(self):
        # put user with user_name theuser and password thepassword in storage
        # set user's status in storage to logged_in
        # set the application state of current_user to theuser

        actual_response = self.project.command("logout")
        expected_response = "theuser is now logged out."

        self.assertEqual(expected_response, actual_response)

        # assert user does not have access to other any functionality

    def test_logout_wrong_number_of_arguments(self):
        # put user with user_name theuser and password thepassword in storage
        # set user's status in storage to logged_in
        # set the application state of current_user to theuser

        actual_response = self.project.command("logout please")
        expected_response = "logout must have exactly 0 arguments. Correct usage: logout"

        self.assertEqual(expected_response, actual_response)

        # assert user still has access to appropriate functionality

    def test_logout_no_logged_in_user(self):
        # set the application state of current_user to no one

        actual_response = self.project.command("logout")
        expected_response = "No one is currently logged in."

        self.assertEqual(expected_response, actual_response)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestProject))
runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
